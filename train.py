"""
train.py
50 Startups Profit Prediction ML Pipeline (CRISP-DM)
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def main():
    print("==================================================")
    # 1. BUSINESS UNDERSTANDING
    print("PHASE 1: Business Understanding")
    print("Goal: Predict the profit of a startup based on its R&D Spend,")
    print("Administration Spend, Marketing Spend, and operating State.")
    print("This allows VCs and founders to understand what factors drive profit.")
    print("==================================================")

    # 2. DATA UNDERSTANDING
    print("\nPHASE 2: Data Understanding")
    data_path = "50_Startups.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset {data_path} not found!")
    
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nData description:")
    print(df.describe())
    
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Calculate correlation of numeric features
    numeric_cols = ["R&D Spend", "Administration", "Marketing Spend", "Profit"]
    corr_matrix = df[numeric_cols].corr().to_dict()
    
    # Calculate state statistics
    state_stats = df.groupby("State")["Profit"].agg(["mean", "median", "count"]).to_dict(orient="index")

    # 3. DATA PREPARATION
    print("\nPHASE 3: Data Preparation")
    
    # Features and Target
    X = df.drop(columns=["Profit"])
    y = df["Profit"]
    
    # Identify numerical and categorical columns
    num_features = ["R&D Spend", "Administration", "Marketing Spend"]
    cat_features = ["State"]
    
    # Create preprocessing pipelines
    num_transformer = StandardScaler()
    cat_transformer = OneHotEncoder(handle_unknown="ignore")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_features),
            ("cat", cat_transformer, cat_features)
        ]
    )
    
    # Split training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")

    # 4. MODELING
    print("\nPHASE 4: Modeling")
    
    # Dictionary of models to evaluate
    models = {
        "Multiple Linear Regression": LinearRegression(),
        "Ridge Regression": GridSearchCV(
            Ridge(),
            param_grid={"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]},
            cv=5
        ),
        "Random Forest Regressor": GridSearchCV(
            RandomForestRegressor(random_state=42),
            param_grid={"n_estimators": [50, 100, 200], "max_depth": [None, 5, 10]},
            cv=5
        ),
        "Gradient Boosting Regressor": GridSearchCV(
            GradientBoostingRegressor(random_state=42),
            param_grid={"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.05, 0.1], "max_depth": [3, 4]},
            cv=5
        )
    }
    
    model_results = {}
    trained_pipelines = {}
    
    for model_name, model in models.items():
        print(f"Training {model_name}...")
        # Build pipeline
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        trained_pipelines[model_name] = pipeline
        
        # Predict
        y_pred = pipeline.predict(X_test)
        
        # 5. EVALUATION
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        model_results[model_name] = {
            "MAE": round(float(mae), 2),
            "RMSE": round(float(rmse), 2),
            "R2": round(float(r2), 4)
        }
        print(f"  Results: R2 = {r2:.4f} | MAE = {mae:.2f} | RMSE = {rmse:.2f}")
        
    print("\nPHASE 5: Evaluation & Model Selection")
    # Choose best model based on R2
    best_model_name = max(model_results, key=lambda k: model_results[k]["R2"])
    best_pipeline = trained_pipelines[best_model_name]
    print(f"Best Model Selected: {best_model_name}")
    print(f"Best Model Metrics: {model_results[best_model_name]}")
    
    # Feature Importance (Extract from best model if supported)
    feature_importances = {}
    
    # Retrieve transformer categories for feature names
    cat_encoder = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
    # Handle both pre-1.0 and modern versions of OneHotEncoder get_feature_names
    if hasattr(cat_encoder, "get_feature_names_out"):
        encoded_cats = list(cat_encoder.get_feature_names_out(cat_features))
    else:
        encoded_cats = list(cat_encoder.get_feature_names(cat_features))
    
    all_features = num_features + encoded_cats
    
    # Extract model coefficients or feature importances
    regressor = best_pipeline.named_steps["regressor"]
    if hasattr(regressor, "best_estimator_"):
        regressor = regressor.best_estimator_
        
    if hasattr(regressor, "coef_"):
        importances = list(regressor.coef_)
        importance_type = "Coefficients"
    elif hasattr(regressor, "feature_importances_"):
        importances = list(regressor.feature_importances_)
        importance_type = "Feature Importances"
    else:
        importances = [0.0] * len(all_features)
        importance_type = "N/A"
        
    feature_importances = {
        "type": importance_type,
        "features": all_features,
        "values": [round(float(val), 4) for val in importances]
    }
    print(f"Feature Importances/Coefficients: {dict(zip(all_features, importances))}")
    
    # 6. DEPLOYMENT (Save artifacts)
    print("\nPHASE 6: Deployment Prep")
    model_filename = "best_model.pkl"
    with open(model_filename, "wb") as f:
        pickle.dump(best_pipeline, f)
    print(f"Saved best model pipeline to {model_filename}")
    
    # Save statistics and evaluation metrics to JSON for Streamlit App
    metrics_data = {
        "best_model_name": best_model_name,
        "metrics": model_results,
        "feature_importances": feature_importances,
        "summary_stats": {
            "shape": df.shape,
            "corr_matrix": corr_matrix,
            "state_stats": state_stats,
            "columns": list(df.columns)
        }
    }
    
    metrics_filename = "model_metrics.json"
    with open(metrics_filename, "w") as f:
        json.dump(metrics_data, f, indent=4)
    print(f"Saved model evaluation metrics to {metrics_filename}")
    print("==================================================")

if __name__ == "__main__":
    main()
