# 🚀 50 Startups Profit Prediction (CRISP-DM Workflow)

An end-to-end Machine Learning project using **Scikit-Learn** and **Streamlit** to predict startup profit based on R&D, Administration, and Marketing expenditures across multiple states. This project follows the industry-standard **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology.

LIVE DEMO：https://50startup.streamlit.app/(https://50startup.streamlit.app/)
---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Project Structure](#-project-structure)
3. [Quick Start & Setup](#-quick-start--setup)
4. [CRISP-DM Workflow Summary](#-crisp-dm-workflow-summary)
5. [Model Performance Comparison](#-model-performance-comparison)
6. [Key Business Recommendations](#-key-business-recommendations)

---

## 🌟 Project Overview
*   **Business Goal**: Predict the profitability of a startup to help Venture Capitalists (VCs) and founders make data-driven budget allocation decisions.
*   **Key Findings**: R&D expenditure is the single most critical driver of profit, contributing over **93.8%** of the model's predictive importance. The operating location (State) has negligible impact (<0.6%) on system profitability.
*   **Interactive Application**: Exposes a gorgeous glassmorphic Streamlit dashboard showcasing data explorations, correlation plots, model metrics, and a live deployment predictor.

---

## 📂 Project Structure

```
├── 50_Startups.csv         # Clean dataset containing 50 startups records
├── train.py                # CRISP-DM Machine Learning pipeline (data prep, model training & saving)
├── app.py                  # Premium Streamlit web application dashboard (deployment)
├── requirements.txt        # Python dependency specifications for local and Streamlit Cloud environments
├── analysis_report_zh.md   # Comprehensive business analysis report in Traditional Chinese
└── README.md               # Project overview and run guide (this file)
```


---

## ⚙️ CRISP-DM Workflow Summary

### 1. Business Understanding
Quantify the ROI of department-level investments (R&D, marketing, operations) and identify key factors leading to startup profitability.

### 2. Data Understanding
*   **Observations**: 50 records, zero missing values.
*   **Correlations**: R&D Spend has a Pearson correlation coefficient of **0.973** with Profit. Marketing Spend has **0.748**. Administration Spend has a low correlation of **0.201**.

### 3. Data Preparation
*   **One-Hot Encoding (獨熱編碼)**: `State` column encoded via `OneHotEncoder`. By converting categorical values into multiple binary indicator columns (0 or 1), we prevent the model from assuming an artificial hierarchy or mathematical order among different states.
*   Feature scaling: Continuous numeric fields normalized via `StandardScaler`.
*   Data Split: 80% Training set (40 rows) and 20% Testing set (10 rows).

### 4. Modeling
We trained 4 regression pipelines with hyperparameter search, including Multiple Linear Regression, Ridge Regression, Random Forest, and Gradient Boosting Regressor.

### 5. Model Evaluation
Evaluated models on the validation set. **Gradient Boosting Regressor** performed the best, explaining **93.54%** of the target variance on the test set.

### 5.1 Feature Selection Study
Explored 5 different feature selection schemes (Forward Selection, Backward Elimination, RFE, SelectKBest with F-Regression, and Mutual Info) to find the optimal combination of variables.

### 6. Deployment
The best pipeline is serialized into `best_model.pkl` and deployed as a real-time web calculator in `app.py`.

---

## 📈 Model Performance Comparison

| Model | $R^2$ Score | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) |
| :--- | :---: | :---: | :---: |
| 🏆 **Gradient Boosting Regressor** | **0.9354** | **$4,986.88** | **$7,234.09** |
| Random Forest Regressor | 0.9264 | $5,720.59 | $7,718.48 |
| Multiple Linear Regression | 0.8987 | $6,961.48 | $9,055.96 |
| Ridge Regression | 0.8985 | $6,981.72 | $9,064.07 |

### Feature Relative Importance
*   **R&D Spend**: **93.80%** (Dominant factor)
*   **Marketing Spend**: **5.05%** (Secondary factor)
*   **Administration Spend**: **0.59%** (Negligible)
*   **State**: **0.56%** (Negligible)

---

## 💡 Key Business Recommendations

1.  **Prioritize R&D Allocation**: R&D spend is the single highest-leverage investment. Budget should scale towards product development and engineering.
2.  **Strategic Marketing Spends**: Marketing is a positive multiplier but is secondary to product quality (R&D). Apply marketing budgets as an accelerator once the product is mature.
3.  **Minimize Admin Bloat**: Administrative overhead does not correlate with profit margins. Keep operational costs lean.
4.  **Ignore Location Bias**: Operational state shows no statistical significance on profit. Choose business locations based on talent access or physical logistics rather than state name profit expectations.
