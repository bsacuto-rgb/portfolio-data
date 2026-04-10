
# import de ce dont on a besoin
import streamlit as st

#On crée la page avec son titre et un layout=wide pour que cela prenne toute la place de l'écran.
st.set_page_config(page_title="Mon Portfolio Data", layout="wide")

# Nous créeons directement la sidebar avec plusieurs onglets.

with st.sidebar:
    st.title ("🕹️ Navigation")
    choix = st.radio ("Aller à :", ["Qui suis-je ?", "Mes projets", "Contact"])

# On remplis nos pages
#Page de mon profil
if choix == "Qui suis-je ?":
    st.title("👤 Mon Profil")
    st.write("Bienvenue sur mon profil.")
    
    # On crée deux colonnes: une pour la présentation, une pour les soft skills/infos 
    col1, col2 = st.columns([2,1]) # On mets la colonne 1 plus large de 2 fois

    with col1:
        st.markdown("""
        ### 🎯 Mon Objectif
        Data Analyst fraîchement diplômé avec une forte appétence pour le **Data Engineering**. 
        Je ne me contente pas d'analyser les données, je m'assure qu'elles coulent de source de manière fiable et automatisée.
        """)
        
        # On crée un expander pour montré les détails de la formation sans prendre trop de place.
        with st.expander("🎓 Ma Formation"):
            st.write("""
            - **Formation Data Analyst** (3 mois intensifs)
            - Focus : SQL, Python, ETL, Docker, Cloud (AWS/GCP)
            """)

        with col2:
            st.info("**Technos préférées**")
            st.markdown("- 🐍 Python\n- 🐳 Docker")

# Page de mes projets
elif choix == ("Mes projets"):
    st.title("🛠️ Mes Projets")
    st.write("Cliquez sur les onglets pour explorer mes réalisations")

    # On crée les sous onglets
    tab_kaggle, tab_api = st.tabs(["📊 Analyse Kaggle","⚡ API Live"])

    #Mon onglet Kaggle:
    with tab_kaggle:
        st.subheader("Pipeline ETL sur Dataset Kaggle")
        st.write("ici on fera le taff")

    #Mon onglet tab_api
    with tab_api:
        st.subheader("Dashboard de données en temps réel")
        st.write("Ici on mettra la connexion à l'API")

# Page de mon contact
elif choix == ("Contact"):
    st.title("📩 Contact")
    st.write("Mon email : test@gmail.com")