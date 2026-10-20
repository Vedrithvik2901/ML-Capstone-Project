
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Application configuration
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"

st.set_page_config(
    page_title="ML Capstone Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# UI theme
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --page-bg: #111318;
        --surface: #1b1e25;
        --surface-hover: #222630;
        --border: #303540;
        --text: #f3f4f6;
        --muted: #a0a6b4;
        --accent: #a3e635;
        --accent-dark: #1d2a13;
    }

    .stApp {
        background: var(--page-bg);
        color: var(--text);
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }


    [data-testid="stSidebarNavSeparator"] {
        display: none;
    }

    [data-testid="stSidebar"] {
        background: #191c23;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--muted);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: clamp(1.5rem, 4vw, 3rem);
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
        border-radius: 22px;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(163, 230, 53, 0.12),
                transparent 35%
            ),
            linear-gradient(135deg, #1c2028, #15171d);
    }

    .eyebrow {
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 0.7rem 0;
        color: var(--text);
        font-size: clamp(2.2rem, 5vw, 3.6rem);
        font-weight: 800;
        letter-spacing: -0.045em;
        line-height: 1.1;
    }

    .hero p {
        max-width: 760px;
        color: var(--muted);
        font-size: 1.04rem;
        line-height: 1.8;
    }

    .hero-note {
        display: inline-block;
        margin-top: 0.5rem;
        padding: 0.45rem 0.75rem;
        border: 1px solid #414a35;
        border-radius: 999px;
        background: #1c2418;
        color: #d9f99d;
        font-size: 0.78rem;
    }

    .section-heading {
        margin-top: 2rem;
        margin-bottom: 0.25rem;
        color: var(--text);
        font-size: 1.45rem;
        font-weight: 750;
    }

    .section-description {
        margin-bottom: 1.1rem;
        color: var(--muted);
        line-height: 1.65;
    }

    /* Equal-size track cards */
    .track-card {
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        height: 260px;
        min-height: 260px;
        padding: 1.35rem;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: var(--surface);
        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            transform 0.2s ease;
    }

    .track-card:hover {
        border-color: #586246;
        background: var(--surface-hover);
        transform: translateY(-2px);
    }

    .track-number {
        margin-bottom: 0.8rem;
        color: var(--accent);
        font-size: 0.73rem;
        font-weight: 750;
        letter-spacing: 0.12em;
    }

    .track-card h3 {
        margin: 0 0 0.65rem;
        color: var(--text);
        font-size: 1.25rem;
        font-weight: 750;
    }

    .track-card p {
        margin: 0;
        color: var(--muted);
        font-size: 0.91rem;
        line-height: 1.65;
    }

    .track-tag {
        margin-top: auto;
        padding-top: 1rem;
        color: #d9f99d;
        font-size: 0.78rem;
        font-weight: 650;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        padding: 1rem 1.1rem;
        border: 1px solid var(--border);
        border-radius: 13px;
        background: var(--surface);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: var(--text);
    }

    /* Buttons */
    .stButton > button {
        min-height: 44px;
        border-radius: 10px;
        font-weight: 650;
        transition: border-color 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        border: 1px solid #b5ef65;
        background: var(--accent);
        color: #17200d;
    }

    .stButton > button[kind="primary"]:hover {
        border-color: #c9f78b;
        background: #b5ef65;
        color: #17200d;
    }

    .stButton > button[kind="secondary"] {
        border: 1px solid #414651;
        background: #20242d;
        color: var(--text);
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #707b8d;
        color: white;
    }

    .workflow-card {
        height: 100%;
        box-sizing: border-box;
        padding: 1.2rem;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: var(--surface);
    }

    .workflow-step {
        margin-bottom: 0.55rem;
        color: var(--accent);
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.1em;
    }

    .workflow-card h4 {
        margin: 0 0 0.5rem;
        color: var(--text);
        font-size: 1rem;
    }

    .workflow-card p {
        margin: 0;
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.65;
    }

    .asset-panel {
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: var(--surface);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    hr {
        border-color: var(--border);
    }

    @media (max-width: 900px) {
        .track-card {
            height: auto;
            min-height: 240px;
        }

        .hero {
            border-radius: 16px;
        }
    }

    @media (max-width: 600px) {
        .block-container {
            padding-top: 1rem;
        }

        .track-card {
            min-height: 0;
        }
    }

.team-member-card {
    box-sizing: border-box;
    width: 100%;
    margin: 0 0 1rem;
    padding: 1.4rem 1.6rem;
    border: 1px solid #303540;
    border-radius: 14px;
    background: #1b1e25;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.team-member-card:hover {
    border-color: #586246;
    background: #20242c;
}

.team-member-number {
    margin-bottom: 0.6rem;
    color: #a3e635;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.12em;
}

.team-member-card h3 {
    margin: 0 0 0.35rem;
    color: #f3f4f6;
    font-size: 1.2rem;
}

.team-member-role {
    margin-bottom: 0.65rem;
    color: #d9f99d;
    font-size: 0.9rem;
    font-weight: 600;
}

.team-member-card p {
    margin: 0;
    color: #a0a6b4;
    font-size: 0.92rem;
    line-height: 1.65;
}

.github-link {
    display: inline-block;
    margin-top: 0.9rem;
    color: #a3e635;
    font-size: 0.88rem;
    font-weight: 650;
    text-decoration: none;
}

.github-link:hover {
    color: #c9f78b;
    text-decoration: underline;
}

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Project inventory
# --------------------------------------------------
@st.cache_data
def get_project_inventory():
    datasets = []

    if DATA_DIR.exists():
        for file in DATA_DIR.rglob("*"):
            if file.is_file() and file.suffix.lower() in {
                ".csv", ".xlsx", ".xls"
            }:
                datasets.append(file)

    models = (
        list(MODEL_DIR.glob("*.joblib"))
        if MODEL_DIR.exists()
        else []
    )

    return datasets, models


datasets, models = get_project_inventory()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("## ML Capstone Project")
    st.caption("An interactive workspace for turning data into predictions, patterns, and insights.")

    st.divider()

    st.markdown("### Workspace")
    st.caption("Choose a track to get started.")

    if st.button(" Home", use_container_width=True):
        st.switch_page("app.py")

    if st.button(" Regression", use_container_width=True):
        st.switch_page("pages/Regression.py")

    if st.button(" Classification", use_container_width=True):
        st.switch_page("pages/Classification.py")

    if st.button(" Clustering", use_container_width=True):
        st.switch_page("pages/Clustering.py")

    if st.button("Visualizations", use_container_width=True):
        st.switch_page("pages/Visualizations.py")

    st.divider()

    


    st.markdown("### Team Cipher")
    st.caption("The team behind the project")

    st.markdown("**G.Dheeraj · [GitHub ↗](https://github.com/Shyam9607)**")
    st.caption("Classification")

    st.markdown("**B.Aashrith · [GitHub ↗](https://github.com/aashrith376)**")
    st.caption("Clustering")

    st.markdown("**G.Vedrithvik · [GitHub ↗](https://github.com/Vedrithvik2901)**")
    st.caption("Regression")



# --------------------------------------------------
# Hero
# --------------------------------------------------
st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">MACHINE LEARNING CAPSTONE</div>
        <h1>Explore. Learn. Analyze.</h1>
        <p>
            An interactive machine learning workspace to explore datasets,
        experiment with regression, classification, and clustering,
        and understand how models turn data into meaningful insights.
        </p>
        <span class="hero-note">
            Regression · Classification · Clustering 
        </span>
    </section>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Overview metrics
# --------------------------------------------------
model_names = {file.stem for file in models}

regression_names = {
    "linear_regression",
    "ridge_regression",
    "lasso_regression",
    "elasticnet_regression",
    "polynomial_regression",
    "decision_tree_regressor",
    "gradient_boosting_regressor",
    "svr",
    "knn_regressor",
    "random_forest_regressor"
}

classification_names = {
    "logistic_regression",
    "knn",
    "gaussian_nb",
    "decision_tree_classifier",
    "svm",
    "random_forest",
    "adaboost",
    "gradient_boosting_classifier",
    "bagging",
    "mlp_classifier",
}

clustering_names = {
    "kmeans_clustering",
    "agglomerative_clustering",
}

m1, m2, m3 = st.columns(3)

with m1:
     st.metric("Tracks", 3)

with m2:
    st.metric("Datasets", 3)

with m3:
        st.metric("Models", 22)


# --------------------------------------------------
# Learning tracks
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Explore machine learning</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Choose a track to explore its dataset, experiment with models, '
    'and understand the results.'
    '</div>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">01 / REGRESSION</div>
            <h3>Predict continuous values</h3>
            <p>
                Explore Melbourne Housing data, estimate property
                prices, and compare regression algorithms.
            </p>
            <div class="track-tag">Price estimation · Model comparison</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Regression →",
        key="home_regression",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/Regression.py")

with c2:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">02 / CLASSIFICATION</div>
            <h3>Predict class labels</h3>
            <p>
                Explore Bank Marketing data, generate class predictions,
                and compare models using classification metrics.
            </p>
            <div class="track-tag">Class prediction · Evaluation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Classification →",
        key="home_classification",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/Classification.py")

with c3:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">03 / CLUSTERING</div>
            <h3>Discover hidden groups</h3>
            <p>
                Investigate Online Retail data, segment customers,
                and discover similarities in purchasing behaviour.
            </p>
            <div class="track-tag">Customer segments · Pattern discovery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Open Clustering →",
        key="home_clustering",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/Clustering.py")

# --------------------------------------------------
# How to use the explorer
# --------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-heading">How to use the explorer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Follow this simple workflow to get the most out of the project.'
    '</div>',
    unsafe_allow_html=True,
)

w1, w2, w3, w4 = st.columns(4, gap="medium")

workflow = [
    (
        "STEP 01",
        "Explore the data",
        "Understand the dataset, features, distributions, and data quality.",
    ),
    (
        "STEP 02",
        "Choose a model",
        "Select an algorithm that matches the machine learning task.",
    ),
    (
        "STEP 03",
        "Inspect results",
        "Compare available evaluation metrics and visual evidence.",
    ),
    (
        "STEP 04",
        "Try predictions",
        "Use supported prediction forms and interpret their outputs.",
    ),
]

for column, (step, title, description) in zip(
    [w1, w2, w3, w4], workflow
):
    with column:
        st.markdown(
            f"""
            <div class="workflow-card">
                <div class="workflow-step">{step}</div>
                <h4>{title}</h4>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# Project assets
# --------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-heading">Project assets</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'A quick inventory of the datasets and trained model files available '
    'in this project.'
    '</div>',
    unsafe_allow_html=True,
)

assets_left, assets_right = st.columns([1.15, 1], gap="large")

with assets_left:
    st.markdown("#### Datasets")

    if datasets:
        dataset_table = pd.DataFrame(
            [
                {
                    "Dataset": file.name,
                    "Track": file.parent.name.replace("_", " ").title(),
                    "Size (MB)": round(
                        file.stat().st_size / (1024 ** 2), 2
                    ),
                }
                for file in sorted(datasets)
            ]
        )

        st.dataframe(
            dataset_table,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No supported datasets found under the data directory.")

with assets_right:
    st.markdown("#### Saved models")

    if models:
        model_table = pd.DataFrame(
            {
                "Model artifact": sorted(file.name for file in models)
            }
        )

        st.dataframe(
            model_table,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No `.joblib` model artifacts found.")


# --------------------------------------------------
# About the team
# --------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-heading">About the Team</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Meet Team Cipher, the team behind this machine learning capstone '
    'project.'
    '</div>',
    unsafe_allow_html=True,
)

team_members = [
    {
        "name": "Shyam Sreehasa Dheeraj Gudipati",
        "role": "Implementation and Visualisation of Classification Algorithms",
        "description": (
            "Implemented and visualised the classification algorithms "
            "on Bank Marketing dataset."
        ),
        "github": "https://github.com/Shyam9607"
    },
    {
        "name": "Bothula Aashrith",
        "role": "Implementation and Visualisation of Clustering Algorithms",
        "description": (
            "Implemented and visualised the clustering algorithms "
            "on Online Retail dataset."
        ),
        "github": "https://github.com/aashrith376"
    },
    {
        "name": "Gamineni Vedrithvik",
        "role": "Implementation and Visualisation of Regression Algorithms",
        "description": (
            "Implemented and visualised the regression algorithms "
            "on Melbourne Housing Prices dataset."
        ),
        "github": "https://github.com/Vedrithvik2901"
    },
]

for index, member in enumerate(team_members, start=1):
    st.markdown(
    f"""
    <div class="team-member-card">
        <div class="team-member-number">TEAM MEMBER {index:02d}</div>
        <h3>{member["name"]}</h3>
        <div class="team-member-role">{member["role"]}</div>
        <p>{member["description"]}</p>
        <a
            href="{member["github"]}"
            target="_blank"
            rel="noopener noreferrer"
            class="github-link"
        >
            GitHub Profile ↗
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()


st.caption(
    "ML Capstone Explorer · Interactive machine learning workspace"
    )

