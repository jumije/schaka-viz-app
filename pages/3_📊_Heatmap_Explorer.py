import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import sys

# Page configuration
st.set_page_config(layout="wide")
st.title("📊 Heatmap Explorer")

# Check if data exists in session state
if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df = st.session_state['df_full']
gene_data = df[[col for col in df.columns if col.startswith('Gene_')]].T

# --- Guided Tour Expander ---
with st.expander("LEARN: What is a Heatmap?"):
    st.markdown("""
    A **heatmap** is a graphical representation of data where values in a matrix are represented as colors. It's fantastic for visualizing large, complex datasets like gene expression at a glance.
    
    - **When to Use:** To see the "big picture" and find patterns or clusters in your data. In genomics, we use it to see which genes behave similarly across which samples.
    - **Key Features:**
        - **Clustering:** It automatically groups similar rows (genes) and similar columns (samples) together, revealing relationships.
        - **Scaling (Z-score):** To make patterns visible, we often scale the data for each gene. A Z-score tells us how many standard deviations a value is from the mean of its gene. Red might mean "higher than average for this gene," and blue "lower than average."
    - **Pitfalls:** Be careful with color choice! A bad colormap can hide or misrepresent the story.
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