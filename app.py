# ==============================================================================
#                      Bioinformatics Visualization Explorer App
# ==============================================================================
# INSTRUCTIONS:
# 1. Save this script as `app.py`.
# 2. In your terminal, run `pip install streamlit pandas numpy seaborn matplotlib lifelines scipy`.
# 3. In the same directory as this file, run `streamlit run app.py`.
# 4. The app will open in your web browser.
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from scipy import stats

# --- App Configuration ---
st.set_page_config(
    page_title="Bioinformatics Visualization Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data Generation Function ---
# This function creates our simulated datasets. We use @st.cache_data to make it fast!
# Streamlit will only re-run this function if the input parameters change.
@st.cache_data
def generate_data(treatment_effect, survival_benefit, correlation_strength, num_hits, random_seed):
    """Generates simulated gene expression, clinical, and differential expression data."""
    np.random.seed(random_seed)

    # --- Dataset 1: Gene Expression & Clinical Data ---
    num_samples = 100
    genes = [f'Gene_{chr(65+i)}' for i in range(10)]

    df_meta = pd.DataFrame({
        'Sample_ID': [f'Sample_{i+1}' for i in range(num_samples)],
        'Treatment_Group': np.random.choice(['Control', 'Treated'], num_samples, p=[0.5, 0.5])
    })

    expression_data = np.log2(np.random.uniform(10, 100, size=(num_samples, len(genes))))
    df_expr = pd.DataFrame(expression_data, columns=genes)
    df_full = pd.concat([df_meta, df_expr], axis=1)

    # Introduce treatment effects based on the user's slider
    treated_indices = df_full['Treatment_Group'] == 'Treated'
    df_full.loc[treated_indices, 'Gene_B'] += np.random.normal(treatment_effect, 0.5, size=treated_indices.sum())
    df_full.loc[treated_indices, 'Gene_C'] += np.random.normal(treatment_effect * 1.2, 0.5, size=treated_indices.sum())
    df_full.loc[treated_indices, 'Gene_H'] -= np.random.normal(treatment_effect * 0.8, 0.5, size=treated_indices.sum())

    # Create a correlation between Gene_D and Gene_E
    df_full['Gene_E'] = df_full['Gene_D'] * correlation_strength + np.random.normal(0, 2 * (1-correlation_strength), num_samples)

    # Add Survival Data
    base_survival = np.random.exponential(365, num_samples)
    treatment_benefit_days = (df_full['Treatment_Group'] == 'Treated') * np.random.exponential(365 * survival_benefit, num_samples)
    df_full['Survival_Time_days'] = (base_survival + treatment_benefit_days).astype(int)

    study_cutoff = 365 * 4
    df_full['Event_Status'] = 1
    df_full.loc[df_full['Survival_Time_days'] > study_cutoff, 'Event_Status'] = 0
    df_full.loc[df_full['Survival_Time_days'] > study_cutoff, 'Survival_Time_days'] = study_cutoff

    # --- Dataset 2: Differential Expression Results ---
    num_genes_total = 1000
    genes_de = [f'Gene_{i}' for i in range(num_genes_total)]
    log2fc = np.random.normal(0, 0.5, num_genes_total)
    
    if num_hits > 0:
      significant_indices = np.random.choice(num_genes_total, num_hits, replace=False)
      log2fc[significant_indices] = np.random.normal(0, 2.5, num_hits)

    p_values = -np.log10(np.random.uniform(0.05, 1, num_genes_total))
    
    if num_hits > 0:
      p_values[significant_indices] = -np.log10(np.random.uniform(1e-12, 1e-4, num_hits))

    df_volcano = pd.DataFrame({
        'gene_id': genes_de,
        'log2_Fold_Change': log2fc,
        'neg_log10_p_value': p_values
    })

    return df_full, df_volcano

# --- App Sidebar ---
with st.sidebar:
    st.title("🧬 Bioinformatics Visualization Explorer")
    st.markdown("A tool to interactively learn about common plots in cancer research.")

    st.header("1. The Data Lab")
    st.markdown("First, create a dataset to explore. Choose a pre-defined scenario or create your own!")

    scenario = st.radio(
        "Choose a data scenario:",
        ("Textbook Case (Clear Effects)", "Subtle Effects (More Realistic)", "Failed Drug Trial (No Survival Benefit)", "Custom"),
        index=0,
        help="Each scenario generates a new dataset with different properties."
    )

    if scenario == "Custom":
        st.subheader("Custom Parameters")
        param_treatment_effect = st.slider("Treatment Effect Size", 0.0, 5.0, 2.5, 0.1)
        param_survival_benefit = st.slider("Survival Benefit Multiplier", 0.0, 5.0, 1.5, 0.1)
        param_correlation_strength = st.slider("Gene Correlation Strength (r)", 0.0, 1.0, 0.8, 0.05)
        param_num_hits = st.slider("Number of Significant Genes (Volcano)", 0, 200, 100, 10)
        param_random_seed = st.number_input("Random Seed", value=42)
    else:
        if scenario == "Textbook Case (Clear Effects)":
            param_treatment_effect = 2.5
            param_survival_benefit = 1.5
            param_correlation_strength = 0.8
            param_num_hits = 100
            param_random_seed = 42
        elif scenario == "Subtle Effects (More Realistic)":
            param_treatment_effect = 0.8
            param_survival_benefit = 0.5
            param_correlation_strength = 0.4
            param_num_hits = 20
            param_random_seed = 42
        elif scenario == "Failed Drug Trial (No Survival Benefit)":
            param_treatment_effect = 2.5
            param_survival_benefit = 0.0 # The key change
            param_correlation_strength = 0.8
            param_num_hits = 100
            param_random_seed = 42

    if st.button("🔬 Generate Dataset"):
        st.session_state.df_full, st.session_state.df_volcano = generate_data(
            param_treatment_effect,
            param_survival_benefit,
            param_correlation_strength,
            param_num_hits,
            param_random_seed
        )
        st.success("Dataset generated successfully!")

    if "df_full" in st.session_state:
        st.markdown("---")
        st.header("2. Choose a Plot")
        app_page = st.radio(
            "Select a visualization to explore:",
            ("Welcome", "Heatmap", "Violin Plot", "Volcano Plot", "Survival Plot", "Scatter Plot"),
            index=0,
            key="plot_choice"
        )
    else:
        st.info("Please generate a dataset to begin exploring the plots.")
        app_page = "Welcome"

# --- Page Rendering Logic ---

# Check if data exists before attempting to show plot pages
data_exists = "df_full" in st.session_state

if app_page == "Welcome":
    st.title("Welcome to the Bioinformatics Visualization Explorer!")
    st.markdown("### A tool for your journey into cancer data analysis.")
    st.markdown("""
        This interactive app is designed to accompany the "Genomische Geheimnisse" course. Here, you can put the principles of data storytelling and visualization into practice.

        **How to use this app:**
        1.  **Start in the `Data Lab` on the sidebar.** Choose a scenario and click the **`Generate Dataset`** button. This creates the simulated data you'll be plotting.
        2.  **Select a plot type** from the sidebar menu that appears.
        3.  **Interact with the widgets** on each page to change plot parameters.
        4.  **Observe how the plot changes** in response to your choices.
        5.  **Examine the Python code** to see exactly how your plot was created.

        This is your sandbox. Experiment, explore, and see how changing data and code can tell different stories!
    """)
    if not data_exists:
      st.warning("👈 **Don't forget to generate a dataset in the sidebar to start!**")


# --- Heatmap Page ---
elif app_page == "Heatmap" and data_exists:
    st.header("Heatmap Explorer")
    st.markdown("A heatmap is perfect for visualizing large amounts of data (like gene expression across many samples) to find patterns and clusters.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        cmap_choice = st.selectbox(
            "Choose a Colormap (cmap):",
            ('vlag', 'coolwarm', 'viridis', 'plasma', 'magma'),
            index=0,
            help="Colormaps change the look and feel. 'vlag' and 'coolwarm' are great for showing up/down regulation around a central point."
        )
        st.info("Notice how `clustermap` automatically groups similar genes and similar samples together to reveal the underlying patterns in the data.")

    with col2:
        st.subheader("Interactive Plot")
        df_full = st.session_state.df_full
        
        # Prepare data for heatmap
        gene_columns = [col for col in df_full.columns if col.startswith('Gene_')]
        gene_data = df_full[gene_columns].T # Transpose so genes are rows

        g = sns.clustermap(gene_data, cmap=cmap_choice, z_score=0, figsize=(12, 10))
        st.pyplot(g)

    st.subheader("The Code Behind the Plot")
    st.code(f"""
import seaborn as sns
import matplotlib.pyplot as plt

# Prepare the data (we want genes as rows, samples as columns)
gene_columns = [col for col in df.columns if col.startswith('Gene_')]
gene_data = df[gene_columns].T

# Create the clustermap
# z_score=0 scales the data for each gene, which is crucial for good visualization.
g = sns.clustermap(
    gene_data, 
    cmap='{cmap_choice}',  # Your chosen colormap!
    z_score=0,
    figsize=(12, 10)
)
st.pyplot(g)
""", language='python')

# --- Violin Plot Page ---
elif app_page == "Violin Plot" and data_exists:
    st.header("Violin Plot Explorer")
    st.markdown("A violin plot shows the distribution of a variable (like a gene's expression) across different categories. It's like a box plot but with more detail.")

    df_full = st.session_state.df_full
    gene_options = [col for col in df_full.columns if col.startswith('Gene_')]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        gene_choice = st.selectbox("Choose a Gene to Plot:", gene_options, index=1)
        show_points = st.checkbox("Show individual data points (swarmplot)", value=True)
        st.info(f"We expect **{gene_choice}** to be different between groups if the treatment effect in the Data Lab was high. Try picking `Gene_B` or `Gene_H` vs `Gene_A`.")
        
    with col2:
        st.subheader("Interactive Plot")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.violinplot(x='Treatment_Group', y=gene_choice, data=df_full, palette='Set2', ax=ax)
        if show_points:
            sns.swarmplot(x='Treatment_Group', y=gene_choice, data=df_full, color=".25", size=3, ax=ax)
        
        ax.set_title(f'Expression of {gene_choice} by Treatment Group', fontsize=16)
        ax.set_xlabel('Treatment Group', fontsize=12)
        ax.set_ylabel('Gene Expression (log2 scale)', fontsize=12)
        st.pyplot(fig)

    st.subheader("The Code Behind the Plot")
    st.code(f"""
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8,6))

# Create the main violin plot
sns.violinplot(x='Treatment_Group', y='{gene_choice}', data=df, palette='Set2', ax=ax)

# Overlay the individual points if the checkbox is ticked
{
"sns.swarmplot(x='Treatment_Group', y='" + gene_choice + "', data=df, color='.25', size=3, ax=ax)" 
if show_points else "# Swarmplot is disabled."
}

ax.set_title('Expression of {gene_choice} by Treatment Group', fontsize=16)
st.pyplot(fig)
""", language='python')

# --- Volcano Plot Page ---
elif app_page == "Volcano Plot" and data_exists:
    st.header("Volcano Plot Explorer")
    st.markdown("A volcano plot visualizes thousands of statistical tests at once. It's used to find genes that are both statistically significant (high on Y-axis) and have a large change in expression (far left or right on X-axis).")

    df_volcano = st.session_state.df_volcano

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parameters")
        pval_thresh = st.slider("-log10(p-value) Threshold", 0.0, 10.0, 2.0, 0.1, help="Higher values are more strict.")
        fc_thresh = st.slider("log2(Fold Change) Threshold", 0.0, 5.0, 1.0, 0.1, help="The magnitude of expression change.")
        
        # Prepare data with new significance column based on sliders
        df_volcano['Significance'] = 'Not Significant'
        up_cond = (df_volcano['log2_Fold_Change'] > fc_thresh) & (df_volcano['neg_log10_p_value'] > pval_thresh)
        down_cond = (df_volcano['log2_Fold_Change'] < -fc_thresh) & (df_volcano['neg_log10_p_value'] > pval_thresh)
        df_volcano.loc[up_cond, 'Significance'] = 'Upregulated'
        df_volcano.loc[down_cond, 'Significance'] = 'Downregulated'

        st.info("Move the sliders to see how changing the significance cutoffs alters which genes are considered 'hits'. This is a key step in real analysis!")

    with col2:
        st.subheader("Interactive Plot")
        fig, ax = plt.subplots(figsize=(9, 7))
        custom_palette = {'Upregulated':'red', 'Downregulated':'blue', 'Not Significant':'grey'}
        sns.scatterplot(
            data=df_volcano,
            x='log2_Fold_Change',
            y='neg_log10_p_value',
            hue='Significance',
            palette=custom_palette,
            s=15,
            alpha=0.7,
            ax=ax
        )
        ax.axhline(y=pval_thresh, color='k', linestyle='--')
        ax.axvline(x=fc_thresh, color='k', linestyle='--')
        ax.axvline(x=-fc_thresh, color='k', linestyle='--')
        ax.set_title('Volcano Plot of Differential Gene Expression', fontsize=16)
        st.pyplot(fig)

    st.subheader("The Code Behind the Plot")
    st.code(f"""
import seaborn as sns
import matplotlib.pyplot as plt

# Define thresholds based on your slider values
pval_threshold = {pval_thresh}
fc_threshold = {fc_thresh}

# Create a new column to classify genes based on the thresholds
df['Significance'] = 'Not Significant'
up_cond = (df['log2_Fold_Change'] > fc_threshold) & (df['neg_log10_p_value'] > pval_threshold)
down_cond = (df['log2_Fold_Change'] < -fc_threshold) & (df['neg_log10_p_value'] > pval_threshold)
df.loc[up_cond, 'Significance'] = 'Upregulated'
df.loc[down_cond, 'Significance'] = 'Downregulated'
        
# Plotting
fig, ax = plt.subplots(figsize=(9, 7))
palette = {{'Upregulated':'red', 'Downregulated':'blue', 'Not Significant':'grey'}}
sns.scatterplot(data=df, x='log2_Fold_Change', y='neg_log10_p_value', hue='Significance', palette=palette, s=15, ax=ax)
ax.axhline(y=pval_threshold, color='k', linestyle='--')
ax.axvline(x=fc_threshold, color='k', linestyle='--')
ax.axvline(x=-fc_threshold, color='k', linestyle='--')
st.pyplot(fig)
""", language='python')


# --- Survival Plot Page ---
elif app_page == "Survival Plot" and data_exists:
    st.header("Kaplan-Meier Survival Plot Explorer")
    st.markdown("This plot is essential in clinical research. It shows the probability of survival over time and allows us to compare outcomes between different patient groups.")
    
    df_full = st.session_state.df_full

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parameters")
        ci_show = st.checkbox("Show 95% Confidence Interval", value=True)
        st.info("The gap between the two curves tells the story. A larger, more consistent gap suggests the treatment has a significant effect on survival. Does the gap change when you adjust the 'Survival Benefit' in the Data Lab?")

    with col2:
        st.subheader("Interactive Plot")
        fig, ax = plt.subplots(figsize=(8, 6))
        kmf = KaplanMeierFitter()
        
        for group in df_full['Treatment_Group'].unique():
            mask = df_full['Treatment_Group'] == group
            kmf.fit(df_full[mask]['Survival_Time_days'], df_full[mask]['Event_Status'], label=group)
            kmf.plot_survival_function(ax=ax, ci_show=ci_show)
        
        ax.set_title('Kaplan-Meier Survival Curves by Treatment Group', fontsize=16)
        ax.set_xlabel('Time (Days)', fontsize=12)
        ax.set_ylabel('Survival Probability', fontsize=12)
        ax.legend(title='Group')
        st.pyplot(fig)

    st.subheader("The Code Behind the Plot")
    st.code(f"""
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
kmf = KaplanMeierFitter()

# Loop through each group to plot them separately
for group in df['Treatment_Group'].unique():
    mask = df['Treatment_Group'] == group
    kmf.fit(
        df[mask]['Survival_Time_days'], 
        df[mask]['Event_Status'], 
        label=group
    )
    # The ci_show parameter is controlled by your checkbox!
    kmf.plot_survival_function(ax=ax, ci_show={ci_show})

st.pyplot(fig)
""", language='python')

# --- Scatter Plot Page ---
elif app_page == "Scatter Plot" and data_exists:
    st.header("Scatter Plot & Correlation Explorer")
    st.markdown("Scatter plots are fundamental for checking the relationship between two numerical variables. Here we can see if two genes are 'co-expressed' (i.e., when one goes up, the other also goes up).")

    df_full = st.session_state.df_full
    gene_options = [col for col in df_full.columns if col.startswith('Gene_')]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parameters")
        x_gene = st.selectbox("Choose a gene for the X-axis:", gene_options, index=3) # Default to Gene_D
        y_gene = st.selectbox("Choose a gene for the Y-axis:", gene_options, index=4) # Default to Gene_E
        
        st.info(f"The `Gene_D` and `Gene_E` relationship was designed in the Data Lab. Try plotting them against each other! Then try plotting `Gene_A` vs `Gene_G` to see what a random relationship looks like.")

    with col2:
        st.subheader("Interactive Plot")
        
        # Calculate correlation
        try:
            r, p_val = stats.pearsonr(df_full[x_gene], df_full[y_gene])
            title = f"Correlation between {x_gene} and {y_gene}\n(Pearson r = {r:.3f})"
        except ValueError:
            r = "N/A"
            title = f"Correlation between {x_gene} and {y_gene}"


        fig, ax = plt.subplots(figsize=(8, 7))
        sns.regplot(
            data=df_full, 
            x=x_gene, 
            y=y_gene, 
            ax=ax, 
            line_kws={"color":"red"}
        )
        ax.set_title(title, fontsize=16)
        st.pyplot(fig)

    st.subheader("The Code Behind the Plot")
    st.code(f"""
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Calculate the correlation to display in the title
r_val, p_val = stats.pearsonr(df['{x_gene}'], df['{y_gene}'])

fig, ax = plt.subplots(figsize=(8, 7))

# regplot is great because it creates a scatter plot and adds a regression line
sns.regplot(data=df, x='{x_gene}', y='{y_gene}', ax=ax, line_kws={{"color":"red"}})

ax.set_title(f"Correlation between {x_gene} and {y_gene}\\n(Pearson r = {{r_val:.3f}})")
st.pyplot(fig)
""", language='python')


# --- Fallback for when data is not loaded ---
else:
    if app_page != "Welcome":
      st.error("Please generate a dataset in the 'Data Lab' on the sidebar before visiting this page.")