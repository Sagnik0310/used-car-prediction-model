import pandas as pd
from sklearn.preprocessing import LabelEncoder

from data.data_loader import DataLoader


class DataPreprocessor:
    """
    Handles all preprocessing operations.
    """

    def __init__(self):

        self.loader = DataLoader()

        self.dataframe = self.loader.load_data()

    def clean_ask_price(self):
        """
        Convert AskPrice from string to float.
        Example:
            ₹ 6,85,000 -> 685000
        """

        self.dataframe["AskPrice"] = (
            self.dataframe["AskPrice"]
            .astype(str)
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        self.dataframe["AskPrice"] = pd.to_numeric(
            self.dataframe["AskPrice"],
            errors="coerce"
        )

    def clean_km_driven(self):
        """
        Convert kmDriven into numeric.
        Example:
            98,000 km -> 98000
        """

        self.dataframe["kmDriven"] = (
            self.dataframe["kmDriven"]
            .fillna("0 km")
            .astype(str)
            .str.replace("km", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        self.dataframe["kmDriven"] = pd.to_numeric(
            self.dataframe["kmDriven"],
            errors="coerce"
        )

    def remove_duplicates(self):
        """
        Remove duplicate rows.
        """

        self.dataframe.drop_duplicates(inplace=True)

    def fill_missing_values(self):
        """
        Fill missing values.
        """

        self.dataframe["kmDriven"] = (
            self.dataframe["kmDriven"]
            .fillna(
                self.dataframe["kmDriven"].median()
            )
        )

    def select_columns(self):
        """
        Keep only useful columns.
        """

        self.dataframe = self.dataframe[
            [
                "Brand",
                "model",
                "Year",
                "Age",
                "kmDriven",
                "Transmission",
                "Owner",
                "FuelType",
                "AskPrice",
            ]
        ]

    def encode_categorical_columns(self):
        """
        Encode categorical columns.
        """

        encoder = LabelEncoder()

        columns = [
            "Brand",
            "model",
            "Transmission",
            "Owner",
            "FuelType",
        ]

        for column in columns:

            self.dataframe[column] = (
                encoder.fit_transform(
                    self.dataframe[column]
                )
            )

    def preprocess(self):
        """
        Execute complete preprocessing pipeline.
        """

        self.remove_duplicates()

        self.clean_ask_price()

        self.clean_km_driven()

        self.fill_missing_values()

        self.select_columns()

        self.encode_categorical_columns()

        self.loader.close_connection()

        return self.dataframe