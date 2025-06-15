import streamlit as st
from sidebar_datainput import show_sidebar_data_input

st.set_page_config(
    page_title="Schaka Bioinformatics Learning Lab",
    page_icon="🧬",
    layout="wide"
)

# --- Show the Sidebar Data Lab ---
show_sidebar_data_input()

# --- Main Page Welcome Content ---
st.title("Welcome to the Bioinformatics Learning Lab!")
st.markdown("### A hands-on environment for your journey into cancer data analysis.")
st.markdown("""
This interactive app is your companion for the "Genomische Geheimnisse" course. Here, you will not just see visualizations—you will build, modify, and experiment with them yourself.

#### How to Use This Lab:

1.  **Use the `Data Lab` in the sidebar to create and modify your dataset.** Choose a scenario or set custom parameters, then click **`Generate/Update Dataset`**.
2.  **The dataset is live!** Changes you make in the sidebar will immediately affect the plots on any page.
3.  **Navigate to a visualization page** using the links in the sidebar to start exploring.
""")

# A check to ensure data is loaded, and guide the user.
if 'df_full' in st.session_state:
    st.info("Dataset is ready. Choose a visualization from the sidebar to continue.")
else:
    st.error("There was an issue loading the data. Please try clicking the 'Generate/Update Dataset' button in the sidebar.")