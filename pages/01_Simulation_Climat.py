import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Simulation Climat", layout="wide")

st.title("🌍 Simulation Climatique & IA")

# --- 1. CHARGEMENT & TRAIN (En haut pour être disponible) ---
@st.cache_data
def load_data():
    # 1. Chargement
    df = pd.read_csv("energy_climat_clean.csv")
    
    # 2. CRUCIAL : Recalculer les colonnes nécessaires avant tout
    # Assure-toi que les colonnes 'gdp' et 'population' existent bien dans ton CSV
    df['gdp_per_capita'] = df['gdp'] / df['population']
    
    return df

@st.cache_resource
def train_model(df):
    features = ["gdp_per_capita", "population", "low_carbon_share_energy"]
    target = "co2_per_capita"
    
    # On nettoie les lignes vides sur les colonnes utilisées
    df_clean = df.dropna(subset=features + [target]).copy()
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(df_clean[features], df_clean[target])
    
    return rf, df_clean

df_ml = load_data()
model, df_clean = train_model(df_ml)

# --- 2. INTERFACE UTILISATEUR ---
tous_les_pays = sorted(df_ml['country'].unique())
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    pays_sel = st.selectbox("Choisir un pays :", tous_les_pays, index=tous_les_pays.index("India") if "India" in tous_les_pays else 0)
with col_ctrl2:
    scenario = st.radio("Scénario Énergétique :", ["Réaliste (Tendanciel historique)", "Éco-Optimiste (+2% Propre/an)"])
with col_ctrl3:
    st.markdown("**Hypothèses :**\n- Croissance PIB/hab : +2.0% / an\n- Croissance Pop : +0.8% / an")

# --- 3. LOGIQUE DE SIMULATION (Ton code) ---
df_pays = df_ml[df_ml['country'] == pays_sel]
row_2022 = df_pays[df_pays['year'] == 2022].iloc[0] if not df_pays[df_pays['year'] == 2022].empty else None

if row_2022 is not None:
    # Calcul pente historique
    df_recent = df_pays[(df_pays['year'] >= 2012) & (df_pays['year'] <= 2022)]
    pente = 0.0
    if len(df_recent) >= 2:
        pente = (df_recent.iloc[-1]['low_carbon_share_energy'] - df_recent.iloc[0]['low_carbon_share_energy']) / 10

    # Projection
    projections = [{'country': pays_sel, 'year': 2022, 'gdp_per_capita': row_2022['gdp_per_capita'], 
                    'population': row_2022['population'], 'low_carbon_share_energy': row_2022['low_carbon_share_energy'],
                    'co2_final': row_2022['co2_per_capita'], 'Source': 'Prédiction IA'}]

    for annee in range(2023, 2051):
        ecart = annee - 2022
        gdp_hab = row_2022['gdp_per_capita'] * (1.02 ** ecart)
        pop = row_2022['population'] * (1.008 ** ecart)
        clean_energy = row_2022['low_carbon_share_energy'] + ((pente if "Réaliste" in scenario else 2.0) * ecart)
        projections.append({'country': pays_sel, 'year': annee, 'gdp_per_capita': gdp_hab, 
                            'population': pop, 'low_carbon_share_energy': min(100, max(0, clean_energy)),
                            'co2_final': None, 'Source': 'Prédiction IA'})
    
    df_futur = pd.DataFrame(projections)
    df_futur.loc[1:, 'co2_final'] = model.predict(df_futur.iloc[1:][['gdp_per_capita', 'population', 'low_carbon_share_energy']])

    # Visualisation
    df_passe = df_pays[['country', 'year', 'gdp_per_capita', 'population', 'low_carbon_share_energy', 'co2_per_capita']].rename(columns={'co2_per_capita': 'co2_final'})
    df_passe['Source'] = 'Historique Réel'
    df_affichage = pd.concat([df_passe, df_futur], ignore_index=True)

    # Métriques
    c1, c2, c3 = st.columns(3)
    c1.metric("CO2 Réel (2022)", f"{row_2022['co2_per_capita']:.2f} t/hab")
    c2.metric("CO2 IA (2050)", f"{df_futur.iloc[-1]['co2_final']:.2f} t/hab")
    c3.metric("Énergie Propre 2050", f"{df_futur.iloc[-1]['low_carbon_share_energy']:.1f} %")

    fig = px.line(df_affichage, x="year", y="co2_final", color="Source", title=f"Trajectoire CO2 : {pays_sel}")
    fig.add_hline(y=2, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)