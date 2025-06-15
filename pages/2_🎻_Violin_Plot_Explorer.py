import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sidebar_datainput import show_sidebar_data_input
from io import StringIO
import sys

st.set_page_config(layout="wide")
show_sidebar_data_input() # This line adds the sidebar to this page
st.title("2. Violin Plot")

if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset on the main page first!")
    st.stop()

df = st.session_state['df_full']
gene_options = [col for col in df.columns if col.startswith('Gene_')]
subtype_options = df['Cancer_Subtype'].unique().tolist()

# --- Guided Tour Expander (UPDATED) ---
with st.expander("LEARN: What is a Violin Plot?"):
    st.markdown("""
    A **violin plot** compares a numerical distribution across different categories. It is a hybrid of a box plot and a density plot, showing more about the data's shape and distribution.

    #### How to Read This Plot:
    1.  **The Shape (Violin):** The width of the violin represents the density of data points at that value. A fatter section means more data points are concentrated there. This helps you see if the data is skewed or has multiple peaks (is "bimodal").
    2.  **The Inner Plot:** The small plot inside the violin provides summary statistics.
        -   `'box'`: Shows a miniature box-and-whisker plot with the median and interquartile range (IQR).
        -   `'quartile'`: Shows the three quartiles (25th, 50th, 75th percentiles).
        -   `'point'` or `'stick'`: Show every single data point.
    3.  **Comparing Violins:** You compare the plots for different categories (e.g., 'Treated' vs. 'Control'). Look for differences in their median, their overall shape, and where they are located on the Y-axis.

    ---
    #### Dive Deeper (External Links):
    - 🔗 **[Seaborn `violinplot` Documentation](https://seaborn.pydata.org/generated/seaborn.violinplot.html):** The official documentation. Explore parameters like `hue`, `split`, and `inner`.
    - 🔗 **[The Python Graph Gallery - Violin Plot](https://www.python-graph-gallery.com/violin-plot/):** Many excellent and easy-to-understand examples.
    """)

st.header("EXPERIMENT: The Control Panel")
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Parameters")
    gene_choice = st.selectbox("Choose a Gene (`y`):", gene_options, index=1)
    inner_style = st.selectbox("Inner plot style (`inner`):", ('box', 'quartile', 'point', 'stick'), index=0)
    selected_subtypes = st.multiselect("Choose Subtypes to Compare (`hue`):", options=subtype_options, default=subtype_options[:2])
    can_split = len(selected_subtypes) == 2
    split_violins = st.checkbox("Split violins (`split=True`)", value=True, disabled=not can_split, help="Only works when exactly two subtypes are selected.")
    
df_filtered = df[df['Cancer_Subtype'].isin(selected_subtypes)]
use_split = can_split and split_violins

with col2:
    st.subheader("Interactive Plot")
    if not selected_subtypes:
        st.warning("Please select at least one cancer subtype.")
    else:
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.violinplot(
            x='Treatment_Group', y=gene_choice, hue='Cancer_Subtype',
            hue_order=selected_subtypes, data=df_filtered, palette='muted',
            split=use_split, inner=inner_style, ax=ax
        )
        ax.set_title(f'Expression of {gene_choice}', fontsize=16)
        st.pyplot(fig)

st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** How does `Gene_B` expression compare between `Subtype_A` vs `Subtype_C`? Create a split violin plot with a box plot inside.")

code = st.text_area("Edit your code here:", value="""import seaborn as sns
import matplotlib.pyplot as plt

subtypes = ['Subtype_A', 'Subtype_C']
df_plot = df[df['Cancer_Subtype'].isin(subtypes)]

fig, ax = plt.subplots(figsize=(10,7))
sns.violinplot(
    x='Treatment_Group', y='Gene_B', hue='Cancer_Subtype',
    data=df_plot, split=True, inner='box', palette='pastel', ax=ax
)
st.pyplot(fig)
""", height=300)

if st.button("Run Code"):
    st.subheader("Your Output")
    old_stdout, sys.stdout = sys.stdout, StringIO()
    try:
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'pd': pd, 'df': df})
        st.code(sys.stdout.getvalue(), language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout