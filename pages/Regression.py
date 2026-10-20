
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from scipy import sparse


# --------------------------------------------------
# Paths and page configuration
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "regression" / "Melbourne_housing.csv"
MODEL_DIR = ROOT / "models"

st.set_page_config(
    page_title="Regression | ML Explorer",
    page_icon="🏠",
    layout="wide",
)

st.title("Regression")
st.caption("Melbourne Housing · Explore data, compare models, predict prices")

st.markdown(
    """
    Explore the housing dataset and use trained regression models
    to estimate a property's price.
    """
)


# --------------------------------------------------
# Load data and artifacts lazily
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_artifact(filename):
    return joblib.load(MODEL_DIR / filename)


try:
    df = load_data()
    preprocessor = load_artifact("housing_preprocessor.joblib")
except Exception as exc:
    st.error(f"Could not load the dataset or preprocessor: {exc}")
    st.stop()


# --------------------------------------------------
# Dataset overview
# --------------------------------------------------
st.subheader("Dataset overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Rows", f"{len(df):,}")
m2.metric("Columns", len(df.columns))
m3.metric(
    "Missing values",
    f"{int(df.isna().sum().sum()):,}",
)
m4.metric(
    "Median price",
    (
        f"A${df['Price'].median():,.0f}"
        if "Price" in df.columns
        else "Unavailable"
    ),
)

overview_tab, data_tab, prediction_tab = st.tabs(
    ["Overview", "Explore data", "Predict a price"]
)

with overview_tab:
    left, right = st.columns(2)

    with left:
        st.markdown("#### Dataset information")
        st.write(f"**File:** `{DATA_PATH.name}`")
        st.write(f"**Rows:** {len(df):,}")
        st.write(f"**Columns:** {len(df.columns)}")

        if "Price" in df.columns:
            st.write(
                f"**Price range:** A${df['Price'].min():,.0f}"
                f" – A${df['Price'].max():,.0f}"
            )

    with right:
        st.markdown("#### Missing values by column")
        missing = df.isna().sum().sort_values(ascending=False)
        missing = missing[missing > 0]

        if missing.empty:
            st.success("No missing values found.")
        else:
            st.dataframe(
                missing.rename("Missing values").to_frame(),
                use_container_width=True,
            )

    if "Price" in df.columns:
        st.markdown("#### Price distribution")
        price_bins = pd.cut(df["Price"], bins=20)

price_distribution = (
    price_bins
    .value_counts()
    .sort_index()
    .rename_axis("Price range")
    .reset_index(name="Number of properties")
)

price_distribution["Price range"] = (
    price_distribution["Price range"].astype(str)
)

st.bar_chart(
    price_distribution,
    x="Price range",
    y="Number of properties",
)

with data_tab:
    st.markdown("#### Preview")
    st.dataframe(df.head(100), use_container_width=True)

    st.markdown("#### Column types")
    types = pd.DataFrame({
        "Column": df.columns,
        "Data type": df.dtypes.astype(str).values,
        "Missing values": df.isna().sum().values,
        "Unique values": df.nunique(dropna=True).values,
    })
    st.dataframe(types, use_container_width=True)


# --------------------------------------------------
# Model definitions
# --------------------------------------------------


MODEL_FILES = {
    "Linear Regression": "linear_regression.joblib",
    "Ridge Regression": "ridge_regression.joblib",
    "Lasso Regression": "lasso_regression.joblib",
    "Elastic Net": "elasticnet_regression.joblib",
    "Decision Tree": "decision_tree_regressor.joblib",
    "Gradient Boosting": "gradient_boosting_regressor.joblib",
    "K-Nearest Neighbors": "knn_regressor.joblib",
    "Support Vector Regression": "svr.joblib",
    "Polynomial Regression": "polynomial_regression.joblib",
}




# --------------------------------------------------
# Prediction helpers
# --------------------------------------------------
def prepare_input(raw_row):
    """Apply the saved preprocessing to raw property features."""
    numeric_columns = list(preprocessor.transformers_[0][2])
    categorical_columns = list(preprocessor.transformers_[1][2])

    ordered_columns = numeric_columns + categorical_columns
    ordered_row = raw_row[ordered_columns].copy()

    # Match the training notebook's treatment of Postcode.
    ordered_row["Postcode"] = ordered_row["Postcode"].astype(object)

    return preprocessor.transform(ordered_row)


def predict_price(model_name, raw_row):
    """Predict a price using the matching saved estimator."""
    X_processed = prepare_input(raw_row)
    model = load_artifact(MODEL_FILES[model_name])

    if model_name == "Polynomial Regression":
        artifacts = load_artifact("polynomial_artifacts.joblib")
        poly = artifacts["transformer"]
        poly_indices = artifacts["polynomial_indices"]
        remaining_indices = artifacts["remaining_indices"]
        numeric_features = artifacts["numerical_features"]

        numeric_count = len(numeric_features)
        X_numeric = X_processed[:, :numeric_count]

        X_poly = poly.transform(X_numeric[:, poly_indices])
        X_remaining = X_processed[:, remaining_indices]

        X_final = sparse.hstack(
            [X_poly, X_remaining],
            format="csr",
        )
        prediction = model.predict(X_final)

    else:
        prediction = model.predict(X_processed)

    # The notebook trained SVR on a scaled target.
    if model_name == "Support Vector Regression":
        scaler = load_artifact("svr_target_scaler.joblib")
        prediction = scaler.inverse_transform(
            np.asarray(prediction).reshape(-1, 1)
        ).ravel()

    return float(np.asarray(prediction).ravel()[0])


# --------------------------------------------------
# Prediction interface
# --------------------------------------------------
with prediction_tab:
    st.markdown("#### Enter property details")
    st.caption(
        "Select values for the property's features. "
        "Property age is calculated from the sale year and year built."
    )

    required_columns = (
    list(preprocessor.transformers_[0][2])
    + list(preprocessor.transformers_[1][2])
)

# PropertyAge is engineered by the notebook, not stored in the raw CSV.
if "PropertyAge" in required_columns and "PropertyAge" not in df.columns:
    if "Date" not in df.columns or "YearBuilt" not in df.columns:
        st.error(
            "Cannot derive PropertyAge: Date or YearBuilt is missing."
        )
        st.stop()

    sale_years = pd.to_datetime(df["Date"], errors="coerce").dt.year
    df["PropertyAge"] = sale_years - pd.to_numeric(
        df["YearBuilt"], errors="coerce"
    )

    # Match the notebook: negative property ages are treated as missing.
    df.loc[df["PropertyAge"] < 0, "PropertyAge"] = np.nan

    missing_columns = [c for c in required_columns if c not in df.columns]

    if missing_columns:
        st.error(
            "The dataset is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    def category_options(column, fallback):
        if column not in df.columns:
            return fallback

        values = df[column].dropna().astype(str).unique().tolist()
        values.sort()
        return values or fallback

    with st.form("housing_prediction_form"):
        st.markdown("##### Location and property type")
        c1, c2, c3 = st.columns(3)

        with c1:
            suburb = st.selectbox(
                "Suburb",
                category_options("Suburb", ["Unknown"]),
            )
            region = st.selectbox(
                "Region",
                category_options("Regionname", ["Unknown"]),
            )
            postcode_options = category_options(
                "Postcode", ["Unknown"]
            )
            postcode = st.selectbox("Postcode", postcode_options)

        with c2:
            property_type = st.selectbox(
                "Property type",
                category_options("Type", ["Unknown"]),
            )
            council = st.selectbox(
                "Council area",
                category_options("CouncilArea", ["Unknown"]),
            )
            seller = st.selectbox(
                "Seller",
                category_options("SellerG", ["Unknown"]),
            )

        with c3:
            method = st.selectbox(
                "Sale method",
                category_options("Method", ["Unknown"]),
            )
            region_again = region
            parking_area = st.selectbox(
                "Parking area",
                category_options("ParkingArea", ["Unknown"]),
            )

        st.markdown("##### Property characteristics")
        c1, c2, c3 = st.columns(3)

        with c1:
            rooms = st.number_input("Rooms", 1, 20, 3)
            bedrooms = st.number_input("Bedrooms", 0, 20, 3)
            bathrooms = st.number_input("Bathrooms", 0, 20, 2)
            car_spaces = st.number_input("Car spaces", 0, 20, 1)

        with c2:
            distance = st.number_input(
                "Distance from city (km)", 0.0, 200.0, 10.0
            )
            land_size = st.number_input(
                "Land size (m²)", 0.0, 100000.0, 300.0
            )
            building_area = st.number_input(
                "Building area (m²)", 0.0, 10000.0, 120.0
            )
            year_built = st.number_input(
                "Year built", 1800, 2026, 2000
            )

        with c3:
            sale_year = st.number_input(
                "Sale year", 2016, 2035, 2017
            )
            latitude = st.number_input(
                "Latitude", -45.0, -35.0, -37.81, format="%.5f"
            )
            longitude = st.number_input(
                "Longitude", 140.0, 155.0, 144.96, format="%.5f"
            )
            property_count = st.number_input(
                "Properties in area", 0, 100000, 5000
            )

        model_name = st.selectbox(
            "Regression model",
            list(MODEL_FILES.keys()),
        )

        submitted = st.form_submit_button(
            "Predict property price",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        property_age = sale_year - year_built

        if property_age < 0:
            st.error("Sale year cannot be earlier than the year built.")
        else:
            raw_row = pd.DataFrame([{
                "Rooms": rooms,
                "Distance": distance,
                "Bedroom": bedrooms,
                "Bathroom": bathrooms,
                "Car": car_spaces,
                "Landsize": land_size,
                "BuildingArea": building_area,
                "YearBuilt": year_built,
                "Latitude": latitude,
                "Longtitude": longitude,
                "Propertycount": property_count,
                "PropertyAge": property_age,
                "Suburb": suburb,
                "Type": property_type,
                "Method": method,
                "SellerG": seller,
                "Postcode": postcode,
                "CouncilArea": council,
                "Regionname": region,
                "ParkingArea": parking_area,
            }])

            try:
                with st.spinner("Generating prediction..."):
                    price = predict_price(model_name, raw_row)

                if not np.isfinite(price):
                    st.error("The model returned an invalid prediction.")
                else:
                    st.success("Prediction generated successfully")
                    st.metric(
                        "Estimated property price",
                        f"A${price:,.0f}",
                    )
                    st.caption(
                        f"Model: {model_name} · "
                        "This is a model estimate, not a property valuation."
                    )

            except Exception as exc:
                st.error(f"Prediction failed: {exc}")
                st.info(
                    "No model files were modified. Share the full error "
                    "so we can fix the specific artifact or input issue."
                )
