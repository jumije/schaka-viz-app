import streamlit as st
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
from io import StringIO
import sys

# Page configuration
st.set_page_config(layout="wide")
st.title("📈 Kaplan-Meier Survival Plot Explorer")

# Check if data exists in session state
if 'df_full' not in st.session_state:
    st.warning("Please generate a dataset in the '🧪 Data Lab' first!")
    st.stop()

# Load data from session state
df = st.session_state['df_full']

# --- Guided Tour Expander ---
with st.expander("LEARN: What is a Survival Plot?"):
    st.markdown("""
    A **Kaplan-Meier survival plot** is one of the most important visualizations in clinical research. It's used to estimate and plot the probability of survival over time.
    
    - **When to Use:** To visualize "time-to-event" data. It is perfectly suited to answer questions like, "Do patients who received Drug A survive longer than patients who received a placebo?"
    - **Key Features:**
        - **Step-wise Curve:** The curve goes down each time an "event" (e.g., death) occurs.
        - **Y-axis:** Represents the estimated survival probability, from 1.0 (100%) at the start.
        - **X-axis:** Represents time since the start of the study or treatment.
        - **Censoring (the small ticks):** This is a crucial concept. A tick indicates that a patient left the study at that time point and was still alive (e.g., the study ended). The Kaplan-Meier model correctly incorporates this information.
    - **Library:** We use a specialized library called `lifelines` for this type of analysis.
    """)

# --- Control Panel and Plot ---
st.header("EXPERIMENT: The Control Panel")
st.markdown("Experiment with the plot's appearance and see how the 'Survival Benefit' from the Data Lab changes the story.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parameters")
    ci_show = st.checkbox("Show 95% Confidence Interval (`ci_show`)", value=True)
    show_censor_ticks = st.checkbox("Show censor ticks (`censor_styles`)", value=True)
    st.info("The Confidence Interval shows the uncertainty in our estimate. If the intervals for two groups do not overlap, it suggests a significant difference.")

with col2:
    st.subheader("Interactive Plot")
    fig, ax = plt.subplots(figsize=(8, 6))
    kmf = KaplanMeierFitter()
    
    for group in df['Treatment_Group'].unique():
        mask = df['Treatment_Group'] == group
        kmf.fit(df[mask]['Survival_Time_days'], df[mask]['Event_Status'], label=group)
        kmf.plot_survival_function(
            ax=ax,
            ci_show=ci_show,
            censor_styles={'ms': 6, 'marker': '|' if show_censor_ticks else 'None'}
        )
    
    ax.set_title('Kaplan-Meier Survival Curves by Treatment Group', fontsize=16)
    ax.set_xlabel('Time (Days)', fontsize=12)
    ax.set_ylabel('Survival Probability', fontsize=12)
    ax.legend(title='Group')
    st.pyplot(fig)


# --- Coding Sandbox ---
st.header("DISCOVER: The Coding Sandbox")
st.info("**Scientific Question:** Generate a survival plot for the 'Treated' vs 'Control' groups. Can you customize the plot to make the lines thicker and use different styles (e.g., a dashed line for 'Control')?")

code_template = """
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# The clinical data is in a DataFrame called `df`.
fig, ax = plt.subplots(figsize=(8, 6))
kmf = KaplanMeierFitter()

# We can plot each group manually to control its style
# Plot for the 'Treated' group
mask_treated = df['Treatment_Group'] == 'Treated'
kmf.fit(df[mask_treated]['Survival_Time_days'], df[mask_treated]['Event_Status'], label='Treated')
kmf.plot_survival_function(ax=ax, lw=3) # lw is line width

# Plot for the 'Control' group
mask_control = df['Treatment_Group'] == 'Control'
kmf.fit(df[mask_control]['Survival_Time_days'], df[mask_control]['Event_Status'], label='Control')
kmf.plot_survival_function(ax=ax, lw=3, linestyle='--') # Add a dashed line style

ax.set_title('Customized Survival Plot', fontsize=16)
st.pyplot(fig)
"""

code = st.text_area("Edit your Python code here:", value=code_template, height=400)

if st.button("Run Code", type="primary"):
    st.subheader("Your Output")
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        exec(code, {'st': st, 'plt': plt, 'KaplanMeierFitter': KaplanMeierFitter, 'df': df})
        console_output = captured_output.getvalue()
        if console_output:
            st.code(console_output, language='bash')
    except Exception as e:
        st.error(f"🚨 An error occurred:\n{e}")
    sys.stdout = old_stdout