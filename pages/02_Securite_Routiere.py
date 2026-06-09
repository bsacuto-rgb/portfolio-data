import streamlit as st

st.set_page_config(page_title="Sécurité Routière", layout="wide")

st.title("🛡️ Analyse : Sécurité Routière (2021-2024)")

# Introduction du projet
st.markdown("""
### 🎯 L'objectif
Analyser 4 ans de données (Fichier BAAC - ONISR) pour identifier les facteurs de gravité des accidents et proposer des leviers de prévention concrets aux autorités.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚙️ Architecture Data")
    st.write("Nous avons mis en place un pipeline ETL complet pour fiabiliser les données :")
    st.markdown("""
    - **Bronze :** Ingestion des fichiers CSV bruts (2021-2024).
    - **Silver :** Nettoyage et typage avec Python (Pandas).
    - **Gold :** Stockage dans PostgreSQL (via AWS RDS) pour une connexion BI fluide.
    """)
    st.image("assets/structure_medaillon.png", caption ="Pipeline complet")

with col2:
    st.subheader("📊 Résultats & Insights")
    st.write("Le dashboard permet de filtrer les accidents par zone et profil.")
    # Si tu as une image dans ton dossier assets, décommente la ligne ci-dessous :
    st.image("assets/dashboard_powerbi.png", caption="Dashboard de suivi")

st.divider()

st.subheader("🔍 Analyse & Observations")
st.write("Au-delà de l'architecture, l'analyse des données a révélé des tendances critiques :")

# Création de 3 colonnes pour les points clés
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**📍 Zones à risque**")
    st.write("Les routes départementales hors agglomération présentent un risque d'accident grave deux fois plus élevé.")
    st.image("assets/hors_agglo.png")

with col_b:
    st.markdown("**⏰ Facteurs temporels**")
    st.write("Le pic de gravité se situe entre 4h et 6h du matin, tandis que l'éclairage public réduit la gravité nocturne de 57%.")
    st.image("assets/illu.png")

with col_c:
    st.markdown("**👤 Profils vulnérables**")
    st.write("Les 15-25 ans et les seniors (65+) sont les populations les plus exposées aux accidents graves.")
    st.image("assets/profils.png")


st.divider()

st.subheader("💡 Mes Recommandations Stratégiques")
st.success("""
Après analyse, voici les 3 axes prioritaires identifiés pour réduire la gravité :
1. **Infrastructures :** Installation d'éclairage public et de glissières préventives sur les zones sombres accidentogènes.
2. **Ciblage :** Campagnes de sensibilisation spécifiques pour les 15-25 ans et les seniors (+65 ans).
3. **Contrôles :** Renforcement de la présence aux heures de trafic dense et de nuit.
""")
st.image("assets/conseils.png")