
import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("## ML Capstone Project")
        st.caption("Machine Learning Explorer")

        st.divider()
        st.markdown("### Workspace")

        pages = [
            ("Home", "app.py"),
            ("Regression", "pages/Regression.py"),
            ("Classification", "pages/Classification.py"),
            ("Clustering", "pages/Clustering.py"),
            ("Visualizations", "pages/Visualizations.py"),
        ]

        for label, page in pages:
            if st.button(
                label,
                key=f"nav_{label.lower()}",
                use_container_width=True,
            ):
                st.switch_page(page)

        st.divider()
        st.markdown("### Team Cipher")

        # Keep your existing team member names and GitHub links here.

        st.divider()
        st.caption("ML Capstone Project · 23CSE301")
