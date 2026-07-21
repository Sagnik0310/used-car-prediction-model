import os
import joblib
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from preprocessing.preprocessing import DataPreprocessor


def main():

    preprocessor = DataPreprocessor()

    dataframe = preprocessor.preprocess()

    X = dataframe.drop("AskPrice", axis=1)

    y = dataframe["AskPrice"]

    categorical_features = [
        "Brand",
        "model",
        "Transmission",
        "Owner",
        "FuelType",
    ]

    numerical_features = [
        "Year",
        "Age",
        "kmDriven",
    ]

    transformer = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            (
                "numerical",
                SimpleImputer(strategy="median"),
                numerical_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", transformer),
            ("regressor", LinearRegression()),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    mse = mean_squared_error(y_test, predictions)

    rmse = np.sqrt(mse)

    r2 = r2_score(y_test, predictions)

    print("\n===== MODEL PERFORMANCE =====")

    print(f"MAE  : {mae:,.2f}")

    print(f"MSE  : {mse:,.2f}")

    print(f"RMSE : {rmse:,.2f}")

    print(f"R²   : {r2:.4f}")

    os.makedirs("model", exist_ok=True)

    joblib.dump(
        model,
        "model/model.pkl",
    )

    print("\nModel saved successfully.")


if __name__ == "__main__":
    main()