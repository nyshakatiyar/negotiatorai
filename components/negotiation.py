import streamlit as st

from services.groq_hr import generate_hr_response
from services.groq_coach import evaluate_response
from utils.scoring import calculate_difficulty


def start_simulation():

    if st.session_state.simulation_started:
        return

    profile = st.session_state.profile

    st.session_state.round = 1
    st.session_state.current_offer = round(
        profile["current_salary"] * 1.17
    )

    initial_offer = st.session_state.current_offer

    first_message = (
        f"Thank you for taking the time to speak with us, "
        f"{profile['name']}. We've reviewed your profile for the "
        f"{profile['role']} position. Based on your experience and "
        f"our current compensation structure, we'd like to begin "
        f"with an offer of ₹{initial_offer:,.0f} per month. "
        f"How would you respond?"
    )

    st.session_state.messages.append(
        {
            "role": "hr",
            "content": first_message
        }
    )

    st.session_state.simulation_started = True


def render_messages():

    for message in st.session_state.messages:

        if message["role"] == "hr":

            with st.chat_message("assistant"):
                st.markdown("**HR Manager**")
                st.write(message["content"])

        else:

            with st.chat_message("user"):
                st.markdown("**You**")
                st.write(message["content"])


def render_metrics():

    if st.session_state.scores:

        latest = st.session_state.scores[-1]

        st.metric(
            "Negotiation Score",
            f"{latest['overall']}/100"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Confidence",
                f"{latest['confidence']}/100"
            )

        with col2:
            st.metric(
                "Persuasiveness",
                f"{latest['persuasiveness']}/100"
            )

    else:

        st.metric(
            "Negotiation Score",
            "—"
        )


def submit_response(candidate_response):

    if not candidate_response.strip():
        st.warning("Please enter a response.")
        return

    hr_messages = [
        m for m in st.session_state.messages
        if m["role"] == "hr"
    ]

    latest_hr_message = hr_messages[-1]["content"]

    st.session_state.messages.append(
        {
            "role": "user",
            "content": candidate_response.strip()
        }
    )

    with st.spinner("AI is evaluating your negotiation..."):

        evaluation = evaluate_response(
            profile=st.session_state.profile,
            hr_message=latest_hr_message,
            candidate_response=candidate_response,
            round_number=st.session_state.round
        )

    st.session_state.scores.append(evaluation)

    st.session_state.difficulty = calculate_difficulty(
        evaluation["overall"],
        st.session_state.difficulty
    )

    if st.session_state.round >= 5:

        st.session_state.simulation_finished = True
        return

    st.session_state.round += 1

    with st.spinner("HR is preparing the next response..."):

        hr_response = generate_hr_response(
            profile=st.session_state.profile,
            conversation=st.session_state.messages,
            round_number=st.session_state.round,
            current_offer=st.session_state.current_offer,
            difficulty=st.session_state.difficulty
        )

    st.session_state.messages.append(
        {
            "role": "hr",
            "content": hr_response
        }
    )


def render_negotiation():

    st.title("Negotiation Room")

    if "profile" not in st.session_state:
        st.warning(
            "Please complete your Candidate Profile first."
        )
        return

    start_simulation()

    left, middle, right = st.columns([1, 2.5, 1])

    profile = st.session_state.profile

    with left:

        st.subheader("Candidate")

        st.write(f"**Role:** {profile['role']}")
        st.write(f"**Experience:** {profile['experience']} years")

        st.divider()

        st.metric(
            "Current Salary",
            f"₹{profile['current_salary']:,.0f}"
        )

        st.metric(
            "Target Salary",
            f"₹{profile['target_salary']:,.0f}"
        )

        st.metric(
            "Minimum",
            f"₹{profile['minimum_salary']:,.0f}"
        )

    with middle:

        st.subheader(
            f"Round {st.session_state.round} / 5"
        )

        render_messages()

        st.divider()

        response = st.text_area(
            "Your Response",
            placeholder=(
                "Explain why you believe your target "
                "salary is justified..."
            ),
            key=f"response_{st.session_state.round}"
        )

        if st.button(
            "Submit Response",
            type="primary",
            use_container_width=True
        ):

            submit_response(response)
            st.rerun()

    with right:

        st.subheader("Performance")

        render_metrics()

        st.divider()

        st.write(
            f"**HR Difficulty:** "
            f"{st.session_state.difficulty}/5"
        )

        if st.session_state.scores:

            latest = st.session_state.scores[-1]

            with st.expander("Latest Feedback"):

                st.write(
                    latest.get("feedback", "")
                )

            with st.expander("Strengths"):

                for strength in latest.get(
                    "strengths", []
                ):
                    st.write(f"• {strength}")

            with st.expander("Weaknesses"):

                for weakness in latest.get(
                    "weaknesses", []
                ):
                    st.write(f"• {weakness}")

            with st.expander("Better Response"):

                st.write(
                    latest.get("better_response", "")
                )