
from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import matplotlib.pyplot as plt


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Classification | ML Capstone Explorer",
    page_icon="🎯",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "classification" / "bank-full.csv"
MODEL_DIR = ROOT / "models"

RANDOM_STATE = 42
TEST_SIZE = 0.20

MODEL_FILES = {
    "Logistic Regression": "logistic_regression.joblib",
    "K-Nearest Neighbors": "knn.joblib",
    "Decision Tree": "decision_tree_classifier.joblib",
    "Gaussian Naive Bayes": "gaussian_nb.joblib",
    "Support Vector Machine": "svm.joblib",
    "Random Forest": "random_forest.joblib",
    "AdaBoost": "adaboost.joblib",
    "Gradient Boosting": "gradient_boosting_classifier.joblib",
    "Bagging Classifier": "bagging.joblib",
    "Multi-Layer Perceptron": "mlp_classifier.joblib",
}


# --------------------------------------------------
# Data and model loading
# --------------------------------------------------
@st.cache_data(show_spinner="Loading Bank Marketing dataset...")
def load_dataset():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH, sep=";")
    data.columns = data.columns.str.strip()

    # Match the feature engineering in classification.ipynb
    data["previously_contacted"] = (
        data["pdays"] != -1
    ).astype(int)

    if "y" not in data.columns:
        raise ValueError(
            "The dataset does not contain the target column 'y'."
        )

    data = data.dropna(subset=["y"]).copy()
    data["y"] = data["y"].astype(str).str.strip().str.lower()

    return data


@st.cache_resource(show_spinner="Loading saved classification models...")
def load_models():
    loaded = {}
    failures = {}

    for display_name, filename in MODEL_FILES.items():
        path = MODEL_DIR / filename

        if not path.exists():
            failures[display_name] = f"File not found: {filename}"
            continue

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                loaded[display_name] = joblib.load(path)
        except Exception as exc:
            failures[display_name] = str(exc)

    return loaded, failures


@st.cache_resource(show_spinner="Preparing evaluation data...")
def prepare_evaluation_data():
    data = load_dataset()

    X = data.drop(columns=["y", "y_numeric"], errors="ignore")
    y = data["y"]

    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    # Match the preprocessing strategy from the notebook.
    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", StandardScaler(), numerical_features),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return (
        X,
        y,
        numerical_features,
        categorical_features,
        preprocessor,
        X_test,
        y_test,
        X_test_processed,
    )


# --------------------------------------------------
# Load resources
# --------------------------------------------------
st.title("🎯 Classification Studio")
st.caption(
    "Explore the Bank Marketing dataset, compare saved classifiers, "
    "and predict whether a customer may subscribe to a term deposit."
)

try:
    df = load_dataset()
    (
        X,
        y,
        numerical_features,
        categorical_features,
        preprocessor,
        X_test,
        y_test,
        X_test_processed,
    ) = prepare_evaluation_data()
    models, model_failures = load_models()

except Exception as exc:
    st.error(f"Could not initialize the classification page: {exc}")
    st.stop()


if model_failures:
    with st.expander("Model loading warnings"):
        for model_name, error in model_failures.items():
            st.warning(f"**{model_name}:** {error}")

if not models:
    st.error("No classification models could be loaded from the models folder.")
    st.stop()


# --------------------------------------------------
# Dataset overview
# --------------------------------------------------
total_records = len(df)
yes_count = int((df["y"] == "yes").sum())
no_count = int((df["y"] == "no").sum())
yes_percentage = 100 * yes_count / total_records if total_records else 0

metric_cols = st.columns(4)
metric_cols[0].metric("Total customers", f"{total_records:,}")
metric_cols[1].metric("Input features", len(X.columns))
metric_cols[2].metric("Subscribed: Yes", f"{yes_count:,}")
metric_cols[3].metric("Positive class", f"{yes_percentage:.1f}%")

st.info(
    "The target is imbalanced: most customers did not subscribe. "
    "A useful classifier should be evaluated with precision, recall, "
    "F1-score, and a confusion matrix—not accuracy alone."
)

overview_tab, explore_tab, evaluate_tab, predict_tab = st.tabs(
    ["Overview", "Explore Data", "Evaluate Models", "Predict"]
)


# --------------------------------------------------
# Tab 1: Overview
# --------------------------------------------------
with overview_tab:
    st.subheader("About the dataset")

    st.write(
        "The Bank Marketing dataset contains information about customers "
        "contacted during a bank marketing campaign. The target column "
        "`y` indicates whether the customer subscribed to a term deposit."
    )

    left, right = st.columns(2)

    with left:
        st.markdown("**Target distribution**")
        target_counts = (
            df["y"]
            .value_counts()
            .reindex(["no", "yes"], fill_value=0)
            .rename_axis("Outcome")
            .reset_index(name="Customers")
        )
        st.bar_chart(target_counts, x="Outcome", y="Customers")

    with right:
        st.markdown("**Feature types**")
        feature_type_data = pd.DataFrame(
            {
                "Feature type": ["Numerical", "Categorical"],
                "Count": [
                    len(numerical_features),
                    len(categorical_features),
                ],
            }
        )
        st.bar_chart(feature_type_data, x="Feature type", y="Count")

    st.markdown("**Input features**")
    st.write(
        ", ".join(numerical_features + categorical_features)
    )

    with st.expander("Preview the dataset"):
        st.dataframe(df.head(20), use_container_width=True)

    with st.expander("Dataset statistics"):
        st.dataframe(df.describe(include="all").T, use_container_width=True)


# --------------------------------------------------
# Tab 2: Explore data
# --------------------------------------------------
with explore_tab:
    st.subheader("Explore individual features")

    all_features = numerical_features + categorical_features
    selected_feature = st.selectbox(
        "Choose a feature",
        all_features,
        key="explore_feature",
    )

    if selected_feature in numerical_features:
        st.markdown(f"**Distribution of {selected_feature}**")
        histogram_data = df[[selected_feature]].dropna()
        st.bar_chart(
            histogram_data[selected_feature].value_counts().sort_index(),
            height=300,
        )

        st.markdown("**Summary statistics**")
        st.dataframe(
            df[selected_feature].describe().to_frame(),
            use_container_width=True,
        )

    else:
        st.markdown(f"**Categories in {selected_feature}**")
        category_counts = (
            df[selected_feature]
            .fillna("Missing")
            .value_counts()
            .head(20)
            .rename_axis(selected_feature)
            .reset_index(name="Customers")
        )
        st.bar_chart(
            category_counts,
            x=selected_feature,
            y="Customers",
            height=350,
        )

    st.divider()
    st.subheader("Feature versus subscription outcome")

    compare_feature = st.selectbox(
        "Choose a feature to compare with the target",
        all_features,
        key="compare_feature",
    )

    if compare_feature in numerical_features:
        grouped = (
            df.groupby("y", observed=False)[compare_feature]
            .agg(["mean", "median"])
            .reindex(["no", "yes"])
        )
        st.markdown("**Mean and median by outcome**")
        st.dataframe(grouped, use_container_width=True)

        st.markdown("**Distribution by outcome**")
        st.caption(
            "The chart below compares average values; it is not a "
            "distribution plot."
        )
        mean_data = (
            df.groupby("y")[compare_feature]
            .mean()
            .reindex(["no", "yes"])
            .rename_axis("Outcome")
            .reset_index(name=f"Mean {compare_feature}")
        )
        st.bar_chart(
            mean_data,
            x="Outcome",
            y=f"Mean {compare_feature}",
        )

    else:
        comparison = pd.crosstab(
            df[compare_feature].fillna("Missing"),
            df["y"],
            normalize="index",
        ) * 100

        st.caption("Values are percentages within each feature category.")
        st.dataframe(
            comparison.round(2),
            use_container_width=True,
        )


# --------------------------------------------------
# Tab 3: Evaluate models
# --------------------------------------------------
with evaluate_tab:
    st.subheader("Compare trained classifiers")

    st.write(
        "Models are evaluated on a stratified 20% test split. "
        "The preprocessing transformer is reconstructed from the dataset "
        "using the notebook's StandardScaler and OneHotEncoder approach."
    )

    selected_models = st.multiselect(
        "Select models to evaluate",
        options=list(models.keys()),
        default=[
            name for name in [
                "Logistic Regression",
                "Decision Tree",
                "Random Forest",
                "Gradient Boosting",
            ]
            if name in models
        ],
    )

    if st.button("Evaluate selected models", type="primary"):
        if not selected_models:
            st.warning("Select at least one model.")
        else:
            results = []
            predictions_by_model = {}

            for name in selected_models:
                model = models[name]

                try:
                    predictions = model.predict(X_test_processed)
                    predictions_by_model[name] = predictions

                    results.append(
                        {
                            "Model": name,
                            "Accuracy": accuracy_score(y_test, predictions),
                            "Precision (yes)": precision_score(
                                y_test,
                                predictions,
                                pos_label="yes",
                                zero_division=0,
                            ),
                            "Recall (yes)": recall_score(
                                y_test,
                                predictions,
                                pos_label="yes",
                                zero_division=0,
                            ),
                            "F1-score (yes)": f1_score(
                                y_test,
                                predictions,
                                pos_label="yes",
                                zero_division=0,
                            ),
                        }
                    )

                except Exception as exc:
                    st.error(f"{name} could not be evaluated: {exc}")

            if results:
                results_df = pd.DataFrame(results).set_index("Model")
                st.markdown("**Evaluation metrics**")
                st.dataframe(
                    results_df.style.format("{:.3f}"),
                    use_container_width=True,
                )

                st.markdown("**Compare metrics**")
                st.bar_chart(results_df)

                selected_for_matrix = st.selectbox(
                    "Choose a model for the confusion matrix",
                    list(predictions_by_model.keys()),
                    key="confusion_matrix_model",
                )

                matrix = confusion_matrix(
                    y_test,
                    predictions_by_model[selected_for_matrix],
                    labels=["no", "yes"],
                )

                fig, ax = plt.subplots(figsize=(5, 4))
                display = ConfusionMatrixDisplay(
                    confusion_matrix=matrix,
                    display_labels=["No", "Yes"],
                )
                display.plot(ax=ax, values_format="d", colorbar=False)
                ax.set_title(f"{selected_for_matrix} — Confusion Matrix")
                st.pyplot(fig)
                plt.close(fig)

                report = classification_report(
                    y_test,
                    predictions_by_model[selected_for_matrix],
                    labels=["no", "yes"],
                    target_names=["No", "Yes"],
                    output_dict=True,
                    zero_division=0,
                )
                st.markdown("**Detailed classification report**")
                st.dataframe(
                    pd.DataFrame(report).T.round(3),
                    use_container_width=True,
                )

    st.caption(
        "Note: this page reconstructs the preprocessing pipeline from the "
        "current dataset. Evaluation is meaningful only if the split settings "
        "and feature definitions match those used when training the saved models."
    )


# --------------------------------------------------
# Tab 4: Predict
# --------------------------------------------------
with predict_tab:
    st.subheader("Predict a customer's subscription outcome")

    st.write(
        "Enter the customer's information below. The selected saved model "
        "will receive the same scaled and one-hot-encoded feature representation "
        "used by the training workflow."
    )

    selected_model_name = st.selectbox(
        "Classification model",
        list(models.keys()),
        key="prediction_model",
    )

    st.caption(
        "The `duration` feature is the last contact duration in seconds. "
        "In a real campaign, this value may not be known before the call; "
        "using it can make a retrospective prediction less useful for "
        "pre-call targeting."
    )

    with st.form("customer_prediction_form"):
        st.markdown("**Customer information**")

        form_values = {}

        # Render numerical features in a compact two-column layout.
        numeric_columns = st.columns(2)

        for index, feature in enumerate(numerical_features):
            series = pd.to_numeric(df[feature], errors="coerce").dropna()

            if series.empty:
                minimum, maximum, default = 0.0, 100.0, 0.0
            else:
                minimum = float(series.min())
                maximum = float(series.max())
                default = float(series.median())

            # Number inputs avoid accidentally selecting a value outside
            # the source dataset's observed range.
            with numeric_columns[index % 2]:
                if pd.api.types.is_integer_dtype(df[feature]):
                    form_values[feature] = st.number_input(
                        feature.replace("_", " ").title(),
                        min_value=int(minimum),
                        max_value=int(maximum),
                        value=int(default),
                        step=1,
                    )
                else:
                    form_values[feature] = st.number_input(
                        feature.replace("_", " ").title(),
                        min_value=minimum,
                        max_value=maximum,
                        value=default,
                    )

        st.markdown("**Categorical features**")
        categorical_columns_ui = st.columns(2)

        for index, feature in enumerate(categorical_features):
            options = sorted(
                df[feature].dropna().astype(str).unique().tolist()
            )

            if not options:
                options = ["unknown"]

            default_index = (
                options.index("unknown")
                if "unknown" in options
                else 0
            )

            with categorical_columns_ui[index % 2]:
                form_values[feature] = st.selectbox(
                    feature.replace("_", " ").title(),
                    options,
                    index=default_index,
                )

        submitted = st.form_submit_button(
            "Predict subscription outcome",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        input_df = pd.DataFrame(
            [{feature: form_values[feature] for feature in X.columns}],
            columns=X.columns,
        )

        try:
            transformed_input = preprocessor.transform(input_df)
            model = models[selected_model_name]
            prediction = str(model.predict(transformed_input)[0]).lower()

            st.divider()
            st.markdown("### Prediction result")

            if prediction == "yes":
                st.success(
                    "The model predicts that this customer **may subscribe**."
                )
            else:
                st.info(
                    "The model predicts that this customer **may not subscribe**."
                )

            st.metric("Predicted class", prediction.upper())

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(transformed_input)[0]
                classes = [str(c).lower() for c in model.classes_]

                if "yes" in classes:
                    yes_probability = float(probabilities[classes.index("yes")])
                    no_probability = float(probabilities[classes.index("no")])

                    prob_col1, prob_col2 = st.columns(2)
                    prob_col1.metric(
                        "Estimated probability: Yes",
                        f"{yes_probability:.1%}",
                    )
                    prob_col2.metric(
                        "Estimated probability: No",
                        f"{no_probability:.1%}",
                    )

                    st.progress(yes_probability)
                    st.caption(
                        "These are model-estimated probabilities, not a "
                        "guarantee that the customer will subscribe."
                    )

            else:
                st.caption(
                    "This model does not expose predict_proba, so calibrated "
                    "class probabilities are not available here."
                )

            with st.expander("Review submitted input"):
                st.dataframe(input_df, use_container_width=True)

        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
            st.caption(
                "Check that the selected model was trained on the same "
                "feature schema and preprocessing representation."
            )
