import streamlit as st

from data.data_loader import DataLoader
from model.predict import CarPricePredictor


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Used Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)


# -------------------------------
# Load Data
# -------------------------------

loader = DataLoader()
df = loader.load_data()
loader.close_connection()

predictor = CarPricePredictor()


# -------------------------------
# Header
# -------------------------------

st.title("🚗 Used Car Price Prediction")

st.markdown(
    """
Predict the estimated selling price of a used car using a Machine Learning model trained on historical car listings.
"""
)

st.divider()


# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.header("Car Details")

brand = st.sidebar.selectbox(
    "Brand",
    sorted(df["Brand"].unique())
)

model = st.sidebar.selectbox(
    "Model",
    sorted(
        df[df["Brand"] == brand]["model"].unique()
    )
)

fuel = st.sidebar.selectbox(
    "Fuel Type",
    sorted(df["FuelType"].unique())
)

transmission = st.sidebar.selectbox(
    "Transmission",
    sorted(df["Transmission"].unique())
)

owner = st.sidebar.selectbox(
    "Owner",
    sorted(df["Owner"].unique())
)

year = st.sidebar.number_input(
    "Manufacturing Year",
    min_value=1990,
    max_value=2035,
    value=2018
)

age = st.sidebar.number_input(
    "Vehicle Age",
    min_value=0,
    max_value=40,
    value=5
)

km = st.sidebar.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000
)


# -------------------------------
# Predict Button
# -------------------------------

if st.sidebar.button("Predict Price"):

    price = predictor.predict(
        brand,
        model,
        year,
        age,
        km,
        transmission,
        owner,
        fuel
    )

    st.success("Prediction Successful")

    st.metric(
        label="Estimated Selling Price",
        value=f"₹ {price:,.2f}"
    )


# -------------------------------
# Dataset Statistics
# -------------------------------

st.divider()

st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cars",
        len(df)
    )

with col2:
    st.metric(
        "Brands",
        df["Brand"].nunique()
    )

with col3:
    st.metric(
        "Fuel Types",
        df["FuelType"].nunique()
    )

with col4:
    st.metric(
        "Models",
        df["model"].nunique()
    )


# -------------------------------
# Dataset Preview
# -------------------------------

st.divider()

st.subheader("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)