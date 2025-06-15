import streamlit as st
import pandas as pd
import numpy as np

# --- App Configuration ---
st.set_page_config(
    page_title="Schaka Bioinformatics Learning Lab",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Generation Function ---
@st.cache_data
def generate_data(treatment_effect, survival_benefit, correlation_strength, num_hits, random_seed):
    """Generates all the simulated data for the app."""
    np.random.seed(random_seed)
    num_samples = 100
    genes = [f'Gene_{chr(65+i)}' for i in range(10)]
    df_meta = pd.DataFrame({
        'Sample_ID': [f'Sample_{i+1}' for i in range(num_samples)],
        'Treatment_Group': np.random.choice(['Control', 'Treated'], num_samples, p=[0.5, 0.5]),
        'Cancer_Subtype': np.random.choice(['Subtype_A', 'Subtype_B', 'Subtype_C'], num_samples, p=[0.4, 0.35, 0.25])
    })
    expression_data = np.log2(np.random.uniform(10, 100, size=(num_samples, len(genes))))
    df_expr = pd.DataFrame(expression_data, columns=genes)
    df_full = pd.concat([df_meta, df_expr], axis=1)
    treated_indices = df_full['Treatment_Group'] == 'Treated'
    df_full.loc[treated_indices, 'Gene_B'] += np.random.normal(treatment_effect, 0.5, size=treated_indices.sum())
    df_full.loc[treated_indices, 'Gene_C'] += np.random.normal(treatment_effect * 1.2, 0.5, size=treated_indices.sum())
    df_full.loc[treated_indices, 'Gene_H'] -= np.random.normal(treatment_effect * 0.8, 0.5, size=treated_indices.sum())
    df_full['Gene_E'] = df_full['Gene_D'] * correlation_strength + np.random.normal(0, 2 * (1 - correlation_strength), num_samples)
    base_survival = np.random.exponential(365, num_samples)
    treatment_benefit_days = (df_full['Treatment_Group'] == 'Treated') * np.random.exponential(365 * survival_benefit, num_samples)
    df_full['Survival_Time_days'] = (base_survival + treatment_benefit_days).astype(int)
    study_cutoff = 365 * 4
    df_full['Event_Status'] = 1
    df_full.loc[df_full['Survival_Time_days'] > study_cutoff, 'Event_Status'] = 0
    df_full.loc[df_full['Survival_Time_days'] > study_cutoff, 'Survival_Time_days'] = study_cutoff
    num_genes_total = 1000
    genes_de = [f'Gene_{i}' for i in range(num_genes_total)]
    log2fc = np.random.normal(0, 0.5, num_genes_total)
    if num_hits > 0:
        significant_indices = np.random.choice(num_genes_total, num_hits, replace=False)
        log2fc[significant_indices] = np.random.normal(0, 2.5, num_hits)
    p_values = -np.log10(np.random.uniform(0.05, 1, num_genes_total))
    if num_hits > 0:
        p_values[significant_indices] = -np.log10(np.random.uniform(1e-12, 1e-4, num_hits))
    df_volcano = pd.DataFrame({'gene_id': genes_de, 'log2_Fold_Change': log2fc, 'neg_log10_p_value': p_values})
    return df_full, df_volcano

# --- Sidebar "Data Lab" Controls ---
with st.sidebar:
    st.title("🔬 The Data Lab")
    st.markdown("Generate and control the dataset used across all visualization pages.")
    
    scenario = st.radio(
        "Choose a data scenario:",
        ("Textbook Case (Clear Effects)", "Subtle Effects (More Realistic)", "Failed Drug Trial (No Survival Benefit)", "Custom"),
        key='scenario_choice'
    )

    if scenario == "Custom":
        st.subheader("Custom Parameters")
        param_treatment_effect = st.slider("Treatment Effect", 0.0, 5.0, 2.5, 0.1)
        param_survival_benefit = st.slider("Survival Benefit", 0.0, 5.0, 1.5, 0.1)
        param_correlation_strength = st.slider("Gene Correlation", 0.0, 1.0, 0.8, 0.05)
        param_num_hits = st.slider("Significant Genes", 0, 200, 100, 10)
        param_random_seed = st.number_input("Random Seed", value=42)
    else:
        # Pre-defined scenarios
        if scenario == "Textbook Case (Clear Effects)":
            param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 2.5, 1.5, 0.8, 100, 42
        elif scenario == "Subtle Effects (More Realistic)":
            param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 0.8, 0.5, 0.4, 20, 42
        else: # Failed Drug Trial
            param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 2.5, 0.0, 0.8, 100, 42
            
    if st.button("🔬 Generate Dataset", type="primary"):
        df_full, df_volcano = generate_data(param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed)
        st.session_state['df_full'] = df_full
        st.session_state['df_volcano'] = df_volcano
        st.success("✅ Datasets Generated!")

# --- Main Page Welcome Content ---
st.title("Welcome to the Bioinformatics Learning Lab!")
st.markdown("### A hands-on environment for your journey into cancer data analysis.")
st.markdown("""
This interactive app is your companion for the "Genomische Geheimnisse" course. Here, you will not just see visualizations—you will build, modify, and experiment with them yourself.

#### How to Use This Lab:

1.  **Use the `Data Lab` in the sidebar to create a dataset.** Choose a scenario and click the **`Generate Dataset`** button.
2.  **Navigate to a visualization page** using the links that appear in the sidebar after you generate data.
3.  On each page, you can:
    *   **Learn** about the plot in the expander.
    *   **Experiment** with parameters in the Control Panel.
    *   **Discover** new insights by modifying code in the Sandbox.

Let's begin!
""")

if 'df_full' in st.session_state:
    st.info("Dataset is ready. Choose a visualization from the sidebar to continue.")
else:
    st.warning("👈 **Please generate a dataset in the sidebar to get started!**")