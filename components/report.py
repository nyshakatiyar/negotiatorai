import streamlit as st
import pandas as pd
import plotly.express as px


def render_report():

    st.title("Final Negotiation Report")

    if not st.session_state.get("simulation_finished", False):

        st.info(
            "Complete all five negotiation rounds to view "
            "your final report."
        )

        return

    profile = st.session_state.profile
    scores = st.session_state.scores

    if not scores:
        st.warning("No negotiation data available.")
        return

    final_score = scores[-1]["overall"]

    target = profile["target_salary"]
    current = profile["current_salary"]

    final_offer = current

    if final_score >= 90:
        final_offer = target

    elif final_score >= 80:
        final_offer = round(
            current + (target - current) * 0.85
        )

    elif final_score >= 70:
        final_offer = round(
            current + (target - current) * 0.70
        )

    else:
        final_offer = round(
            current + (target - current) * 0.50
        )

    achievement = round(
        (final_offer / target) * 100,
        1
    )

    st.subheader("Negotiation Outcome")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Final Offer",
            f"₹{final_offer:,.0f}"
        )

    with col2:
        st.metric(
            "Target Salary",
            f"₹{target:,.0f}"
        )

    with col3:
        st.metric(
            "Target Achieved",
            f"{achievement}%"
        )

    with col4:
        st.metric(
            "Overall Score",
            f"{final_score}/100"
        )

    st.divider()

    st.subheader("Performance Progression")

    data = []

    for index, score in enumerate(scores, start=1):

        data.append(
            {
                "Round": index,
                "Overall": score["overall"],
                "Confidence": score["confidence"],
                "Persuasiveness": score["persuasiveness"],
                "Evidence": score["evidence"],
                "Communication": score["communication"],
                "Professionalism": score["professionalism"],
                "Strategy": score["strategy"]
            }
        )

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Round",
        y=[
            "Overall",
            "Confidence",
            "Persuasiveness",
            "Evidence"
        ],
        markers=True,
        title="Negotiation Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    latest = scores[-1]

    st.subheader("Final AI Feedback")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Strengths")

        for strength in latest.get(
            "strengths", []
        ):
            st.write(f"• {strength}")

    with col2:

        st.markdown("### Areas to Improve")

        for weakness in latest.get(
            "weaknesses", []
        ):
            st.write(f"• {weakness}")

    st.divider()

    st.subheader("Coach Recommendation")

    st.write(
        latest.get(
            "feedback",
            "No feedback available."
        )
    )

    st.subheader("Recommended Better Response")

    st.info(
        latest.get(
            "better_response",
            "No recommendation available."
        )
    )