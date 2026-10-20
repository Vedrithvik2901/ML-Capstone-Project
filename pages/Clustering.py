
from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

from utils.layout import render_sidebar

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Clustering | ML Capstone Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

st.title("🔍 Customer Segmentation")
st.caption(
    "Explore customer purchasing behaviour using K-Means "
    "and Agglomerative Clustering on the Online Retail dataset."
)

# ---------------------------------------------------------
# PATHS AND CONSTANTS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clustering" / "Online Retail.xlsx"
MODELS_DIR = BASE_DIR / "models"

KMEANS_PATH = MODELS_DIR / "kmeans_clustering.joblib"
AGGLOMERATIVE_PATH = MODELS_DIR / "agglomerative_clustering.joblib"

FEATURE_COLUMNS = [
    "Frequency",
    "Monetary",
    "AverageOrderValue",
    "UniqueProducts",
]


# ---------------------------------------------------------
# LOAD AND CLEAN DATA
# ---------------------------------------------------------
@st.cache_data(show_spinner="Loading and preparing Online Retail data...")
def load_customer_data(file_path, file_mtime):
    """Clean transaction data and construct customer-level features."""
    del file_mtime  # Used as part of the cache key.

    df = pd.read_excel(file_path)
    original_rows = len(df)

    # Remove duplicate transactions.
    retail = df.drop_duplicates().copy()
    after_duplicates = len(retail)

    # CustomerID is required for customer-level aggregation.
    retail = retail.dropna(subset=["CustomerID"]).copy()
    after_missing_customers = len(retail)

    retail["CustomerID"] = retail["CustomerID"].astype(int)
    retail["InvoiceDate"] = pd.to_datetime(retail["InvoiceDate"])

    # Remove cancelled invoices.
    retail = retail[
        ~retail["InvoiceNo"].astype(str).str.startswith("C")
    ].copy()
    after_cancellations = len(retail)

    # Remove invalid quantities and prices.
    retail = retail[
        (retail["Quantity"] > 0) & (retail["UnitPrice"] > 0)
    ].copy()

    retail["Sales"] = retail["Quantity"] * retail["UnitPrice"]

    # Aggregate transactions into customer-level features.
    customer_features = retail.groupby("CustomerID").agg(
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Sales", "sum"),
        UniqueProducts=("StockCode", "nunique"),
    )

    customer_features["AverageOrderValue"] = (
        customer_features["Monetary"]
        / customer_features["Frequency"]
    )

    customer_features = customer_features[FEATURE_COLUMNS]
    customer_features = customer_features.replace(
        [np.inf, -np.inf], np.nan
    ).dropna()

    customer_features = customer_features[
        (customer_features > 0).all(axis=1)
    ].copy()

    cleaning_summary = {
        "Original transactions": original_rows,
        "After removing duplicates": after_duplicates,
        "After removing missing CustomerIDs": after_missing_customers,
        "After removing cancelled invoices": after_cancellations,
        "Valid customer records": len(customer_features),
        "Customers": customer_features.shape[0],
    }

    # Match the notebook's transformation pipeline.
    X_log = np.log1p(customer_features)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)

    return (
        df,
        retail,
        customer_features,
        X_log,
        X_scaled,
        scaler,
        cleaning_summary,
    )


# ---------------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_models(kmeans_path, agglomerative_path):
    """Load the saved clustering models."""
    models = {}

    if Path(kmeans_path).exists():
        models["K-Means"] = joblib.load(kmeans_path)

    if Path(agglomerative_path).exists():
        models["Agglomerative"] = joblib.load(agglomerative_path)

    return models


# ---------------------------------------------------------
# CLUSTER ASSIGNMENTS AND METRICS
# ---------------------------------------------------------
@st.cache_data(show_spinner="Calculating customer clusters...")
def calculate_clusters(X_scaled, _model, model_name):
    """Generate cluster labels for the supplied customer dataset."""
    if model_name == "K-Means":
        labels = _model.predict(X_scaled)
    else:
        # AgglomerativeClustering has no predict() method.
        # Refit on the same customer dataset to obtain labels.
        labels = AgglomerativeClustering(
            n_clusters=3,
            linkage="ward",
        ).fit_predict(X_scaled)

    labels = np.asarray(labels)
    unique_labels = np.unique(labels)

    if len(unique_labels) < 2 or len(unique_labels) >= len(labels):
        metrics = {
            "Silhouette Score": np.nan,
            "Davies-Bouldin Index": np.nan,
            "Calinski-Harabasz Score": np.nan,
        }
    else:
        metrics = {
            "Silhouette Score": silhouette_score(X_scaled, labels),
            "Davies-Bouldin Index": davies_bouldin_score(
                X_scaled, labels
            ),
            "Calinski-Harabasz Score": calinski_harabasz_score(
                X_scaled, labels
            ),
        }

    return labels, metrics


def format_number(value):
    """Format numeric values for display."""
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"


# ---------------------------------------------------------
# CHECK REQUIRED FILES
# ---------------------------------------------------------
if not DATA_PATH.exists():
    st.error(f"Dataset not found: `{DATA_PATH}`")
    st.info(
        "Ensure `Online Retail.xlsx` is inside "
        "`data/clustering/`."
    )
    st.stop()

try:
    (
        raw_df,
        retail_df,
        customer_features,
        X_log,
        X_scaled,
        scaler,
        cleaning_summary,
    ) = load_customer_data(
        str(DATA_PATH),
        DATA_PATH.stat().st_mtime,
    )
except Exception as exc:
    st.error(f"Could not load or preprocess the dataset: {exc}")
    st.stop()

try:
    models = load_models(str(KMEANS_PATH), str(AGGLOMERATIVE_PATH))
except Exception as exc:
    st.error(f"Could not load the saved clustering models: {exc}")
    st.stop()

if not models:
    st.error(
        "No clustering models were found. Expected model files:\n\n"
        "- `models/kmeans_clustering.joblib`\n"
        "- `models/agglomerative_clustering.joblib`"
    )
    st.stop()

# The saved artifacts were trained with four customer-level features.
for model_name, model in models.items():
    expected_features = getattr(model, "n_features_in_", 4)
    if expected_features != len(FEATURE_COLUMNS):
        st.error(
            f"{model_name} expects {expected_features} features, "
            f"but this page creates {len(FEATURE_COLUMNS)}. "
            "Check the model's training preprocessing."
        )
        st.stop()

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
overview_tab, explore_tab, analysis_tab, segmentation_tab = st.tabs(
    [
        "📌 Overview",
        "📊 Explore Data",
        "📈 Cluster Analysis",
        "👥 Customer Segmentation",
    ]
)

# ---------------------------------------------------------
# TAB 1: OVERVIEW
# ---------------------------------------------------------
with overview_tab:
    st.subheader("Project Overview")

    st.write(
        """
        Customer segmentation groups customers with similar purchasing
        behaviour. Instead of assigning predefined labels, clustering
        algorithms discover patterns in customer-level data.

        This project uses the **Online Retail** transaction dataset.
        Transaction records are cleaned and aggregated into four
        customer-level features before clustering.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Original Transactions", f"{len(raw_df):,}")

    with col2:
        st.metric("Customers Analysed", f"{len(customer_features):,}")

    with col3:
        st.metric("Customer Features", len(FEATURE_COLUMNS))

    st.markdown("#### Algorithms")

    left, right = st.columns(2)

    with left:
        st.markdown("**K-Means Clustering**")
        st.write(
            "Partitions customers into a predefined number of clusters "
            "by minimising within-cluster squared distances. The saved "
            "model can assign a new transformed customer profile."
        )

    with right:
        st.markdown("**Agglomerative Clustering**")
        st.write(
            "Builds clusters hierarchically by repeatedly merging "
            "groups. The saved estimator does not provide a direct "
            "`predict()` method for unseen customers."
        )

    st.markdown("#### Features used")

    feature_descriptions = pd.DataFrame(
        {
            "Feature": FEATURE_COLUMNS,
            "Meaning": [
                "Number of distinct invoices for a customer",
                "Total sales value associated with the customer",
                "Monetary value divided by invoice frequency",
                "Number of distinct products purchased",
            ],
        }
    )
    st.dataframe(feature_descriptions, use_container_width=True, hide_index=True)

    st.markdown("#### Data cleaning summary")
    summary_df = pd.DataFrame(
        list(cleaning_summary.items()),
        columns=["Step", "Row / customer count"],
    )
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.caption(
        "Preprocessing follows the notebook's duplicate removal, "
        "CustomerID filtering, cancellation removal, positive quantity "
        "and price filtering, customer aggregation, log1p transformation, "
        "and StandardScaler steps."
    )


# ---------------------------------------------------------
# TAB 2: EXPLORE DATA
# ---------------------------------------------------------
with explore_tab:
    st.subheader("Explore the Customer Dataset")

    st.write(
        "Each row below represents a customer rather than an individual "
        "transaction."
    )

    st.markdown("#### Customer feature sample")
    st.dataframe(
        customer_features.head(100),
        use_container_width=True,
    )

    st.markdown("#### Descriptive statistics")
    st.dataframe(
        customer_features.describe().T,
        use_container_width=True,
    )

    st.markdown("#### Feature distributions")

    selected_feature = st.selectbox(
        "Choose a feature",
        FEATURE_COLUMNS,
        key="explore_feature",
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(
        customer_features[selected_feature],
        bins=40,
        edgecolor="black",
    )
    ax.set_title(f"Distribution of {selected_feature}")
    ax.set_xlabel(selected_feature)
    ax.set_ylabel("Number of customers")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Correlation between customer features")
    corr = customer_features.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    image = ax.imshow(corr, aspect="auto", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    ax.set_title("Feature Correlation Matrix")
    fig.colorbar(image, ax=ax, label="Correlation")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Transformed features")
    st.write(
        "The notebook applies `log1p` to reduce skew, followed by "
        "`StandardScaler` so that features with large numeric ranges "
        "do not dominate distance calculations."
    )

    transformed_df = pd.DataFrame(
        X_scaled,
        columns=FEATURE_COLUMNS,
        index=customer_features.index,
    )
    st.dataframe(transformed_df.head(20), use_container_width=True)


# ---------------------------------------------------------
# TAB 3: CLUSTER ANALYSIS
# ---------------------------------------------------------
with analysis_tab:
    st.subheader("Cluster Analysis")

    model_names = list(models.keys())
    selected_model_name = st.selectbox(
        "Select clustering algorithm",
        model_names,
        key="analysis_model",
    )
    selected_model = models[selected_model_name]

    try:
        labels, metrics = calculate_clusters(
            X_scaled,
            selected_model,
            selected_model_name,
        )
    except Exception as exc:
        st.error(f"Could not generate clusters: {exc}")
        st.stop()

    labelled_df = customer_features.copy()
    labelled_df["Cluster"] = labels

    st.markdown("#### Evaluation metrics")

    m1, m2, m3 = st.columns(3)
    m1.metric("Silhouette Score", format_number(metrics["Silhouette Score"]))
    m2.metric(
        "Davies-Bouldin Index",
        format_number(metrics["Davies-Bouldin Index"]),
    )
    m3.metric(
        "Calinski-Harabasz Score",
        format_number(metrics["Calinski-Harabasz Score"]),
    )

    with st.expander("How to interpret these metrics"):
        st.markdown(
            """
            - **Silhouette Score:** ranges from -1 to 1; higher values
              generally indicate better separation and cohesion.
            - **Davies-Bouldin Index:** lower values generally indicate
              better-separated clusters.
            - **Calinski-Harabasz Score:** higher values generally indicate
              more separation between clusters relative to within-cluster
              dispersion.

            These metrics evaluate the generated assignments on the
            current preprocessed customer dataset. They do not by
            themselves prove that a segmentation is commercially useful.
            """
        )

    st.markdown("#### Number of customers in each cluster")
    cluster_counts = (
        labelled_df["Cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("Cluster")
        .reset_index(name="Customers")
    )
    st.dataframe(cluster_counts, use_container_width=True, hide_index=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(
        cluster_counts["Cluster"].astype(str),
        cluster_counts["Customers"],
    )
    ax.set_title(f"{selected_model_name}: Cluster Sizes")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Number of customers")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### PCA visualisation")

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    plot_df = pd.DataFrame(
        {
            "PC1": X_pca[:, 0],
            "PC2": X_pca[:, 1],
            "Cluster": labels.astype(str),
        },
        index=customer_features.index,
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    for cluster in sorted(plot_df["Cluster"].unique()):
        subset = plot_df[plot_df["Cluster"] == cluster]
        ax.scatter(
            subset["PC1"],
            subset["PC2"],
            label=f"Cluster {cluster}",
            alpha=0.65,
            s=18,
        )

    ax.set_title(f"{selected_model_name}: PCA Cluster Projection")
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    explained_variance = pca.explained_variance_ratio_.sum() * 100
    st.caption(
        f"The first two principal components explain "
        f"{explained_variance:.2f}% of the variance in the scaled data. "
        "The plot is a two-dimensional projection of four-dimensional data."
    )

    st.markdown("#### Cluster profiles")
    profile = labelled_df.groupby("Cluster")[FEATURE_COLUMNS].median()
    st.dataframe(profile, use_container_width=True)

    st.markdown("#### Browse assigned customers")
    labelled_display = labelled_df.reset_index()
    labelled_display = labelled_display.rename(
        columns={labelled_display.columns[0]: "CustomerID"}
    )
    st.dataframe(
        labelled_display.head(200),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# TAB 4: CUSTOMER SEGMENTATION
# ---------------------------------------------------------
with segmentation_tab:
    st.subheader("Customer Segmentation")

    st.write(
        "Inspect an existing customer and view their purchasing "
        "characteristics alongside the cluster assignment."
    )

    segmentation_model_name = st.selectbox(
        "Select algorithm",
        list(models.keys()),
        key="segmentation_model",
    )
    segmentation_model = models[segmentation_model_name]

    try:
        segmentation_labels, _ = calculate_clusters(
            X_scaled,
            segmentation_model,
            segmentation_model_name,
        )
    except Exception as exc:
        st.error(f"Could not assign clusters: {exc}")
        st.stop()

    segmentation_df = customer_features.copy()
    segmentation_df["Cluster"] = segmentation_labels

    customer_ids = segmentation_df.index.astype(str).tolist()
    selected_customer_id = st.selectbox(
        "Choose a CustomerID",
        customer_ids,
        key="selected_customer",
    )

    selected_customer = int(selected_customer_id)
    customer_row = segmentation_df.loc[selected_customer]
    customer_cluster = int(customer_row["Cluster"])

    st.markdown(f"#### Customer {selected_customer}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Assigned Cluster", str(customer_cluster))
    c2.metric("Invoice Frequency", f"{customer_row['Frequency']:,.0f}")
    c3.metric("Total Monetary Value", f"{customer_row['Monetary']:,.2f}")
    c4.metric(
        "Unique Products",
        f"{customer_row['UniqueProducts']:,.0f}",
    )

    st.metric(
        "Average Order Value",
        f"{customer_row['AverageOrderValue']:,.2f}",
    )

    st.markdown("#### Selected customer's features")
    st.dataframe(
        customer_row[FEATURE_COLUMNS].to_frame("Value"),
        use_container_width=True,
    )

    st.markdown("#### Compare with the assigned cluster")
    cluster_customers = segmentation_df[
        segmentation_df["Cluster"] == customer_cluster
    ]

    comparison = pd.DataFrame(
        {
            "Selected customer": customer_row[FEATURE_COLUMNS],
            "Cluster median": cluster_customers[FEATURE_COLUMNS].median(),
            "Overall median": customer_features[FEATURE_COLUMNS].median(),
        }
    )
    st.dataframe(comparison, use_container_width=True)

    st.markdown("#### Cluster interpretation guide")

    st.write(
        """
        Use the feature values and cluster medians to interpret the
        segment. These are data-driven groups, not predefined labels.
        For example, a cluster with higher monetary value and frequency
        may contain more valuable or frequent customers, while a cluster
        with lower values may represent less active customers.

        Interpret each cluster from its actual profile rather than
        assuming that a particular cluster number always means the same
        thing.
        """
    )

    st.markdown("#### Try a new customer profile with K-Means")

    st.caption(
        "This prediction is available only with K-Means. The profile is "
        "transformed using log1p and the scaler fitted to the current "
        "cleaned customer dataset."
    )

    if "K-Means" not in models:
        st.info("The K-Means model is not available.")
    else:
        with st.form("new_customer_form"):
            frequency = st.number_input(
                "Number of distinct invoices",
                min_value=1,
                value=3,
                step=1,
            )
            monetary = st.number_input(
                "Total monetary value",
                min_value=0.01,
                value=500.0,
                step=50.0,
            )
            average_order_value = st.number_input(
                "Average order value",
                min_value=0.01,
                value=monetary / frequency,
                step=10.0,
            )
            unique_products = st.number_input(
                "Number of unique products",
                min_value=1,
                value=10,
                step=1,
            )

            submitted = st.form_submit_button("Predict K-Means Cluster")

        if submitted:
            new_profile = pd.DataFrame(
                [
                    {
                        "Frequency": frequency,
                        "Monetary": monetary,
                        "AverageOrderValue": average_order_value,
                        "UniqueProducts": unique_products,
                    }
                ],
                columns=FEATURE_COLUMNS,
            )

            new_log = np.log1p(new_profile)
            new_scaled = scaler.transform(new_log)

            try:
                new_cluster = models["K-Means"].predict(new_scaled)[0]
                st.success(
                    f"The new customer profile is assigned to "
                    f"**Cluster {new_cluster}** by K-Means."
                )
                st.dataframe(new_profile, use_container_width=True)
            except Exception as exc:
                st.error(f"Could not predict the cluster: {exc}")

    st.info(
        "Agglomerative Clustering does not support direct prediction for "
        "a new customer. Its assignments above are generated by fitting "
        "the clustering algorithm to the existing cleaned customer data."
    )

st.divider()
st.caption(
    "ML Capstone Explorer | Customer Segmentation | "
    "Online Retail Dataset"
)
