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
st.title("🌋 Volcano Plot Explorer")

# Check if data exists in session state
if 'df_volcano' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df_volcano = st.session_state['df_volcano']

# --- Guided Tour Expander (UPDATED) ---
with st.expander("LEARN: What is a Volcano Plot?"):
    st.markdown("""
    A **volcano plot** is a type of scatter plot used to quickly identify meaningful data points from a large number of tests. It's the standard for visualizing differential expression results.

    #### How to Read This Plot:
    1.  **The X-Axis (log2 Fold Change):** This measures *how much* a gene's expression changed.
        -   Values > 0 mean the gene was **upregulated** (more expression in the treated group).
        -   Values < 0 mean the gene was **downregulated**.
        -   The further from zero, the larger the change.
    2.  **The Y-Axis (-log10 P-value):** This measures the *statistical significance* of the change. A higher value means the result is less likely due to random chance (i.e., more significant).
    3.  **The Quadrants:** The plot is divided by threshold lines into important zones:
        -   **Top Right:** Highly upregulated and significant genes (our best "hits").
        -   **Top Left:** Highly downregulated and significant genes (also great "hits").
        -   **Bottom/Center:** Genes that are not statistically significant or did not change much.

    ---
    #### Dive Deeper (External Links):
    - 🔗 **[BiostatSQUID - Volcano Plots](https://biostatsquid.com/volcano-plot/):** A great introduction to volcano plots, including how to interpret them and why they are useful.
    - 🔗 **[Seaborn `scatterplot` Documentation](https://seaborn.pydata.org/generated/seaborn.scatterplot.html):** Since there's no built-in `volcanoplot` function, we build it ourselves using a standard scatter plot!
    """)


# --- Control Panel and Plot ---
st.header("EXPERIMENT: The Control Panel")
st.markdown("Use the sliders to see how changing significance thresholds impacts which genes are identified as hits.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    pval_thresh = st.slider(
        "Significance Threshold (-log10 P-value)",
        min_value=0.0, max_value=10.0, value=2.0, step=0.1,
        help="Higher values make the significance test more strict."
    )
    fc_thresh = st.slider(
        "Fold Change Threshold (log2)",
        min_value=0.0, max_value=5.0, value=1.0, step=0.1,
        help="Filters for genes with at least this magnitude of change."
    )
    
    # Create a dynamic copy for the interactive plot
    df_interactive = df_volcano.copy()
    df_interactive['Significance'] = 'Not Significant'
    up_cond = (df_interactive['log2_Fold_Change'] > fc_thresh) & (df_interactive['neg_log10_p_value'] > pval_thresh)
    down_cond = (df_interactive['log2_Fold_Change'] < -fc_thresh) & (df_interactive['neg_log10_p_value'] > pval_thresh)
    df_interactive.loc[up_cond, 'Significance'] = 'Upregulated'
    df_interactive.loc[down_cond, 'Significance'] = 'Downregulated'
    
    # Display summary
    st.write("Genes selected as hits:")
    st.table(df_interactive['Significance'].value_counts())

with col2:
    st.subheader("Interactive Plot")
    fig, ax = plt.subplots(figsize=(9, 7))
    custom_palette = {'Upregulated':'red', 'Downregulated':'blue', 'Not Significant':'#BBBBBB'}
    
    sns.scatterplot(
        data=df_interactive, x='log2_Fold_Change', y='neg_log10_p_value',
        hue='Significance', palette=custom_palette, s=20, alpha=0.7, ax=ax,
        hue_order=['Upregulated', 'Downregulated', 'Not Significant']
    )
    ax.axhline(y=pval_thresh, color='k', linestyle='--', lw=1)
    ax.axvline(x=fc_thresh, color='k', linestyle='--', lw=1)
    ax.axvline(x=-fc_thresh, color='k', linestyle='--', lw=1)
    ax.set_title('Volcano Plot of Differential Gene Expression', fontsize=16)
    st.pyplot(fig)


# --- Coding Sandbox ---
st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** Can you create a volcano plot with stricter thresholds (p-value > 4, fold change > 2) and label the most significant upregulated gene?")

code_template = """
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# The data is in a DataFrame called `df_volcano`.
df_plot = df_volcano.copy()

# 1. Define stricter thresholds
pval_thresh_strict = 4.0
fc_thresh_strict = 2.0

# 2. Add the 'Significance' column based on these new thresholds
df_plot['Significance'] = 'Not Significant'
up_cond = (df_plot['log2_Fold_Change'] > fc_thresh_strict) & (df_plot['neg_log10_p_value'] > pval_thresh_strict)
down_cond = (df_plot['log2_Fold_Change'] < -fc_thresh_strict) & (df_plot['neg_log10_p_value'] > pval_thresh_strict)
df_plot.loc[up_cond, 'Significance'] = 'Upregulated'
df_plot.loc[down_cond, 'Significance'] = 'Downregulated'

# 3. Create the plot
fig, ax = plt.subplots(figsize=(9, 7))
palette = {'Upregulated':'red', 'Downregulated':'blue', 'Not Significant':'grey'}
sns.scatterplot(data=df_plot, x='log2_Fold_Change', y='neg_log10_p_value', hue='Significance', palette=palette, ax=ax)
ax.axhline(y=pval_thresh_strict, color='k', linestyle='--')
ax.axvline(x=fc_thresh_strict, color='k', linestyle='--')
ax.axvline(x=-fc_thresh_strict, color='k', linestyle='--')

# 4. Challenge: Find and label the top upregulated gene
# Hint: Sort the DataFrame to find the gene with the highest p-value among upregulated ones.
upregulated_genes = df_plot[df_plot['Significance'] == 'Upregulated']
if not upregulated_genes.empty:
    top_gene = upregulated_genes.sort_values('neg_log10_p_value', ascending=False).iloc[0]
    ax.text(top_gene.log2_Fold_Change, top_gene.neg_log10_p_value, top_gene.gene_id, fontsize=9)

st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=400)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'pd': pd, 'df_volcano': df_volcano})
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout