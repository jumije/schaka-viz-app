import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from io import StringIO
import sys

# Page configuration
st.set_page_config(layout="wide")
st.title("🔎 Scatter Plot & Correlation Explorer")

# Check if data exists in session state
if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df = st.session_state['df_full']
gene_options = [col for col in df.columns if col.startswith('Gene_')]

# --- Guided Tour Expander ---
with st.expander("LEARN: What is a Scatter Plot?"):
    st.markdown("""
    A **scatter plot** is a fundamental graph for visualizing the relationship between two numerical variables. Each dot on the plot represents a single data point (in our case, a single patient).

    - **When to Use:** To see if two variables are correlated. For example, "When the expression of Gene X goes up, does the expression of Gene Y also go up?"
    - **Key Features:**
        - **Correlation:** The pattern of the dots tells you about the relationship. An upward trend from left-to-right is a *positive correlation*. A downward trend is a *negative correlation*. No clear pattern means no correlation.
        - **Regression Line:** We often add a line of best fit (`regplot` in Seaborn does this automatically) to summarize the trend.
        - **Correlation Coefficient (r):** This is a value between -1 and 1 that quantifies the strength of the linear relationship. A value near 1 or -1 is a strong correlation, while a value near 0 is a weak one.
    """)

# --- Control Panel and Plot ---
st.header("EXPERIMENT: The Control Panel")
st.markdown("Choose different genes to see how their relationships change. The 'Gene Correlation' in the Data Lab was set between `Gene_D` and `Gene_E`.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    x_gene = st.selectbox("X-axis Gene:", gene_options, index=3) # Default Gene_D
    y_gene = st.selectbox("Y-axis Gene:", gene_options, index=4) # Default Gene_E
    hue_choice = st.selectbox("Color points by (`hue`):", (None, 'Treatment_Group'), index=0)

    # Calculate correlation for info box
    try:
        r_val, p_val = stats.pearsonr(df[x_gene], df[y_gene])
        st.info(f"The Pearson correlation coefficient (r) between these two genes is **{r_val:.3f}**.")
    except ValueError:
        st.warning("Could not calculate correlation.")
        
with col2:
    st.subheader("Interactive Plot")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df, 
        x=x_gene, 
        y=y_gene,
        hue=hue_choice,
        ax=ax
    )
    ax.set_title(f"Relationship between {x_gene} and {y_gene}", fontsize=16)
    st.pyplot(fig)


# --- Coding Sandbox ---
st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** Confirm that `Gene_D` and `Gene_E` are positively correlated. Create a regression plot (not just a scatter plot) and add a title that automatically displays the calculated Pearson 'r' value.")

code_template = f"""
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# The data is in a DataFrame called `df`.
fig, ax = plt.subplots(figsize=(8, 6))

x_axis_gene = 'Gene_D'
y_axis_gene = 'Gene_E'

# 1. Use sns.regplot() to show a regression line
sns.regplot(
    data=df,
    x=x_axis_gene,
    y=y_axis_gene,
    line_kws={{"color": "red"}}, # Make the line red
    ax=ax
)

# 2. Calculate the correlation coefficient
r_val, _ = stats.pearsonr(df[x_axis_gene], df[y_axis_gene])

# 3. Create a dynamic title using an f-string
title = f"Correlation of {{x_axis_gene}} and {{y_axis_gene}}\\nPearson r = {{r_val:.3f}}"
ax.set_title(title, fontsize=16)

st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=400)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        exec(code, {'st': st, 'sns': sns, 'plt': plt, 'stats': stats, 'df': df})
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout