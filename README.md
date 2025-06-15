# 🧬 Schaka Bioinformatics Learning Lab

This is an interactive web application built with Streamlit for the Deutsche SchülerAkademie course "Genomische Geheimnisse: Auf Spurensuche in der Krebsforschung". It serves as a hands-on learning environment for data handling, analysis, and visualization in Python.

## Features

- **Interactive Data Generation:** A "Data Lab" to create simulated biological datasets with user-controlled parameters.
- **Multi-Page Layout:** Each key visualization type has its own dedicated learning page.
- **Guided Learning:** Expander sections explain the theory behind each plot.
- **Control Panels:** Interactive widgets allow students to experiment with plot parameters without writing code.
- **Live Coding Sandbox:** Students can modify and execute Python code directly in the app to answer scientific questions and see the results instantly.

## 🚀 Getting Started

You will need a few things installed on your computer to run this app locally and deploy it.

### Prerequisites
1.  **Python:** Version 3.9 or higher.
2.  **Conda or Venv:** A way to manage Python environments is highly recommended.
3.  **Git and a GitHub Account:** To clone the repository and deploy the app.

### Local Setup Instructions

1.  **Clone the Repository:**
    Open your terminal or command prompt and clone the project files from GitHub.
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Set Up Environment (Recommended):**
    Create a clean Python environment to avoid conflicts with other projects.
    ```bash
    # Using conda
    conda create --name schaka-app-env python=3.10
    conda activate schaka-app-env
    ```

3.  **Install Dependencies:**
    This project uses a `requirements.txt` file to manage its specific library needs. **Do not use a full conda environment file for deployment.**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    Once the dependencies are installed, you can launch the Streamlit app.
    ```bash
    streamlit run app.py
    ```
    The app should automatically open in a new tab in your web browser!

### Deployment to Streamlit Community Cloud

You can host this app for free so your students can access it from anywhere.

1.  **Push to GitHub:** Make sure your project folder (containing `app.py`, `requirements.txt`, and the `pages/` directory) is a public GitHub repository.
2.  **Sign Up:** Go to [share.streamlit.io](https://share.streamlit.io) and sign up using your GitHub account.
3.  **Deploy:**
    - Click "New app".
    - Select your repository and the `main` branch.
    - The "Main file path" should be `app.py`.
    - Click "Deploy!".

Streamlit will build the app from your GitHub repository and host it on a public URL. Any time you `git push` an update to your `main` branch, the app will automatically redeploy.