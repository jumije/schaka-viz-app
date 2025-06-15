import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sidebar_datainput import show_sidebar_data_input
from io import StringIO
import sys

# Page configuration
st.set_page_config(layout="wide")
show_sidebar_data_input() # This line adds the sidebar to this page
st.title("🔎 Scatter Plot & Correlation Explorer")

# Check if data exists in session state
if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df = st.session_state['df_full']
gene_options = [col for col in df.columns if col.startswith('Gene_')]

# --- Guided Tour Expander (UPDATED) ---
with st.expander("LEARN: What is a Scatter Plot?"):
    st.markdown("""
    A **scatter plot** is a fundamental graph for visualizing the relationship between two numerical variables. Each dot on the plot represents a single data point (in our case, a single patient).

    #### How to Read This Plot:
    1.  **Check the Axes:** Identify what variable is on the X-axis and what is on the Y-axis.
    2.  **Look for a Trend:** Do the dots seem to form a pattern?
        -   **Positive Correlation:** The pattern goes up from left to right. As X increases, Y tends to increase.
        -   **Negative Correlation:** The pattern goes down from left to right. As X increases, Y tends to decrease.
        -   **No Correlation:** The dots look like a random cloud with no clear trend.
    3.  **Examine the Regression Line:** The line drawn through the points (`sns.regplot` does this) shows the best-fit summary of the linear trend. The shaded area around it is the 95% confidence interval for this line.
    4.  **Check the 'r' value:** The Pearson correlation coefficient (r) is a number from -1 to 1 that quantifies the strength of the *linear* relationship. The closer to 1 or -1, the stronger the correlation.

    ---
    #### Dive Deeper (External Links):
    - 🔗 **[Seaborn `scatterplot` Documentation](https://seaborn.pydata.org/generated/seaborn.scatterplot.html):** The official documentation for the function we use. See all the possible parameters you can change!
    - 🔗 **[Seaborn `regplot` Documentation](https://seaborn.pydata.org/generated/seaborn.regplot.html):** The official documentation for the function we use. See all the possible parameters you can change!
    - 🔗 **[A simple explanation of Pearson Correlation](https://www.scribbr.com/statistics/pearson-correlation-coefficient/):** A great article explaining what the 'r' value means.
    """)

# --- Control Panel and Plot ---
st.header("EXPERIMENT: The Control Panel")
st.markdown("Choose different genes to see how their relationships change. The 'Gene Correlation' in the Data Lab was set between `Gene_D` and `Gene_E`.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    x_gene = st.selectbox("X-axis Gene:", gene_options, index=3) # Default Gene_D
    y_gene = st.selectbox("Y-axis Gene:", gene_options, index=4) # Default Gene_E
    
    # *** THE FIX IS HERE: Add 'Cancer_Subtype' to the hue options ***
    hue_choice = st.selectbox("Color points by (`hue`):", (None, 'Treatment_Group', 'Cancer_Subtype'), index=0)

    # Calculate correlation for info box
    try:
        r_val, p_val = stats.pearsonr(df[x_gene], df[y_gene])
        st.info(f"The overall Pearson correlation coefficient (r) between these two genes is **{r_val:.3f}**.")
    except ValueError:
        st.warning("Could not calculate correlation.")
        
with col2:
    st.subheader("Interactive Plot")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Use different plot functions based on whether hue is selected
    if hue_choice:
        sns.scatterplot(data=df, x=x_gene, y=y_gene, hue=hue_choice, ax=ax, alpha=0.8)
    else:
        sns.regplot(data=df, x=x_gene, y=y_gene, ax=ax, line_kws={"color":"red"})

    ax.set_title(f"Relationship between {x_gene} and {y_gene}", fontsize=16)
    st.pyplot(fig)


# --- Coding Sandbox ---
st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** Create a regression plot for `Gene_D` vs. `Gene_E`, but color the individual points by `Cancer_Subtype`. Does the correlation seem to exist within each subtype?")

code_template = f"""
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# The data is in a DataFrame called `df`.
fig, ax = plt.subplots(figsize=(8, 6))

x_axis_gene = 'Gene_D'
y_axis_gene = 'Gene_E'

# 1. Use sns.scatterplot to color by 'Cancer_Subtype'
sns.scatterplot(
    data=df,
    x=x_axis_gene,
    y=y_axis_gene,
    hue='Cancer_Subtype',
    palette='bright', # Try different palettes!
    ax=ax
)

# 2. You can also add an overall regression line on top!
sns.regplot(
    data=df,
    x=x_axis_gene,
    y=y_axis_gene,
    scatter=False, # Set scatter=False so it doesn't plot the points again
    color='black',
    ax=ax
)

# 3. Add a title
ax.set_title(f"Correlation colored by Subtype", fontsize=16)

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