import streamlit as st
from sidebar_datainput import show_sidebar_data_input

st.set_page_config(
    page_title="Schaka Bioinformatics Learning Lab",
    page_icon="🧬",
    layout="wide"
)

# --- Show the Sidebar Data Lab ---
show_sidebar_data_input()

# --- Main Page Welcome Content ---
st.title("Welcome to the Bioinformatics Learning Lab!")
st.markdown("## A hands-on environment for your journey into cancer data analysis.")
st.markdown("""
In this interactive app, you will not just see visualizations — you will build, modify, and experiment with them yourself.

## How to Use This Lab:

1.  **Use the `Data Lab` in the sidebar to create and modify your dataset.** Choose a scenario or set custom parameters, then click **`Generate/Update Dataset`**.
2.  **The dataset is live!** Changes you make in the sidebar will immediately affect the plots on any page.
3.  **Navigate to a visualization page** using the links in the sidebar to start exploring.
""")

# --- Dataset Explanation ---
with st.expander("📋 Click here to learn about the **Data Lab** and the **Datasets** it simulates"):
    st.markdown("""
    ### The Generated DataFrames
    
    The Data Lab generates two related, simulated datasets that mimic a real cancer research study.
                
    #### 1. Clinical & Expression Data
        Represents data for 100 patients, including their treatment group, cancer subtype, gene expression levels, and survival outcome. This is used for the Scatter, Violin, Heatmap, and Survival plots.
    
        - **Patient Info (Metadata):**
            - `Sample_ID`: A unique ID for each patient.
            - `Treatment_Group`: Whether the patient received the new drug (`Treated`) or a placebo (`Control`).
            - `Cancer_Subtype`: The type of cancer the patient has (`Subtype_A`, `B`, or `C`).
    
        - **Molecular Data:**
            - `Gene_A` to `Gene_J`: The measured expression level for 10 different genes. A higher number means the gene is more "active." The values are on a log2 scale, which is common in biology.
    
        - **Clinical Outcome:**
            - `Survival_Time_days`: The number of days the patient was followed in the study.
            - `Event_Status`: The patient's status at the end of their follow-up. `1` means the event (death) occurred. `0` means the patient was **censored** (e.g., the study ended and they were still alive). This is crucial for survival analysis.
    

    #### 2. Statistical Results 
        Simulates the results of a statistical analysis on 1,000 genes, showing how much each gene's expression changed and how significant that change was. This is used for the Volcano Plot.
                
        - `gene_id`: The identifier for each gene.
                
        - `log2_Fold_Change`: The magnitude of the expression change. A value of `1` means the gene's expression doubled in the treated group; `-1` means it was halved.
                
        - `neg_log10_p_value`: The statistical significance. A p-value tells you the probability of seeing a result by chance. By taking the `-log10`, we make very small (and therefore very significant) p-values into large numbers. **A higher value on this column means higher significance!**
    """)

# --- Parameter Explanation ---
with st.expander("🎛️ Click here to learn about the **Data Lab** and the **Parameters** it uses"):
    st.markdown("""
    #### The Data Lab Parameters (Your Controls!)
                
    The sliders and scenarios in the sidebar directly control the properties of the simulated data. Understanding them is key to data storytelling.

    - **Treatment Effect:**
        - **What it controls:** How strongly the drug affects the expression of `Gene_B`, `Gene_C`, and `Gene_H`.
        - **High Value:** Creates a large, obvious difference in expression between the 'Treated' and 'Control' groups. This will be very visible in the **Violin Plots** and **Heatmap**.
        - **Low Value:** Creates a subtle, small difference that might be hard to distinguish from random noise, which is more common with real-world data.

    - **Survival Benefit:**
        - **What it controls:** How much longer, on average, the 'Treated' patients survive compared to the 'Control' patients.
        - **High Value:** Creates a large, clear separation between the two curves in the **Survival Plot**, indicating a very effective drug.
        - **Low Value (or 0):** The survival curves will be very close or overlapping, suggesting the drug has little to no effect on patient survival, even if it changes gene expression.

    - **Gene Correlation:**
        - **What it controls:** The strength of the relationship between the expression of `Gene_D` and `Gene_E`.
        - **High Value (close to 1.0):** The points in the **Scatter Plot** will form a tight, clear line, simulating a strong biological co-regulation. The Pearson 'r' value will be high.
        - **Low Value (close to 0.0):** The points will look like a random cloud, simulating two unrelated genes. The Pearson 'r' value will be near zero.

    - **Significant Genes:**
        - **What it controls:** The number of "hit" genes that are simulated to be significantly affected by the treatment.
        - **High Value:** Many genes will appear as significant (colored red and blue) in the **Volcano Plot**, simulating a drug with widespread, systemic effects.
        - **Low Value:** Very few genes will pass the significance threshold, simulating a drug with a highly specific and targeted effect.
    """)

# A check to ensure data is loaded, and guide the user.
if 'df_full' in st.session_state:
    st.info("Dataset is ready. Choose a visualization from the sidebar to continue.")
else:
    st.warning("👈 **Please generate a dataset in the sidebar to get started!**")