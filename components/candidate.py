import streamlit as st


def render_candidate_form():

    st.title("Candidate Profile")

    st.write(
        "Tell the AI HR manager about yourself before starting "
        "the negotiation."
    )

    with st.form("candidate_form"):

        name = st.text_input(
            "Name",
            placeholder="Enter your name"
        )

        role = st.text_input(
            "Job Role",
            placeholder="e.g. Software Engineer"
        )

        experience = st.number_input(
            "Years of Experience",
            min_value=0.0,
            max_value=40.0,
            value=2.0,
            step=0.5
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            current_salary = st.number_input(
                "Current Salary (₹/month)",
                min_value=1,
                value=70000,
                step=1000
            )

        with col2:
            target_salary = st.number_input(
                "Target Salary (₹/month)",
                min_value=1,
                value=96400,
                step=1000
            )

        with col3:
            minimum_salary = st.number_input(
                "Minimum Acceptable Salary (₹/month)",
                min_value=1,
                value=85000,
                step=1000
            )

        skills = st.text_area(
            "Key Skills",
            placeholder="Python, SQL, Machine Learning, React..."
        )

        achievements = st.text_area(
            "Major Achievements",
            placeholder="Describe projects, awards, leadership, etc."
        )

        company_type = st.selectbox(
            "Company Type",
            [
                "Startup",
                "Mid-size Company",
                "Large Corporation",
                "FAANG / Big Tech",
                "Consulting",
                "FinTech",
                "Other"
            ]
        )

        submitted = st.form_submit_button(
            "Start Negotiation",
            use_container_width=True
        )

    if submitted:

        if not name.strip():
            st.error("Please enter your name.")
            return False

        if not role.strip():
            st.error("Please enter your job role.")
            return False

        if target_salary < minimum_salary:
            st.error(
                "Target salary must be greater than or equal "
                "to minimum acceptable salary."
            )
            return False

        if current_salary <= 0:
            st.error("Current salary must be greater than zero.")
            return False

        profile = {
            "name": name.strip(),
            "role": role.strip(),
            "experience": experience,
            "current_salary": current_salary,
            "target_salary": target_salary,
            "minimum_salary": minimum_salary,
            "skills": skills.strip(),
            "achievements": achievements.strip(),
            "company_type": company_type
        }

        st.session_state.profile = profile
        st.session_state.simulation_started = False
        st.session_state.simulation_finished = False
        st.session_state.messages = []
        st.session_state.scores = []
        st.session_state.round = 0
        st.session_state.current_offer = current_salary
        st.session_state.difficulty = 1

        st.success("Candidate profile saved.")

        return True

    return False