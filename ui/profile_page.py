# ui/profile_page.py

import streamlit as st
from services.resume_parser import ResumeParser
from services.profile_extractor import ProfileExtractor
from models.profile import Profile
from services.profile_service import ProfileService


service = ProfileService()


def render_profile():

    st.header("👤 Career Profile")

    if "parsed_profile" not in st.session_state:
        st.session_state.parsed_profile = {}

    profile = service.get_profile()

    if profile is None:
        profile = Profile()

    #parsed = st.session_state.parsed_profile

    uploaded_resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
    )

    if uploaded_resume:

        if st.button("✨ Extract Profile with AI"):

            with st.spinner("Parsing your resume..."):

                try:
                                       
                    resume_text = ResumeParser.extract_text(uploaded_resume)

                    extracted = ProfileExtractor.extract(resume_text)

                    extracted["resume"] = resume_text

                    st.session_state.parsed_profile = extracted
                    
                    #parsed = st.session_state.parsed_profile

                    st.success("Profile extracted successfully!")

                    st.rerun()

                except Exception as e:

                    st.error(f"Error extracting profile: {e}")

    parsed = st.session_state.parsed_profile
                

    with st.form("profile_form"):

        name = st.text_input(
            "Name",
            value=parsed.get("name", profile.name)
        )

        email = st.text_input(
            "Email",
            value=parsed.get("email", profile.email)
        )

        phone = st.text_input(
            "Phone",
            value=parsed.get("phone", profile.phone)
        )

        linkedin = st.text_input(
            "LinkedIn",
            value=parsed.get("linkedin", profile.linkedin)
        )

        github = st.text_input(
            "GitHub",
            value=parsed.get("github", profile.github)
        )

        years = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=40,
            value=parsed.get("years_experience", profile.years_experience)
        )

        expected_salary = st.text_input(
            "Expected Salary",
            value=parsed.get("expected_salary", profile.expected_salary)
        )

        preferred_roles = st.text_input(
            "Preferred Roles (comma separated)",
            value=", ".join(parsed.get("preferred_roles", profile.preferred_roles))
        )

        preferred_locations = st.text_input(
            "Preferred Locations",
            value=", ".join(parsed.get("preferred_locations", profile.preferred_locations))
        )

        skills = st.text_input(
            "Skills",
            value=", ".join(parsed.get("skills", profile.skills))
        )

        industries = st.text_input(
            "Industries",
            value=", ".join(parsed.get("industries", profile.industries))
        )

        resume = st.text_area(
            "Resume",
            value= parsed.get("resume", profile.resume),
            height=300
        )

        submitted = st.form_submit_button("💾 Save Profile")

        if submitted:

            updated = Profile(

                name=name,

                email=email,

                phone=phone,

                linkedin=linkedin,

                github=github,

                years_experience=years,

                expected_salary=expected_salary,

                preferred_roles=[
                    x.strip()
                    for x in preferred_roles.split(",")
                    if x.strip()
                ],

                preferred_locations=[
                    x.strip()
                    for x in preferred_locations.split(",")
                    if x.strip()
                ],

                skills=[
                    x.strip()
                    for x in skills.split(",")
                    if x.strip()
                ],

                industries=[
                    x.strip()
                    for x in industries.split(",")
                    if x.strip()
                ],

                resume=resume

            )

            #st.write(updated)
            service.save_profile(updated)

            st.session_state.parsed_profile = {}
            
            st.success("Profile saved successfully!")

            