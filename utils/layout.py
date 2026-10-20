"""Shared Streamlit layout elements for the ML Capstone Explorer."""

import streamlit as st


def render_sidebar() -> None:
    """Render the home page sidebar on every Streamlit page."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavSeparator"] {
            display: none;
        }

        [data-testid="stSidebar"] {
            background: #191c23;
            border-right: 1px solid #303540;
        }

        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #a0a6b4;
        }

        [data-testid="stSidebar"] .stButton > button {
            min-height: 44px;
            border: 1px solid #414651;
            border-radius: 10px;
            background: #20242d;
            color: #f3f4f6;
            font-weight: 650;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: #707b8d;
            color: #ffffff;
        }

        [data-testid="stSidebar"] hr {
            border-color: #303540;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## ML Capstone Project")
        st.caption(
            "An interactive workspace for turning data into predictions, "
            "patterns, and insights."
        )

        st.divider()
        st.markdown("### Workspace")
        st.caption("Choose a track to get started.")

        navigation = (
            ("Home", "app.py"),
            ("Regression", "pages/Regression.py"),
            ("Classification", "pages/Classification.py"),
            ("Clustering", "pages/Clustering.py"),
            ("Visualizations", "pages/Visualizations.py"),
        )

        for label, page in navigation:
            if st.button(label, key=f"sidebar_{label.lower()}", use_container_width=True):
                st.switch_page(page)

        st.divider()
        st.markdown("### Team Cipher")
        st.caption("The team behind the project")

        team = (
            ("G.Dheeraj", "Classification", "https://github.com/Shyam9607"),
            ("B.Aashrith", "Clustering", "https://github.com/aashrith376"),
            ("G.Vedrithvik", "Regression", "https://github.com/Vedrithvik2901"),
        )

        for name, role, github_url in team:
            st.markdown(f"**{name} · [GitHub ↗]({github_url})**")
            st.caption(role)
