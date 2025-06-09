import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("🧪 The Data Lab")
st.markdown("All great analysis starts with data. Here, you can generate your own simulated dataset to explore in the other modules. The data you generate here will be available across all pages of the app.")

# --- Data Generation Function (same as before) ---
@st.cache_data
def generate_data(treatment_effect, survival_benefit, correlation_strength, num_hits, random_seed):
    """Generates simulated gene expression, clinical, and differential expression data."""
    np.random.seed(random_seed)

    # --- Dataset 1: Gene Expression & Clinical Data ---
    num_samples = 100
    genes = [f'Gene_{chr(65+i)}' for i in range(10)]
    df_meta = pd.DataFrame({'Sample_ID': [f'Sample_{i+1}' for i in range(num_samples)], 'Treatment_Group': np.random.choice(['Control', 'Treated'], num_samples, p=[0.5, 0.5])})
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
    df_volcano = pd.DataFrame({'gene_id': genes_de, 'log2_Fold_Change': log2fc, 'neg_log10_p_value': p_values})

    return df_full, df_volcano

st.subheader("Step 1: Choose a Data Scenario")
scenario = st.radio(
    "Select a pre-defined scenario or create your own:",
    ("Textbook Case (Clear Effects)", "Subtle Effects (More Realistic)", "Failed Drug Trial (No Survival Benefit)", "Custom"),
    key='scenario_choice'
)

if scenario == "Custom":
    st.subheader("Step 2: Set Custom Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        param_treatment_effect = st.slider("Treatment Effect Size", 0.0, 5.0, 2.5, 0.1)
        param_survival_benefit = st.slider("Survival Benefit Multiplier", 0.0, 5.0, 1.5, 0.1)
    with col2:
        param_correlation_strength = st.slider("Gene Correlation Strength (r)", 0.0, 1.0, 0.8, 0.05)
        param_num_hits = st.slider("Number of Significant Genes", 0, 200, 100, 10)
    with col3:
        param_random_seed = st.number_input("Random Seed", value=42, help="Change this number to get a different random dataset with the same parameters.")

else:
    st.subheader("Step 2: Review Scenario Parameters")
    if scenario == "Textbook Case (Clear Effects)":
        params = {'Treatment Effect Size': 2.5, 'Survival Benefit Multiplier': 1.5, 'Gene Correlation Strength (r)': 0.8, 'Number of Significant Genes': 100}
        param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 2.5, 1.5, 0.8, 100, 42
    elif scenario == "Subtle Effects (More Realistic)":
        params = {'Treatment Effect Size': 0.8, 'Survival Benefit Multiplier': 0.5, 'Gene Correlation Strength (r)': 0.4, 'Number of Significant Genes': 20}
        param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 0.8, 0.5, 0.4, 20, 42
    else: # Failed Drug Trial
        params = {'Treatment Effect Size': 2.5, 'Survival Benefit Multiplier': 0.0, 'Gene Correlation Strength (r)': 0.8, 'Number of Significant Genes': 100}
        param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed = 2.5, 0.0, 0.8, 100, 42
    st.json(params)
    
st.subheader("Step 3: Generate and Preview the Data")

if st.button("🔬 Generate Dataset", type="primary"):
    df_full, df_volcano = generate_data(param_treatment_effect, param_survival_benefit, param_correlation_strength, param_num_hits, param_random_seed)
    st.session_state['df_full'] = df_full
    st.session_state['df_volcano'] = df_volcano
    st.success("✅ Datasets generated and stored! You can now navigate to the explorer pages.")

if 'df_full' in st.session_state:
    st.markdown("---")
    st.markdown("#### Preview of Clinical & Gene Expression Data (`df_full`)")
    st.dataframe(st.session_state['df_full'].head())
    
    st.markdown("#### Preview of Differential Expression Results (`df_volcano`)")
    st.dataframe(st.session_state['df_volcano'].head())