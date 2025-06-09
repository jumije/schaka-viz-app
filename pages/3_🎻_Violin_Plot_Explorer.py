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

with st.expander("LEARN: What is a Violin Plot?"):
    st.markdown("""
    A **violin plot** is a powerful way to compare the distribution of a numerical variable across different categories. It's a hybrid of a box plot and a density plot.
    
    - **When to Use:** When you want to compare not just the median or average, but the entire shape of the data distribution (e.g., Is the data spread out? Does it have two peaks?) for a gene between 'Treated' and 'Control' groups.
    - **Key Features:**
        - **Width:** The thickness of the violin shows how many data points are at that value.
        - **Inner Plot:** The small plot inside can be a box plot, quartile lines, or stick lines showing individual points.
    - **Pitfalls:** Can be less intuitive to a lay audience than a simple bar chart. Make sure your labels are clear!
    """)

st.header("EXPERIMENT: The Control Panel")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    gene_choice = st.selectbox("Choose a Gene (`y`):", gene_options, index=1)
    inner_style = st.selectbox("Inner plot style (`inner`):", ('box', 'quartile', 'stick', 'point'), index=0)
    split_violins = st.checkbox("Split violins (if applicable)", value=False, help="Requires a 'hue' variable. We will add this later.")
    
    st.info(f"The `Data Lab` was designed to affect `Gene_B`, `Gene_C`, and `Gene_H`. Select one of these to see a clear difference between the groups.")

with col2:
    st.subheader("Interactive Plot")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.violinplot(
        x='Treatment_Group',
        y=gene_choice,
        data=df,
        palette='Set2',
        inner=inner_style,
        ax=ax
    )
    ax.set_title(f'Expression of {gene_choice} by Treatment Group', fontsize=16)
    st.pyplot(fig)

st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** For `Gene_C`, create a violin plot that shows quartile lines inside and add a swarm plot on top to see every individual data point.")

code_template = f"""
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# The data is in a DataFrame called `df`.
fig, ax = plt.subplots(figsize=(8,6))

# Create the main violin plot
# Try changing y='{gene_choice}' or inner='quartile'
sns.violinplot(
    x='Treatment_Group',
    y='Gene_C',
    data=df,
    palette='Set2',
    inner='quartile', # Show quartile lines
    ax=ax
)

# Now, add a swarm plot on the same axes (ax)
sns.swarmplot(
    x='Treatment_Group',
    y='Gene_C',
    data=df,
    color='black', # Make points a different color
    size=4,        # Make points a bit bigger
    ax=ax
)

ax.set_title('My Custom Violin Plot', fontsize=16)
st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=400)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'df': df})
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout