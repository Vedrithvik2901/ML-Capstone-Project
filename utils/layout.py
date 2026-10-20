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
            background: #e7ece3;
            border-right: 1px solid #c8d3c8;
        }

        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #5f7469;
        }

        [data-testid="stSidebar"] .stButton > button {
            min-height: 44px;
            border: 1px solid #8a9a86;
            border-radius: 10px;
            background: #f5f6f2;
            color: #004b36;
            font-weight: 650;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: #004b36;
            background: #ffffff;
            color: #004b36;
        }

        [data-testid="stSidebar"] hr {
            border-color: #c8d3c8;
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
