"""
app.py
50 Startups Interactive Profit Predictor & CRISP-DM Showcase
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="50 Startups CRISP-DM Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.03) 0%, rgba(168, 85, 247, 0.03) 90%);
    }
    
    /* Dashboard Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.04);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    .light-theme-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Metrics Styling */
    .premium-metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    
    .premium-metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Headings */
    .gradient-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .dark-mode-section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.25s ease-in-out !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* Custom Prediction Alert Card */
    .pred-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-top: 20px;
    }
    
    .pred-val {
        font-size: 3rem;
        font-weight: 800;
        color: #6366f1;
        margin: 10px 0;
        text-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model metrics
@st.cache_data
def load_metrics_and_data():
    metrics_path = "model_metrics.json"
    data_path = "50_Startups.csv"
    
    metrics = None
    df = None
    
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        
    return metrics, df

# Helper to load trained pipeline
@st.cache_resource
def load_model():
    model_path = "best_model.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

metrics, df = load_metrics_and_data()
model_pipeline = load_model()

# Sidebar Setup
st.sidebar.markdown("<div style='text-align: center; padding: 10px;'><h2 style='margin-bottom:0;'>🚀 CRISP-DM</h2><p style='color:#6366f1; font-weight:600;'>50 Startups Solver</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Select CRISP-DM Phase:",
    [
        "🚀 Project Overview",
        "1. Business Understanding",
        "2. Data Understanding",
        "3 & 4. Prep & Modeling",
        "5. Model Evaluation",
        "6. Interactive Predictor (Deployment)"
    ]
)

# Define columns theme helper
is_dark = True  # We default to glass-card overlay which looks premium on both.
card_class = "glass-card"

# ----------------- OVERVIEW -----------------
if app_mode == "🚀 Project Overview":
    st.markdown("<h1 class='gradient-text'>50 Startups Profit Prediction Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome! This interactive dashboard applies the industry-standard **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology to solve the **50 Startups** prediction problem. 
    Using machine learning, we predict startup profit based on R&D, Administration, and Marketing spends, and the state of operations.
    """)
    
    # Showcase cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='premium-metric-title'>Dataset Size</div>
            <div class='premium-metric-value'>50 Startups</div>
            <p style='margin-top:8px; font-size:0.9rem; color:#64748b;'>Clean records across three states.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        best_r2 = "N/A"
        if metrics:
            best_model_name = metrics["best_model_name"]
            best_r2 = f"{metrics['metrics'][best_model_name]['R2'] * 100:.2f}%"
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='premium-metric-title'>Best Model R² Score</div>
            <div class='premium-metric-value'>{best_r2}</div>
            <p style='margin-top:8px; font-size:0.9rem; color:#64748b;'>High-accuracy variance explanation.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        top_driver = "R&D Spend"
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='premium-metric-title'>Key Profit Driver</div>
            <div class='premium-metric-value'>{top_driver}</div>
            <p style='margin-top:8px; font-size:0.9rem; color:#64748b;'>Determined via regression coefficients.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### The CRISP-DM Lifecycle Steps in this App:")
    
    st.markdown(f"""
    <div class='{card_class}'>
        <ol>
            <li><b>Business Understanding</b>: Define the business questions and objectives.</li>
            <li><b>Data Understanding</b>: Explore the 50 Startups dataset structure, summary statistics, and correlations.</li>
            <li><b>Data Preparation</b>: Preprocess variables (Scaling and One-Hot Encoding state categories).</li>
            <li><b>Modeling</b>: Train and optimize multiple regression models (Linear, Ridge, Random Forest, Gradient Boosting).</li>
            <li><b>Evaluation</b>: Evaluate model performances on test data and analyze feature impacts.</li>
            <li><b>Deployment</b>: Expose the best-performing model pipeline via an interactive web calculator.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ----------------- PHASE 1: BUSINESS UNDERSTANDING -----------------
elif app_mode == "1. Business Understanding":
    st.markdown("<h1 class='gradient-text'>Phase 1: Business Understanding</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='{card_class}'>
        <h3>🎯 The Problem & Objectives</h3>
        <p>
            Venture Capitalists and startup incubators evaluate dozens of business ideas and pitches daily.
            One major question they face is: <b>How do spending patterns in research and development, administration, and marketing relate to the ultimate profitability of a startup?</b>
        </p>
        <p>
            By leveraging machine learning, we want to construct a reliable predictive model that:
            <ul>
                <li>Accurately predicts a startup's <b>Profit</b>.</li>
                <li>Identifies which spending category (e.g. <b>R&D</b> vs. <b>Marketing</b>) has the highest positive correlation with Profit.</li>
                <li>Determines if operational location (<b>State</b>) plays a significant role in profit variation.</li>
            </ul>
        </p>
        <p><b>Business Action:</b> Allocate investment budgets efficiently across R&D, operations, and marketing to optimize profit margins.</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- PHASE 2: DATA UNDERSTANDING -----------------
elif app_mode == "2. Data Understanding":
    st.markdown("<h1 class='gradient-text'>Phase 2: Data Understanding</h1>", unsafe_allow_html=True)
    
    if df is not None:
        tab1, tab2, tab3 = st.tabs(["📊 Dataset Viewer & Stats", "📈 Visual Relationships", "🕸️ Correlation Analysis"])
        
        with tab1:
            st.markdown("### Raw Dataset View (50 Startups)")
            st.dataframe(df.style.background_gradient(cmap="Purples", subset=["Profit"]), width="stretch")
            
            st.markdown("### Summary Statistics")
            st.dataframe(df.describe().T, width="stretch")
            
        with tab2:
            st.markdown("### Explore Spend Categories vs Profit")
            feature_to_plot = st.selectbox("Choose feature to plot against Profit:", ["R&D Spend", "Administration", "Marketing Spend"])
            
            # Draw beautiful interactive Altair scatter plot
            scatter = alt.Chart(df).mark_circle(size=80, opacity=0.8).encode(
                x=alt.X(feature_to_plot, title=f"{feature_to_plot} ($)"),
                y=alt.Y('Profit', title='Profit ($)'),
                color=alt.Color('State', scale=alt.Scale(scheme='set2')),
                tooltip=['R&D Spend', 'Administration', 'Marketing Spend', 'State', 'Profit']
            ).properties(
                height=450,
                width=800
            ).interactive()
            
            st.altair_chart(scatter, use_container_width=True)
            
        with tab3:
            st.markdown("### Correlation Heatmap (Numeric Columns)")
            
            if metrics:
                corr = pd.DataFrame(metrics["summary_stats"]["corr_matrix"])
                
                # Styled Correlation Matrix representation in Streamlit
                st.dataframe(corr.style.background_gradient(cmap="coolwarm", axis=None).format("{:.3f}"), width="stretch")
                st.markdown("""
                > **Insights:**
                > * **R&D Spend** has an extremely high correlation (~0.97) with **Profit**, suggesting it is the primary driver.
                > * **Marketing Spend** also shows a strong positive correlation (~0.75) with Profit.
                > * **Administration Spend** has very little correlation (~0.20) with Profit, indicating operations overhead doesn't directly scale profitability.
                """)
    else:
        st.error("Dataset not found! Please run the training pipeline first to make sure files are generated.")

# ----------------- PHASE 3 & 4: DATA PREP & MODELING -----------------
elif app_mode == "3 & 4. Prep & Modeling":
    st.markdown("<h1 class='gradient-text'>Phases 3 & 4: Data Preparation & Modeling</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='{card_class}'>
            <h3>🛠️ Data Preparation Steps</h3>
            <p>To prepare the raw startup data for Scikit-learn regressors, we executed:</p>
            <ul>
                <li><b>One-Hot Encoding:</b> Converted the categorical column <code>State</code> (New York, California, Florida) into indicator columns to avoid imposing an artificial numerical order.</li>
                <li><b>Standardization:</b> Normalized numeric columns (<code>R&D Spend</code>, <code>Administration</code>, <code>Marketing Spend</code>) to have a mean of 0 and standard deviation of 1. This prevents features with larger ranges from dominating models like Ridge or Gradient Boosting.</li>
                <li><b>Train-Test Split:</b> Split the data into an 80% Training set (40 startups) and 20% Validation set (10 startups) to measure generalization performance.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class='{card_class}'>
            <h3>🤖 Model Selection Strategy</h3>
            <p>We trained four distinct types of algorithms using Scikit-Learn pipelines to identify the best fit:</p>
            <ol>
                <li><b>Multiple Linear Regression:</b> Provides a baseline understanding and directly interpretable linear equations.</li>
                <li><b>Ridge Regression (L2 Regularization):</b> Adds regularized penalties to coefficients to control potential overfitting.</li>
                <li><b>Random Forest Regressor:</b> An ensemble tree-based method that models non-linear relationships.</li>
                <li><b>Gradient Boosting Regressor:</b> Sequentially builds boosting decision trees to minimize residuals.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ----------------- PHASE 5: EVALUATION -----------------
elif app_mode == "5. Model Evaluation":
    st.markdown("<h1 class='gradient-text'>Phase 5: Evaluation</h1>", unsafe_allow_html=True)
    
    if metrics:
        st.markdown("### Model Comparison Matrix")
        st.markdown("Below are the validation set results of all evaluated models, sorted by performance.")
        
        comparison_df = pd.DataFrame(metrics["metrics"]).T
        comparison_df = comparison_df.sort_values(by="R2", ascending=False)
        st.dataframe(comparison_df.style.highlight_max(axis=0, color="#dcfce7", subset=["R2"]).highlight_min(axis=0, color="#fee2e2", subset=["MAE", "RMSE"]), width="stretch")
        
        # Highlight best model
        best_name = metrics["best_model_name"]
        st.success(f"🏆 The **{best_name}** achieved the best performance with an $R^2$ of **{metrics['metrics'][best_name]['R2']:.4f}**.")
        
        # Plot Feature Importance/Coefficients
        st.markdown("### Feature Coefficients / Importances")
        feat_imp = metrics["feature_importances"]
        
        if feat_imp["type"] != "N/A":
            imp_df = pd.DataFrame({
                "Feature": feat_imp["features"],
                "Value": feat_imp["values"]
            })
            imp_df = imp_df.sort_values(by="Value", ascending=True)
            
            bar_chart = alt.Chart(imp_df).mark_bar(color="#6366f1", cornerRadius=4).encode(
                x=alt.X('Value', title=f"{feat_imp['type']} Value"),
                y=alt.Y('Feature', sort='-x', title='Features'),
                tooltip=['Feature', 'Value']
            ).properties(
                height=300,
                width=800
            )
            
            st.altair_chart(bar_chart, use_container_width=True)
            st.markdown(f"""
            This chart visualizes the model's coefficients/importances. 
            * If **Linear/Ridge**: Positive values indicate a positive correlation (higher spend increases profit).
            * If **Tree-based**: Higher positive values indicate higher relative split importance of the feature.
            """)
    else:
        st.warning("Model metrics file not found. Please run the training pipeline first using `python train.py`.")

# ----------------- PHASE 6: DEPLOYMENT INTERACTIVE PREDICTOR -----------------
elif app_mode == "6. Interactive Predictor (Deployment)":
    st.markdown("<h1 class='gradient-text'>Phase 6: Deployment Predictor</h1>", unsafe_allow_html=True)
    st.markdown("Test the deployed Scikit-Learn machine learning pipeline. Input a custom budget allocation below to predict the startup's profitability in real-time.")
    
    if model_pipeline is not None and metrics is not None:
        best_model_name = metrics["best_model_name"]
        st.info(f"Active Pipeline Model: **{best_model_name}**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
            st.markdown("#### 🛠️ Budget Allocation Parameters")
            
            # Numeric inputs
            rd_spend = st.slider("R&D Spend ($)", min_value=0, max_value=250000, value=75000, step=1000)
            marketing_spend = st.slider("Marketing Spend ($)", min_value=0, max_value=500000, value=150000, step=2500)
            admin_spend = st.slider("Administration Spend ($)", min_value=0, max_value=200000, value=120000, step=1000)
            
            # Categorical state input
            states = ["California", "Florida", "New York"]
            state = st.selectbox("Operating State", states)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"<div class='{card_class}' style='height: 100%; display: flex; flex-direction: column; justify-content: center;'>", unsafe_allow_html=True)
            st.markdown("#### 🔮 Run Predictor")
            st.write("Click below to run the input vector through the preprocessing transformer and selected regressor.")
            
            if st.button("Predict Startup Profit"):
                # Construct dataframe from user inputs
                input_df = pd.DataFrame([{
                    "R&D Spend": rd_spend,
                    "Administration": admin_spend,
                    "Marketing Spend": marketing_spend,
                    "State": state
                }])
                
                # Make prediction
                prediction = model_pipeline.predict(input_df)[0]
                
                # Show results with sleek custom element
                st.markdown(f"""
                <div class='pred-card'>
                    <div style='font-size:0.9rem; text-transform:uppercase; color:#94a3b8; font-weight:600;'>Predicted Profit Margin</div>
                    <div class='pred-val'>${prediction:,.2f}</div>
                    <div style='font-size:0.85rem; color:#64748b;'>R&D to Profit Efficiency: {rd_spend/max(1, prediction)*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Model and metrics not found. Run the training pipeline (`python train.py`) first to deploy the model.")
