import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# On crée la page avec son titre et un layout=wide
st.set_page_config(page_title="Mon Portfolio Data", layout="wide")

# ==========================================
# FONCTIONS CACHÉES (MACHINE LEARNING)
# ==========================================
@st.cache_data
def load_data():
    # ⚠️ Remplace par le VRAI nom de ton fichier CSV (ex: 'owid-co2-data.csv')
    df = pd.read_csv("energy_climat_clean.csv") 
    df['gdp_per_capita'] = df['gdp'] / df['population']
    features = ["gdp_per_capita", "population", "low_carbon_share_energy"]
    target = "co2_per_capita"
    return df.dropna(subset=features + [target]).copy()

@st.cache_resource
def train_model(data):
    features = ["gdp_per_capita", "population", "low_carbon_share_energy"]
    target = "co2_per_capita"
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(data[features], data[target])
    return rf

# Chargement global des données et de l'IA
df_ml = load_data()
tous_les_pays = sorted(df_ml['country'].unique())
model = train_model(df_ml)


# ==========================================
# SIDEBAR (NAVIGATION)
# ==========================================
with st.sidebar:
    st.title("🕹️ Navigation")
    choix = st.radio("Aller à :", ["Qui suis-je ?", "Mes projets", "Contact"])


# ==========================================
# PAGE 1 : QUI SUIS-JE ?
# ==========================================
if choix == "Qui suis-je ?":
    st.title("👤 Mon Profil")
    st.write("Bienvenue sur mon profil.")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### 🎯 Mon Objectif
        Data Analyst fraîchement diplômé avec une forte appétence pour le **Data Engineering**. 
        Je ne me contente pas d'analyser les données, je m'assure qu'elles coulent de source de manière fiable et automatisée.
        """)
        
        with st.expander("🎓 Ma Formation"):
            st.write("""
            - **Formation Data Analyst** (3 mois intensifs)
            - Focus : SQL, Python, ETL, Machine Learning, Docker
            """)

    with col2:
        st.info("**Technos préférées**")
        st.markdown("- 🐍 Python\n- 🐳 Docker\n- 🤖 Scikit-Learn")


# ==========================================
# PAGE 2 : MES PROJETS (OÙ EST LE SIMULATEUR)
# ==========================================
elif choix == "Mes projets":
    st.title("🛠️ Mes Projets")
    st.write("Cliquez sur les onglets pour explorer mes réalisations")

    tab_kaggle, tab_api = st.tabs(["📊 Simulateur CO2 (Machine Learning)", "⚡ API Live"])

    # --- L'ONGLET DU SIMULATEUR CO2 ---
    with tab_kaggle:
        st.subheader("🤖 Pipeline ML : Prédiction des Émissions de CO2 (1990-2050)")
        st.write("Ce module utilise un modèle **Random Forest** pour simuler l'impact des politiques énergétiques mondiales.")
        
        # Petit panneau de contrôle spécifique à l'onglet
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            pays_sel = st.selectbox("Choisir un pays :", tous_les_pays, index=tous_les_pays.index("India") if "India" in tous_les_pays else 0)
        with col_ctrl2:
            scenario = st.radio("Scénario Énergétique :", ["Réaliste (Tendanciel historique)", "Éco-Optimiste (+2% Propre/an)"])
        with col_ctrl3:
            st.markdown("**Paramètres fixes (Futur) :**\n- Croissance PIB/hab : +2.0% / an\n- Croissance Pop : +0.8% / an")

        # 🏃‍♂️ ALGORITHME DE SIMULATION INTERACTIF
        df_pays = df_ml[df_ml['country'] == pays_sel]
        row_2022 = df_pays[df_pays['year'] == 2022]

        if row_2022.empty:
            st.warning(f"Pas de données 2022 disponibles pour : {pays_sel}")
        else:
            row_2022 = row_2022.iloc[0]
            
            # Calcul pente historique
            df_recent = df_pays[(df_pays['year'] >= 2012) & (df_pays['year'] <= 2022)]
            has_2012 = not df_recent[df_recent['year'] == 2012].empty
            has_2022 = not df_recent[df_recent['year'] == 2022].empty
            pente = (df_recent[df_recent['year'] == 2022]['low_carbon_share_energy'].values[0] - 
                     df_recent[df_recent['year'] == 2012]['low_carbon_share_energy'].values[0]) / 10 if (has_2012 and has_2022) else 0.0

            # 🏃‍♂️ ALGORITHME DE SIMULATION INTERACTIF CORRIGÉ
            projections = []
            
            # --- LE FIX : Point d'ancrage pour souder le graphique ---
            # On force le premier point du futur (2022) à prendre la VRAIE valeur historique
            projections.append({
                'country': pays_sel, 
                'year': 2022, 
                'gdp_per_capita': row_2022['gdp_per_capita'], 
                'population': row_2022['population'], 
                'low_carbon_share_energy': row_2022['low_carbon_share_energy'],
                'co2_final': row_2022['co2_per_capita'], # On utilise le vrai CO2 historique
                'Source': 'Prédiction IA' # Tagged "IA" pour que Plotly démarre sa ligne ici !
            })

            # La boucle reprend normalement à partir de 2023
            for annee in range(2023, 2051):
                ecart = annee - 2022
                gdp_hab = row_2022['gdp_per_capita'] * ((1 + 0.02) ** ecart) # +2% PIB/hab
                pop = row_2022['population'] * ((1 + 0.008) ** ecart)       # +0.8% Pop
                
                if scenario == "Réaliste (Tendanciel historique)":
                    clean_energy = row_2022['low_carbon_share_energy'] + (pente * ecart)
                else:
                    clean_energy = row_2022['low_carbon_share_energy'] + (2.0 * ecart)
                
                clean_energy = max(0.0, min(100.0, clean_energy))
                
                projections.append({
                    'country': pays_sel, 'year': annee, 'gdp_per_capita': gdp_hab, 
                    'population': pop, 'low_carbon_share_energy': clean_energy,
                    'co2_final': None, # L'IA va compléter cette case juste après
                    'Source': 'Prédiction IA'
                })
            
            df_futur = pd.DataFrame(projections)
            
            # L'IA fait sa prédiction uniquement sur les lignes futures réelles (2023 à 2050)
            X_futur = df_futur[['gdp_per_capita', 'population', 'low_carbon_share_energy']].iloc[1:]
            df_futur.loc[df_futur.index[1:], 'co2_final'] = model.predict(X_futur)

            # Préparation passé
            df_passe = df_pays[['country', 'year', 'gdp_per_capita', 'population', 'low_carbon_share_energy', 'co2_per_capita']].copy()
            df_passe = df_passe.rename(columns={'co2_per_capita': 'co2_final'})
            df_passe['Source'] = 'Historique Réel'

            df_affichage = pd.concat([df_passe, df_futur], ignore_index=True).sort_values('year')

            # 📊 AFFICHAGE DES RÉSULTATS DANS L'ONGLET
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("CO2 Réel (2022)", f"{row_2022['co2_per_capita']:.2f} t/hab")
            with col_m2:
                co2_2050 = df_futur.iloc[-1]['co2_final']
                st.metric("CO2 IA (2050)", f"{co2_2050:.2f} t/hab", delta=f"{co2_2050 - row_2022['co2_per_capita']:.2f} t")
            with col_m3:
                st.metric("Énergie Propre 2050", f"{df_futur.iloc[-1]['low_carbon_share_energy']:.1f} %")

            # Dessin de la courbe Plotly
            fig = px.line(df_affichage, x="year", y="co2_final", color="Source",
                          color_discrete_map={'Historique Réel': 'blue', 'Prédiction IA': 'green' if scenario == "Éco-Optimiste (+2% Propre/an)" else 'orange'},
                          title=f"Trajectoire CO2 : {pays_sel} ({scenario})",
                          labels={"co2_final": "CO2 par habitant (Tonnes)", "year": "Année"})
            fig.add_hline(y=2, line_dash="dash", line_color="red", annotation_text="Objectif GIEC (2t)")
            fig.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig, use_container_width=True)

    # L'autre onglet (vide pour l'instant)
    with tab_api:
        st.subheader("Dashboard de données en temps réel")
        st.write("Ici on mettra la connexion à l'API plus tard.")


# ==========================================
# PAGE 3 : CONTACT
# ==========================================
elif choix == "Contact":
    st.title("📩 Contact")
    st.write("Mon email : test@gmail.com")