
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from utils.layout import render_sidebar

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

st.set_page_config(
    page_title="Visualizations | ML Capstone Project",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #111318;
        color: #f3f4f6;
    }

    .viz-hero {
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #303540;
        border-radius: 18px;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(163, 230, 53, 0.10),
                transparent 35%
            ),
            #1b1e25;
    }

    .viz-eyebrow {
        color: #a3e635;
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.14em;
    }

    .viz-hero h1 {
        margin: 0.6rem 0;
        font-size: clamp(2rem, 4vw, 3rem);
        letter-spacing: -0.04em;
    }

    .viz-hero p {
        max-width: 760px;
        color: #a0a6b4;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background: #1b1e25;
        border: 1px solid #303540;
        border-radius: 12px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Dataset loaders
# --------------------------------------------------
@st.cache_data
def load_housing(path, modified):
    del modified
    return pd.read_csv(path)


@st.cache_data
def load_bank(path, modified):
    del modified
    df = pd.read_csv(path, sep=";")
    if len(df.columns) == 1:
        df = pd.read_csv(path)
    return df


@st.cache_data
def load_retail(path, modified):
    del modified
    return pd.read_excel(path)


def find_dataset(folder, filename):
    path = DATA_DIR / folder / filename
    return path if path.exists() else None


housing_path = find_dataset("regression", "Melbourne_housing.csv")
bank_path = find_dataset("classification", "bank-full.csv")
retail_path = find_dataset("clustering", "Online Retail.xlsx")

st.markdown(
    """
    <div class="viz-hero">
        <div class="viz-eyebrow">DATA EXPLORATION</div>
        <h1>Visualizations & Insights</h1>
        <p>
            Explore the datasets behind the three machine learning tracks.
            Use the charts to understand distributions, compare categories,
            and discover patterns before interpreting model results.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

available = []
if housing_path:
    available.append("Regression · Melbourne Housing")
if bank_path:
    available.append("Classification · Bank Marketing")
if retail_path:
    available.append("Clustering · Online Retail")

if not available:
    st.error(
        "No supported datasets were found. Check the files under "
        "`data/regression`, `data/classification`, and `data/clustering`."
    )
    st.stop()

selected = st.selectbox("Choose a dataset", available)

# --------------------------------------------------
# Regression visualizations
# --------------------------------------------------
if selected == "Regression · Melbourne Housing":
    try:
        df = load_housing(
            str(housing_path), housing_path.stat().st_mtime
        )
    except Exception as exc:
        st.error(f"Could not load the housing dataset: {exc}")
        st.stop()

    if "Price" not in df.columns:
        st.error("The housing dataset does not contain a Price column.")
        st.stop()

    prices = pd.to_numeric(df["Price"], errors="coerce").dropna()
    prices = prices[prices > 0]

    st.subheader("Melbourne Housing")
    st.caption(
        "Explore property-price distributions and how prices vary "
        "across available property categories."
    )

    a, b, c = st.columns(3)
    a.metric("Properties with valid prices", f"{len(prices):,}")
    b.metric("Median price", f"A${prices.median():,.0f}")
    c.metric("Mean price", f"A${prices.mean():,.0f}")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Property price distribution")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(prices, bins=40, edgecolor="black", alpha=0.85)
        ax.set_xlabel("Price (AUD)")
        ax.set_ylabel("Number of properties")
        ax.set_title("Distribution of property prices")
        ax.ticklabel_format(style="plain", axis="x")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.markdown("#### Price by property type")
        if "Type" in df.columns:
            chart_df = pd.DataFrame(
                {
                    "Type": df["Type"],
                    "Price": pd.to_numeric(df["Price"], errors="coerce"),
                }
            ).dropna()
            chart_df = chart_df[chart_df["Price"] > 0]
            grouped = (
                chart_df.groupby("Type")["Price"]
                .median()
                .sort_values(ascending=False)
            )
            st.bar_chart(grouped)
        else:
            st.info("The dataset has no Type column.")

    st.markdown("#### Explore a numeric feature")
    numeric_columns = [
        col for col in df.select_dtypes(include=np.number).columns
        if col != "Price"
    ]

    if numeric_columns:
        feature = st.selectbox(
            "Select a feature to compare with price",
            numeric_columns,
        )
        plot_df = pd.DataFrame(
            {
                feature: pd.to_numeric(df[feature], errors="coerce"),
                "Price": pd.to_numeric(df["Price"], errors="coerce"),
            }
        ).dropna()

        if len(plot_df) > 5000:
            plot_df = plot_df.sample(5000, random_state=42)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.scatter(plot_df[feature], plot_df["Price"], alpha=0.35, s=12)
        ax.set_xlabel(feature)
        ax.set_ylabel("Price (AUD)")
        ax.set_title(f"{feature} vs property price")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


    # Additional housing visualizations

    st.divider()
    st.markdown("### More Housing Insights")

    left, right = st.columns(2)

    # 1. Price by number of rooms
    with left:
        if "Rooms" in df.columns:
            st.markdown("#### Median Price by Number of Rooms")

            room_prices = df[["Rooms", "Price"]].copy()
            room_prices["Price"] = pd.to_numeric(
                room_prices["Price"], errors="coerce"
            )
            room_prices = room_prices.dropna()
            room_prices = room_prices[room_prices["Price"] > 0]

            room_prices = room_prices.groupby("Rooms")["Price"].median()

            st.bar_chart(room_prices)
        else:
            st.info("Rooms column unavailable.")

    # 2. Price by region or suburb
    with right:
        location_col = next(
            (c for c in ["Regionname", "Suburb", "CouncilArea"]
             if c in df.columns),
            None
        )

        if location_col:
            st.markdown("#### Median Price by Location")

            location_data = df[[location_col, "Price"]].copy()
            location_data["Price"] = pd.to_numeric(
                location_data["Price"], errors="coerce"
            )
            location_data = location_data.dropna()

            top_locations = (
                location_data.groupby(location_col)["Price"]
                .median()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(top_locations)
        else:
            st.info("No location column available.")

    # 3. Property-type price spread
    if "Type" in df.columns:
        st.markdown("#### Price Spread by Property Type")

        box_data = df[["Type", "Price"]].copy()
        box_data["Price"] = pd.to_numeric(
            box_data["Price"], errors="coerce"
        )
        box_data = box_data.dropna()
        box_data = box_data[box_data["Price"] > 0]

        types = sorted(box_data["Type"].astype(str).unique())

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.boxplot(
            [
                box_data.loc[
                    box_data["Type"].astype(str) == t, "Price"
                ].values
                for t in types
            ],
            labels=types,
            showfliers=False
        )
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Price (AUD)")
        ax.set_title("Property Price Spread")
        ax.ticklabel_format(style="plain", axis="y")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 4. Correlation heatmap
    st.markdown("#### Numeric Feature Correlations")

    numeric_df = df.select_dtypes(include=np.number).copy()
    numeric_df = numeric_df.dropna(axis=1, how="all")

    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(10, 7))
        image = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(
            corr.columns, rotation=70, ha="right"
        )
        ax.set_yticks(range(len(corr.columns)))
        ax.set_yticklabels(corr.columns)

        ax.set_title("Housing Feature Correlation Heatmap")
        fig.colorbar(image, ax=ax, label="Correlation")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 5. Missing values
    st.markdown("#### Data Quality: Missing Values")

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False).head(15)

    if not missing.empty:
        st.bar_chart(missing)
    else:
        st.success("No missing values found.")


# --------------------------------------------------
# Classification visualizations
# --------------------------------------------------
elif selected == "Classification · Bank Marketing":
    try:
        df = load_bank(str(bank_path), bank_path.stat().st_mtime)
    except Exception as exc:
        st.error(f"Could not load the bank dataset: {exc}")
        st.stop()

    st.subheader("Bank Marketing")
    st.caption(
        "Explore subscription outcomes and the distribution of customer "
        "characteristics in the marketing dataset."
    )

    if "y" not in df.columns:
        st.error("The bank dataset does not contain the expected target 'y'.")
        st.stop()

    target = df["y"].astype(str).str.lower().str.strip()
    target_counts = target.value_counts()

    a, b, c = st.columns(3)
    a.metric("Customer records", f"{len(df):,}")
    b.metric("Target classes", f"{target.nunique():,}")
    c.metric(
        "Subscription rate",
        f"{(target == 'yes').mean() * 100:.1f}%",
    )

    left, right = st.columns(2)

    with left:
        st.markdown("#### Subscription class balance")
        st.bar_chart(target_counts)

    with right:
        st.markdown("#### Subscription rate by category")
        categorical_columns = [
            col for col in df.select_dtypes(include="object").columns
            if col not in {"y"}
        ]

        if categorical_columns:
            category = st.selectbox(
                "Choose a customer attribute",
                categorical_columns,
            )
            group_df = pd.DataFrame(
                {
                    "Category": df[category].fillna("Missing").astype(str),
                    "Subscribed": (target == "yes").astype(int),
                }
            )

            # Limit the chart to the most frequent categories.
            top_categories = (
                group_df["Category"]
                .value_counts()
                .head(12)
                .index
            )
            group_df = group_df[
                group_df["Category"].isin(top_categories)
            ]

            rates = (
                group_df.groupby("Category")["Subscribed"]
                .mean()
                .mul(100)
                .sort_values(ascending=False)
            )
            st.bar_chart(rates)
            st.caption("Values show the subscription rate within each category.")
        else:
            st.info("No categorical features were found.")

    st.markdown("#### Numeric feature distribution")
    numeric_columns = list(df.select_dtypes(include=np.number).columns)

    if numeric_columns:
        feature = st.selectbox(
            "Choose a numeric feature",
            numeric_columns,
            key="bank_numeric",
        )
        values = pd.to_numeric(df[feature], errors="coerce").dropna()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.hist(values, bins=35, edgecolor="black", alpha=0.85)
        ax.set_title(f"Distribution of {feature}")
        ax.set_xlabel(feature)
        ax.set_ylabel("Customer records")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


    # Additional classification visualizations

    st.divider()
    st.markdown("### Customer and Campaign Insights")

    # 1. Subscription rate by age group
    if "age" in df.columns:
        st.markdown("#### Subscription Rate by Age Group")

        age_data = pd.DataFrame({
            "Age": pd.to_numeric(df["age"], errors="coerce"),
            "Subscribed": (target == "yes").astype(int)
        }).dropna()

        age_bins = [0, 25, 35, 45, 55, 65, 120]
        age_labels = [
            "25 and below", "26–35", "36–45",
            "46–55", "56–65", "Above 65"
        ]

        age_data["Age Group"] = pd.cut(
            age_data["Age"],
            bins=age_bins,
            labels=age_labels
        )

        age_rates = (
            age_data.groupby("Age Group", observed=False)["Subscribed"]
            .mean()
            .mul(100)
        )

        st.bar_chart(age_rates)
        st.caption(
            "Shows the percentage of customers subscribing within each age group."
        )

    left, right = st.columns(2)

    # 2. Contact method
    with left:
        if "contact" in df.columns:
            st.markdown("#### Subscription Rate by Contact Method")

            contact_data = pd.DataFrame({
                "Contact": df["contact"].fillna("Missing"),
                "Subscribed": (target == "yes").astype(int)
            })

            contact_rates = (
                contact_data.groupby("Contact")["Subscribed"]
                .mean()
                .mul(100)
                .sort_values(ascending=False)
            )

            st.bar_chart(contact_rates)

    # 3. Campaign contacts
    with right:
        if "campaign" in df.columns:
            st.markdown("#### Campaign Contact Distribution")

            campaign = pd.to_numeric(
                df["campaign"], errors="coerce"
            ).dropna()

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(campaign, bins=30, edgecolor="black")
            ax.set_xlabel("Number of contacts")
            ax.set_ylabel("Customers")
            ax.set_title("Contacts During This Campaign")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    # 4. Numeric feature correlation
    st.markdown("#### Numeric Feature Correlation Heatmap")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(10, 7))
        image = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(
            corr.columns, rotation=70, ha="right"
        )
        ax.set_yticks(range(len(corr.columns)))
        ax.set_yticklabels(corr.columns)

        ax.set_title("Bank Marketing Correlation Heatmap")
        fig.colorbar(image, ax=ax, label="Correlation")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 5. Compare a numeric feature across target classes
    numeric_cols = list(
        df.select_dtypes(include=np.number).columns
    )

    if numeric_cols:
        st.markdown("#### Feature Distribution by Subscription Outcome")

        selected_feature = st.selectbox(
            "Select a feature to compare",
            numeric_cols,
            key="classification_outcome_feature"
        )

        plot_data = pd.DataFrame({
            "Feature": pd.to_numeric(
                df[selected_feature], errors="coerce"
            ),
            "Outcome": target
        }).dropna()

        outcomes = sorted(plot_data["Outcome"].unique())

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.boxplot(
            [
                plot_data.loc[
                    plot_data["Outcome"] == outcome, "Feature"
                ].values
                for outcome in outcomes
            ],
            labels=outcomes,
            showfliers=False
        )
        ax.set_xlabel("Subscription Outcome")
        ax.set_ylabel(selected_feature)
        ax.set_title(f"{selected_feature} by Subscription Outcome")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


# --------------------------------------------------
# Clustering visualizations
# --------------------------------------------------
else:
    try:
        df = load_retail(str(retail_path), retail_path.stat().st_mtime)
    except Exception as exc:
        st.error(f"Could not load the Online Retail dataset: {exc}")
        st.stop()

    st.subheader("Online Retail")
    st.caption(
        "Explore sales patterns, country-level activity, and "
        "customer purchasing behaviour."
    )

    required = {
        "InvoiceNo", "StockCode", "Quantity", "UnitPrice",
        "InvoiceDate", "CustomerID", "Country",
    }
    missing = required - set(df.columns)

    if missing:
        st.error("Missing expected columns: " + ", ".join(sorted(missing)))
        st.stop()

    retail = df.drop_duplicates().copy()
    retail = retail.dropna(subset=["CustomerID"]).copy()
    retail["CustomerID"] = retail["CustomerID"].astype(int)
    retail["InvoiceDate"] = pd.to_datetime(
        retail["InvoiceDate"], errors="coerce"
    )
    retail = retail[
        ~retail["InvoiceNo"].astype(str).str.startswith("C")
    ].copy()
    retail = retail[
        (retail["Quantity"] > 0) & (retail["UnitPrice"] > 0)
    ].copy()
    retail["Sales"] = retail["Quantity"] * retail["UnitPrice"]

    a, b, c = st.columns(3)
    a.metric("Valid transactions", f"{len(retail):,}")
    b.metric("Unique customers", f"{retail['CustomerID'].nunique():,}")
    c.metric("Total sales", f"{retail['Sales'].sum():,.2f}")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Monthly sales trend")
        monthly = (
            retail.dropna(subset=["InvoiceDate"])
            .set_index("InvoiceDate")["Sales"]
            .resample("MS")
            .sum()
        )
        st.line_chart(monthly)
        st.caption("Monthly sales are calculated from positive quantities and prices.")

    with right:
        st.markdown("#### Top countries by sales")
        country_sales = (
            retail.groupby("Country")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(country_sales)


    # Additional retail visualizations

    st.divider()
    st.markdown("### Retail Sales Insights")

    left, right = st.columns(2)

    # 1. Monthly order volume
    with left:
        st.markdown("#### Monthly Order Volume")

        monthly_orders = (
            retail.dropna(subset=["InvoiceDate"])
            .set_index("InvoiceDate")["InvoiceNo"]
            .resample("MS")
            .nunique()
        )

        st.line_chart(monthly_orders)

    # 2. Top products by sales
    with right:
        st.markdown("#### Top Products by Sales")

        product_sales = (
            retail.groupby("Description")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
        )

        st.bar_chart(product_sales)

    left, right = st.columns(2)

    # 3. Countries by order count
    with left:
        st.markdown("#### Orders by Country")

        country_orders = (
            retail.groupby("Country")["InvoiceNo"]
            .nunique()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
        )

        st.bar_chart(country_orders)

    # 4. Quantity distribution
    with right:
        st.markdown("#### Quantity per Transaction Line")

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(
            retail["Quantity"],
            bins=40,
            edgecolor="black"
        )
        ax.set_xlabel("Quantity")
        ax.set_ylabel("Transaction lines")
        ax.set_title("Distribution of Purchased Quantities")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 5. Customer recency
    st.markdown("#### Customer Recency")

    customer_last_purchase = retail.groupby("CustomerID")[
        "InvoiceDate"
    ].max()

    latest_date = retail["InvoiceDate"].max()

    recency_days = (
        latest_date - customer_last_purchase
    ).dt.days.dropna()

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(recency_days, bins=35, edgecolor="black")
    ax.set_xlabel("Days since last purchase")
    ax.set_ylabel("Customers")
    ax.set_title("Customer Recency Distribution")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # 6. Customer frequency versus monetary value
    st.markdown("#### Customer Frequency vs Spending")

    customer_summary = retail.groupby("CustomerID").agg(
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Sales", "sum")
    ).dropna()

    if len(customer_summary) > 5000:
        customer_summary = customer_summary.sample(
            5000, random_state=42
        )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(
        customer_summary["Frequency"],
        customer_summary["Monetary"],
        alpha=0.4,
        s=15
    )
    ax.set_xlabel("Number of distinct invoices")
    ax.set_ylabel("Total spending")
    ax.set_title("Customer Purchase Frequency vs Spending")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


    st.markdown("#### Customer purchasing behaviour")
    customers = retail.groupby("CustomerID").agg(
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Sales", "sum"),
        UniqueProducts=("StockCode", "nunique"),
    )
    customers["AverageOrderValue"] = (
        customers["Monetary"] / customers["Frequency"]
    )

    feature_columns = [
        "Frequency", "Monetary", "AverageOrderValue", "UniqueProducts"
    ]
    customers = customers[feature_columns].replace(
        [np.inf, -np.inf], np.nan
    ).dropna()
    customers = customers[(customers > 0).all(axis=1)]

    if len(customers) >= 3:
        X_scaled = StandardScaler().fit_transform(np.log1p(customers))
        X_pca = PCA(n_components=2, random_state=42).fit_transform(X_scaled)

        plot_df = pd.DataFrame(
            {"PC1": X_pca[:, 0], "PC2": X_pca[:, 1]},
            index=customers.index,
        )

        # Use saved K-Means if available; otherwise show the PCA projection.
        model_path = ROOT / "models" / "kmeans_clustering.joblib"

        if model_path.exists():
            try:
                import joblib
                model = joblib.load(model_path)
                if getattr(model, "n_features_in_", 4) == 4:
                    labels = model.predict(X_scaled)
                    plot_df["Cluster"] = labels.astype(str)
                else:
                    plot_df["Cluster"] = "Customers"
            except Exception:
                plot_df["Cluster"] = "Customers"
        else:
            plot_df["Cluster"] = "Customers"

        if len(plot_df) > 5000:
            plot_df = plot_df.sample(5000, random_state=42)

        fig, ax = plt.subplots(figsize=(9, 5))
        for label, group in plot_df.groupby("Cluster"):
            ax.scatter(
                group["PC1"],
                group["PC2"],
                s=16,
                alpha=0.6,
                label=f"Cluster {label}",
            )
        ax.set_title("Customer PCA projection")
        ax.set_xlabel("Principal Component 1")
        ax.set_ylabel("Principal Component 2")
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "PCA projects the four scaled customer features into two "
            "dimensions. Cluster labels are shown when the saved K-Means "
            "model can be loaded successfully."
        )
    else:
        st.info("Not enough valid customer records to create a PCA plot.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption("ML Capstone Project · 23CSE301")
