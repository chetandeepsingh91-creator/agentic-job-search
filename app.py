import time

from services.search_query_builder import SearchQueryBuilder

start = time.time()
print("App start...")

import streamlit as st
from ui.profile_page import render_profile

@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")
    
def get_vector_store():
    from memory import vector_store
    return vector_store.add_to_vector_store 
    
    
    
from agents import (
    job_understanding_agent,
    fit_agent,
    apply_decision_agent,
    ranking_agent,
    jobs_crawler_agent
)
from services.networking_service import NetworkingService
from services.outreach_service import draft_outreach_messages
from services.resume_service import generate_tailored_resume_pdf, is_apply_yes
from ui.networking_section import render_networking_result

# from memory import (
    # add_to_memory,
    # load_memory,
    # save_memory
# )

print("Imports done:", time.time() - start)

st.set_page_config(page_title="AI Job Agent", layout="wide")

st.title("🤖 AI Career Copilot")

render_profile()

from services.profile_service import ProfileService

profile_service = ProfileService()

profile = profile_service.get_profile()

if profile is None:

    st.warning(
        "Please complete your Career Profile first."
    )

    st.stop()

resume = profile.resume

discover_people = st.checkbox(
    "Find LinkedIn contacts for each job",
    value=True,
    help="Uses SerpAPI to look up public LinkedIn profiles for each job.",
)


@st.cache_resource
def get_networking_service():
    return NetworkingService()


if st.button("Run AI Job Copilot 🚀"):

    if not resume:
        st.warning("Please upload resume")
    else:
        with st.spinner("Finding and evaluating jobs..."):
 
            search = SearchQueryBuilder.build(profile)

            st.info(
                f"""
            Searching for:

            Role:
            {search.query}

            Location:
            {search.location}
            """
            )

            jobs = jobs_crawler_agent.run(search)

            if not jobs:
                st.warning(
                    "No jobs were found for your search. "
                    "Try broadening your preferred role or location in your profile."
                )

            i=1

            for job in jobs:
                jd = job.get("description", "")

                st.markdown(f"---Job {i}---")
                st.subheader(f"{job.get("title","")} at {job.get("company","")}")
                             

                st.write("Generating Job Summary...")
                jd_summary = job_understanding_agent.run(jd)
                st.write("Job Summary:")
                st.write(jd_summary)

                st.write("Performing Fit Analysis...")
                fit = fit_agent.run(profile, jd_summary)
                st.write("📊 Fit:")
                st.write(fit)

                st.write("Making Apply Decision...")
                decision = apply_decision_agent.run(profile, job, fit)
                st.write("🧠 Apply Decision:")
                st.write(decision)

                tailored_resume = None
                if is_apply_yes(decision):
                    st.write("Generating Tailored Resume...")
                    try:
                        pdf_bytes, filename, tailored_resume = (
                            generate_tailored_resume_pdf(
                                profile=profile,
                                job_description=jd_summary,
                                company=job.get("company", ""),
                                job_title=job.get("title", ""),
                            )
                        )
                        st.download_button(
                            label="Download tailored resume (PDF)",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"resume-download-{i}",
                        )
                    except Exception as e:
                        st.error(f"Failed to generate tailored resume PDF: {e}")
                else:
                    st.info(
                        "Apply decision is No — skipping tailored resume generation."
                    )

                st.write("Finding LinkedIn contacts...")
                networking = None
                try:
                    networking = get_networking_service().find_people(
                        job=job,
                        discover_people=discover_people,
                    )
                except Exception as e:
                    st.warning(f"LinkedIn profile search failed: {e}")

                if networking is not None:
                    try:
                        if networking.people:
                            st.write("Drafting outreach messages...")
                            networking = draft_outreach_messages(
                                profile,
                                job,
                                networking,
                                job_summary=jd_summary,
                            )
                        render_networking_result(
                            networking, key_prefix=f"job-{i}"
                        )
                    except Exception as e:
                        st.warning(
                            f"Could not display LinkedIn contacts: {e}"
                        )

                st.markdown(f"[👉 Apply Here]({job.get("apply_link","")})")
                    #st.markdown(f"[👉 Apply Here]({r['job']['apply_link']})")

                              
                if tailored_resume:
                    add_to_vector_store = get_vector_store()
                    add_to_vector_store(
                        tailored_resume,
                        {
                            "type": "tailored_resume",
                            "job": job
                        }
                    )

                i+=1
            

                                





