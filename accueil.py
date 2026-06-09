import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Baptiste Sacuto - Portfolio", page_icon="📊", layout="wide")

# Sidebar commune à tout le portfolio
with st.sidebar:
    st.title("👨‍💻 Baptiste Sacuto")
    st.write("Data Analyst | Logistique & Flux")
    st.markdown("---")
    # Liens externes
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/baptiste-sacuto)")
    st.markdown("[🐙 GitHub](https://github.com/ton-profil)")

# Contenu de la page d'accueil
st.title("Bienvenue sur mon Portfolio Data 🚀")

st.markdown("""
"Mon truc à moi, c'est de faire le pont entre le métier et la technique.

Après des expériences variées sur le terrain — de la gestion de flux voyageurs à la logistique import chez Leclerc — j'ai basculé à fond dans la donnée pour mieux comprendre et automatiser ce qui se passe dans les coulisses.

Aujourd'hui, je ne me contente pas de faire des graphiques. Mon approche est orientée Data Engineering : je construis des pipelines robustes, du nettoyage en Python au stockage Cloud (AWS/PostgreSQL), pour que la donnée soit propre, disponible et exploitable.

Ce que tu trouveras ici :

Mes projets end-to-end : De l'ingestion API à la mise en production sur Streamlit.

Mon approche technique : Python, SQL, Docker et le déploiement Cloud.

Curieux de voir comment je travaille ? Explore mes réalisations via le menu à gauche."
""")

# --- BOUTON CV AMÉLIORÉ ---
try:
    with open("CV_Baptiste_SACUTO_Data_analyst.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    
    st.download_button(
        label="📥 Télécharger mon CV",
        data=PDFbyte,
        file_name="CV_Baptiste_Sacuto.pdf",
        mime='application/pdf'
    )
except FileNotFoundError:
    st.warning("⚠️ Fichier CV introuvable à la racine. Vérifie bien le nom du fichier.")