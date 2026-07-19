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
    tailored_resume_agent,
    apply_decision_agent,
    ranking_agent,
    jobs_crawler_agent
)

# from memory import (
    # add_to_memory,
    # load_memory,
    # save_memory
# )

print("Imports done:", time.time() - start)

st.set_page_config(page_title="AI Job Agent", layout="wide")

st.title("🤖 Multi-Agent Job Search System")

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
            #st.write(jobs)
            # results = []
            final_results = []
            
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

                st.write("Generating Tailored Resume...")
                tailored_resume = tailored_resume_agent.run(profile, jd_summary)
                st.write("📄 Tailored Resume:")
                st.write(tailored_resume)

                
                st.markdown(f"[👉 Apply Here]({job.get("apply_link","")})")
                    #st.markdown(f"[👉 Apply Here]({r['job']['apply_link']})")

                              
                add_to_vector_store = get_vector_store()
                add_to_vector_store(
                    tailored_resume,
                    {
                        "type": "tailored_resume",
                        "job": job
                    }
                )

                i+=1
            

                                





