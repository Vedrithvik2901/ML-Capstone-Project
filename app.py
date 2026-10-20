import streamlit as st
import pandas as pd
from pathlib import Path

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
# Theme
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #111318;
        color: #F3F4F6;
    }

    [data-testid="stSidebar"] {
        background: #191C23;
        border-right: 1px solid #30333B;
    }

    .hero {
        padding: 2rem 0 1.5rem 0;
    }

    .eyebrow {
        color: #A3E635;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero h1 {
        font-size: clamp(2.2rem, 5vw, 3.8rem);
        font-weight: 750;
        letter-spacing: -0.045em;
        margin: 0.6rem 0;
        color: #F3F4F6;
    }

    .hero p {
        color: #A0A3AD;
        font-size: 1.05rem;
        max-width: 720px;
        line-height: 1.7;
    }

    .track-card {
        background: #1B1E24;
        border: 1px solid #30333B;
        border-radius: 16px;
        padding: 1.25rem;
        min-height: 190px;
    }

    .track-card h3 {
        color: #F3F4F6;
        margin-top: 0.5rem;
    }

    .track-card p {
        color: #A0A3AD;
        line-height: 1.6;
    }

    .track-number {
        color: #A3E635;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
    }

    div[data-testid="stMetric"] {
        background: #1B1E24;
        border: 1px solid #30333B;
        border-radius: 12px;
        padding: 1rem;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    hr {
        border-color: #30333B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Cached project inventory
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
    st.markdown("## 🧠 ML Explorer")
    st.caption("Machine Learning Capstone")

    st.divider()

    st.markdown("**WORKSPACE**")
    st.markdown("Use the pages in this sidebar to navigate between the ML tracks.")

    st.divider()
    st.caption("Regression · Classification · Clustering")

# --------------------------------------------------
# Hero
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">MACHINE LEARNING CAPSTONE</div>
        <h1>Explore. Learn. Analyze.</h1>
        <p>
            An interactive workspace for exploring datasets, understanding
            machine learning models, and investigating predictions across
            regression, classification, and clustering.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Overview metrics
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Datasets available", len(datasets))

with col2:
    st.metric("Saved model artifacts", len(models))

with col3:
    st.metric("Learning tracks", 3)

st.divider()

# --------------------------------------------------
# Learning tracks
# --------------------------------------------------
st.subheader("Explore machine learning")
st.caption("Choose a track to investigate its data, models, and results.")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">01 / REGRESSION</div>
            <h3>Predict continuous values</h3>
            <p>
                Explore Melbourne Housing data, estimate property prices,
                and compare regression algorithms.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Regression", use_container_width=True):
        st.switch_page("pages/Regression.py")

with c2:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">02 / CLASSIFICATION</div>
            <h3>Predict class labels</h3>
            <p>
                Investigate Bank Marketing data and compare classifiers
                using meaningful evaluation metrics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Classification", use_container_width=True):
        st.switch_page("pages/Classification.py")

with c3:
    st.markdown(
        """
        <div class="track-card">
            <div class="track-number">03 / CLUSTERING</div>
            <h3>Discover hidden groups</h3>
            <p>
                Explore Online Retail data and investigate customer
                or transaction clusters.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Clustering", use_container_width=True):
        st.switch_page("pages/Clustering.py")

st.divider()

# --------------------------------------------------
# Dataset inventory
# --------------------------------------------------
st.subheader("Project assets")

left, right = st.columns([1.2, 1])

with left:
    st.markdown("#### Datasets")

    if datasets:
        dataset_table = pd.DataFrame(
            [
                {
                    "Dataset": file.name,
                    "Track": file.parent.name.title(),
                    "Size (MB)": round(file.stat().st_size / (1024**2), 2),
                }
                for file in datasets
            ]
        )
        st.dataframe(
            dataset_table,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No datasets found under the data directory.")

with right:
    st.markdown("#### Saved models")

    if models:
        st.dataframe(
            pd.DataFrame(
                {"Model artifact": sorted(file.name for file in models)}
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No .joblib model artifacts found.")

st.divider()
st.caption("ML Capstone Explorer · Interactive research workspace")
