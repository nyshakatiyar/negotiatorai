import streamlit as st


def render_dashboard():

    st.title("NegotiateAI")

    st.subheader("AI-Powered Salary Negotiation Simulator")

    st.write(
        """
        Practice real-world salary negotiations with an AI HR manager.
        Receive instant performance analysis, adaptive difficulty,
        and personalized negotiation coaching.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AI HR Manager",
            "Active"
        )

    with col2:
        st.metric(
            "Negotiation Rounds",
            "5"
        )

    with col3:
        st.metric(
            "AI Coaching",
            "Real-time"
        )

    st.divider()

    st.subheader("How It Works")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown("### 01")
        st.write("Create your candidate profile.")

    with step2:
        st.markdown("### 02")
        st.write("Negotiate with AI HR.")

    with step3:
        st.markdown("### 03")
        st.write("Receive performance scores.")

    with step4:
        st.markdown("### 04")
        st.write("Get your final negotiation report.")

    st.divider()

    st.info(
        "Go to Candidate Profile to begin your first simulation."
    )