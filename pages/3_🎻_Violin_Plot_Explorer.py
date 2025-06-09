import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import sys

st.set_page_config(layout="wide")
st.title("🎻 Violin Plot Explorer")

if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

df = st.session_state['df_full']
gene_options = [col for col in df.columns if col.startswith('Gene_')]
subtype_options = df['Cancer_Subtype'].unique().tolist()

with st.expander("LEARN: What is a Violin Plot?"):
    st.markdown("""
    A **violin plot** is a powerful way to compare the distribution of a numerical variable across different categories. It's a hybrid of a box plot and a density plot.
    
    - **When to Use:** When you want to compare not just the median or average, but the entire shape of the data distribution (e.g., Is the data spread out? Does it have two peaks?) for a gene between 'Treated' and 'Control' groups.
    - **Key Features:**
        - **Width:** The thickness of the violin shows how many data points are at that value.
        - **`hue` Parameter:** Adds a third variable using color for subgroup analysis.
        - **`split=True`:** When using `hue` with exactly two categories, this merges them into a single violin for direct comparison.
    """)

st.header("EXPERIMENT: The Control Panel")
st.markdown("Use the widgets to explore gene expression across treatment groups and cancer subtypes.")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    gene_choice = st.selectbox("Choose a Gene (`y`):", gene_options, index=1)
    
    selected_subtypes = st.multiselect(
        "Choose Cancer Subtypes to Compare (`hue`):",
        options=subtype_options,
        default=subtype_options[:2] # Default to the first two subtypes
    )
    
    # Logic for enabling the split checkbox
    can_split = len(selected_subtypes) == 2
    split_violins = st.checkbox(
        "Split violins (`split=True`)", 
        value=True, 
        disabled=not can_split,
        help="Only works when exactly two subtypes are selected."
    )
    
    # Filter the dataframe based on selection
    df_filtered = df[df['Cancer_Subtype'].isin(selected_subtypes)]

    # Final decision on whether to split
    use_split = can_split and split_violins

with col2:
    st.subheader("Interactive Plot")
    if not selected_subtypes:
        st.warning("Please select at least one cancer subtype to display a plot.")
    else:
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.violinplot(
            x='Treatment_Group',
            y=gene_choice,
            hue='Cancer_Subtype',
            hue_order=selected_subtypes,
            data=df_filtered,
            palette='muted',
            split=use_split,
            inner='quartile',
            ax=ax
        )
        ax.set_title(f'Expression of {gene_choice}', fontsize=16)
        ax.legend(title='Subtype')
        st.pyplot(fig)

st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** How does the expression of `Gene_B` compare between 'Treated' and 'Control' groups, specifically when comparing only `Subtype_A` vs. `Subtype_C`? Create a **split violin plot** to show this direct comparison.")

code_template = f"""
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# The data is in a DataFrame called `df`.

# 1. First, filter the DataFrame to include only the subtypes we want.
subtypes_to_compare = ['Subtype_A', 'Subtype_C']
df_plot = df[df['Cancer_Subtype'].isin(subtypes_to_compare)]


# 2. Now, create the plot using the filtered data
fig, ax = plt.subplots(figsize=(10,7))
sns.violinplot(
    x='Treatment_Group', 
    y='Gene_B',          
    hue='Cancer_Subtype',# Use subtype for color
    data=df_plot,
    split=True,          # Set split to True!
    inner='quartile',
    palette='pastel',
    ax=ax
)

ax.set_title('Gene B Expression: Subtype A vs. Subtype C', fontsize=16)
st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=400)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        # We pass pd so the user can use it in their code
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'pd': pd, 'df': df})
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout