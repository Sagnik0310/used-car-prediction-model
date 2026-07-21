import joblib
import pandas as pd


class CarPricePredictor:
    """
    Loads the trained model and predicts car prices.
    """

    def __init__(self):
        self.model = joblib.load("model/model.pkl")

    def predict(
        self,
        brand,
        model,
        year,
        age,
        km_driven,
        transmission,
        owner,
        fuel_type,
    ):
        """
        Predict the selling price of a used car.
        """

        input_dataframe = pd.DataFrame(
            {
                "Brand": [brand],
                "model": [model],
                "Year": [year],
                "Age": [age],
                "kmDriven": [km_driven],
                "Transmission": [transmission],
                "Owner": [owner],
                "FuelType": [fuel_type],
            }
        )

        prediction = self.model.predict(input_dataframe)

        return round(prediction[0], 2)