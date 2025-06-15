import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sidebar_datainput import show_sidebar_data_input
from io import StringIO
import sys

# Page configuration
st.set_page_config(layout="wide")
show_sidebar_data_input() # This line adds the sidebar to this page
st.title("📊 Heatmap Explorer")

# Check if data exists in session state
if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df = st.session_state['df_full']
gene_data = df[[col for col in df.columns if col.startswith('Gene_')]].T

# --- Guided Tour Expander (UPDATED) ---
with st.expander("LEARN: What is a Heatmap?"):
    st.markdown("""
    A **heatmap** visualizes a matrix as a grid of colors. It's especially powerful when combined with clustering to find patterns in large datasets like gene expression.

    #### How to Read This Plot:
    1.  **The Grid:** Each cell in the grid represents a single value (e.g., the expression of one gene in one sample).
    2.  **The Colors:** The color of each cell is mapped to its value. You must check the color bar legend to see what the colors mean (e.g., yellow is high, purple is low).
    3.  **The Dendrograms (Trees):** These trees on the rows and columns show the results of *hierarchical clustering*. Samples (or genes) that are grouped closely together on a branch are more similar to each other than those on distant branches. The primary goal is often to see if samples cluster by a known category, like 'Treated' vs. 'Control'.
    4.  **Data Scaling:** To make patterns visible, we almost always scale the data by gene (`z_score=0`). This means the colors represent the relative expression for that gene (e.g., "high for *this gene's* average"), not the absolute expression value.

    ---
    #### Dive Deeper (External Links):
    - 🔗 **[Seaborn `clustermap` Documentation](https://seaborn.pydata.org/generated/seaborn.clustermap.html):** This is the function we use. It combines a heatmap with clustering.
    - 🔗 **[The Python Graph Gallery - Heatmap](https://www.python-graph-gallery.com/heatmap/):** A great resource with many examples and explanations.
    """)

# --- Control Panel and Plot ---
st.header("EXPERIMENT: The Control Panel")
st.markdown("Use the widgets below to see how parameters change the plot.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    cmap_choice = st.selectbox("Colormap (`cmap`):", ('vlag', 'coolwarm', 'viridis', 'plasma'))
    show_annot = st.checkbox("Show values (`annot`)", value=False)
    cluster_rows = st.checkbox("Cluster Rows (Genes)", value=True)
    cluster_cols = st.checkbox("Cluster Columns (Samples)", value=True)
    
    st.info("The most impactful choice is scaling (`z_score`). Notice how without it (z_score=None), a few highly expressed genes dominate the colors, hiding the patterns in other genes.")
    z_score_option = st.radio("Scale data (Z-score)", ('by Row (Genes)', 'None'), horizontal=True, index=0)
    z_score_val = 0 if z_score_option == 'by Row (Genes)' else None
    
with col2:
    st.subheader("Interactive Plot")
    try:
        g = sns.clustermap(
            gene_data,
            cmap=cmap_choice,
            annot=show_annot,
            fmt=".1f" if show_annot else None,
            row_cluster=cluster_rows,
            col_cluster=cluster_cols,
            z_score=z_score_val,
            figsize=(10, 8)
        )
        st.pyplot(g)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- Coding Sandbox ---
st.header("DISCOVER: The Coding Sandbox")
st.markdown("Now it's your turn! Modify the code below to answer the scientific question.")

st.info("**Scientific Question:** Can you generate a heatmap that clearly separates the 'Treated' and 'Control' groups and uses the 'coolwarm' colormap?")

code_template = """
# Tip: You can access the gene expression data via the `gene_data` DataFrame.
# Try changing the `cmap`, `annot`, or `z_score` parameters.
# `z_score=0` scales by row, which is usually best. `z_score=1` scales by column.

fig = sns.clustermap(
    gene_data,
    cmap='viridis',
    z_score=0,          # Standardize by row (gene)
    figsize=(10, 8)
)

# Use st.pyplot() to display your plot in Streamlit!
st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=300)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        # The locals dict makes our data available to the executed code
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'gene_data': gene_data})
        
        # Get the output from the buffer
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
            
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")

    # Restore stdout
    sys.stdout = old_stdout