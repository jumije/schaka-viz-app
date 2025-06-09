import streamlit as st

st.set_page_config(
    page_title="Schaka Bioinformatics Learning Lab",
    page_icon="🧬",
    layout="wide"
)

# --- HIDE THE MAIN PAGE FROM THE SIDEBAR ---
# This is a small CSS trick to hide the first list item (which is this main page)
# in the sidebar navigation. This makes the app feel cleaner.
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


# --- WELCOME PAGE CONTENT (The rest is the same as before) ---
st.title("Welcome to the Bioinformatics Learning Lab! 🔬")

st.markdown("""
### A hands-on environment for your journey into cancer data analysis.

This interactive app is your companion for the "Genomische Geheimnisse" course. Here, you will not just see visualizations—you will build, modify, and experiment with them yourself.

#### How to Use This Lab:

1.  👈 **Navigate using the sidebar on the left.**
2.  **Start at the `Data Lab` page.** This is where you'll generate the simulated dataset that all other pages will use. You can create different scenarios to see how data properties affect the story a plot can tell.
3.  **Explore the visualization pages.** Each page is a lesson dedicated to a specific plot type.
    *   Read the **"Learn More"** section to understand the theory.
    *   Use the **"Control Panel"** to experiment with plot parameters without writing code.
    *   Tackle the **"Coding Sandbox"** to answer a scientific question by modifying Python code directly and seeing the results instantly!

Let's begin!
""")