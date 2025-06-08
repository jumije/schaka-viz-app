# Bioinformatics Visualization Explorer 🧬

An interactive Streamlit web app designed for the Deutsche SchülerAkademie 2025 course, "Genomische Geheimnisse: Auf Spurensuche in der Krebsforschung". This tool provides a hands-on digital lab for learning about key data visualizations in bioinformatics.

**[➡️ View the Live App!](YOUR_STREAMLIT_APP_LINK_HERE)** <!-- 👈 **IMPORTANT:** Replace this with the public URL of your deployed Streamlit app! -->

---

 
<!-- 💡 **Pro-Tip:** Record a short screen capture of you using the app (e.g., changing a slider and seeing the plot update) and save it as a GIF. Upload it to a site like imgur.com and paste the link here. It's the best way to show what your app does! -->

## About The Project

This application was created to bring data science concepts to life for students exploring bioinformatics and cancer research. Instead of just seeing static images in a presentation, this tool allows you to:

*   **Experiment** with simulated biological data.
*   **Interact** with plot parameters and see the effects in real-time.
*   **Understand** the Python code that generates these powerful visualizations.

It's a sandbox where you can build an intuition for how data, code, and storytelling come together to answer scientific questions.

## Features

This app is built around two core ideas: the **Data Lab** and the **Plot Explorers**.

### 🔬 The Data Lab
Create your own dataset on the fly! Choose from pre-defined scenarios or tune the parameters yourself to see how the underlying data affects the final plots.
*   **Pre-defined Scenarios:**
    *   `Textbook Case`: Strong, clear effects for easy interpretation.
    *   `Subtle Effects`: A more realistic dataset where the story is harder to find.
    *   `Failed Drug Trial`: A scenario where a treatment works on genes but provides no survival benefit—a crucial lesson in analysis!
*   **Custom Parameters:** You control everything from treatment effect size to gene correlation.

### 📊 Plot Explorers
For each of the five key visualizations, you get a dedicated page with interactive controls:
*   **Heatmap:** Change the colormap and see how clustering reveals patterns in gene expression across all samples.
*   **Violin Plot:** Select any gene and compare its expression distribution between the "Treated" and "Control" groups.
*   **Volcano Plot:** Adjust significance thresholds with sliders to discover which genes are the most promising "hits" in a differential expression analysis.
*   **Survival Plot:** Analyze clinical outcomes with Kaplan-Meier curves and see the impact of treatment on patient survival probability.
*   **Scatter Plot:** Investigate relationships between any two genes and instantly see their correlation coefficient.

---

## Getting Started: Running the App Locally

To run this application on your own computer, you can choose one of two methods. Using Conda and the `environment.yml` file is the most reliable way to ensure a perfect setup.

### Option 1: The Recommended Way (using Conda)

This method recreates the exact development environment and is the best for avoiding package conflicts.

1.  **Clone the repository**
    ```sh
    git clone https://github.com/YOUR_USERNAME/schaka-viz-app.git
    cd schaka-viz-app
    ```

2.  **Create the environment from the `environment.yml` file**
    This single command will create a new conda environment named `schaka-app` with all the correct dependencies installed.
    ```sh
    conda env create -f environment.yml
    ```

3.  **Activate the new environment**
    ```sh
    conda activate schaka-app
    ```

### Option 2: The Quick Way (using pip)

This method is faster if you don't use Conda, but may be more prone to dependency conflicts if your base environment has older packages.

1.  **Clone the repository**
    ```sh
    git clone https://github.com/YOUR_USERNAME/schaka-viz-app.git
    cd schaka-viz-app
    ```

2.  **Create a virtual environment (Optional but Recommended)**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    
3.  **Install requirements**
    The `requirements.txt` file contains the essential packages needed to run the app.
    ```sh
    pip install -r requirements.txt
    ```

### Running the App

Once you have installed the dependencies using either method, run the following command from your project directory:

```sh
streamlit run app.py