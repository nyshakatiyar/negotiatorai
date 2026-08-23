import os

import streamlit as st
from dotenv import load_dotenv

from components.dashboard import render_dashboard
from components.candidate import render_candidate_form
from components.negotiation import render_negotiation
from components.report import render_report


# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NegotiateAI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Session State
# --------------------------------------------------

defaults = {
    "profile": None,
    "messages": [],
    "scores": [],
    "round": 0,
    "current_offer": 0,
    "difficulty": 1,
    "simulation_started": False,
    "simulation_finished": False
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        # 💼 NegotiateAI

        **AI Salary Negotiation Simulator**
        """
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Candidate Profile",
            "Negotiation Room",
            "Final Report"
        ]
    )

    st.divider()

    if st.session_state.profile:

        st.caption("Current Candidate")

        st.write(
            f"**{st.session_state.profile['name']}**"
        )

        st.write(
            st.session_state.profile["role"]
        )

        st.divider()

        if st.session_state.simulation_started:

            st.caption(
                f"Round {st.session_state.round}/5"
            )


# --------------------------------------------------
# Page Router
# --------------------------------------------------

if page == "Dashboard":

    render_dashboard()


elif page == "Candidate Profile":

    render_candidate_form()


elif page == "Negotiation Room":

    render_negotiation()


elif page == "Final Report":

    render_report()