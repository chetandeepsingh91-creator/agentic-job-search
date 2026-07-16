import time

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

role = st.text_input("🎯 Target Role", value="Product Manager")

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
        st.warning("Please add resume")
    else:
        with st.spinner("Finding and evaluating jobs..."):

            jobs = jobs_crawler_agent.run(role)
            #st.write(jobs)
            # results = []
            final_results = []
            
            

            for job in jobs:
                jd = job.get("description", "")
                    
                jd_summary = job_understanding_agent.run(jd)

                #st.write(f"📊 Job Summary: {jd_summary}")

                fit = fit_agent.run(resume, jd_summary)
                
                decision = apply_decision_agent.run(jd_summary, fit)
                
                tailored_resume = tailored_resume_agent.run(resume, jd_summary)
                
                final_results.append({
                "job": job,
                "fit": fit,
                "decision": decision,
                # "application": application_content,
                "tailored_resume": tailored_resume
                })
                
                add_to_vector_store = get_vector_store()
                add_to_vector_store(
                    tailored_resume,
                    {
                        "type": "tailored_resume",
                        "job": job
                    }
                )
            

                
            # ranking = ranking_agent(results)
                
            # st.subheader("📊 Job Rankings")
            # st.write(ranking)

            for r in final_results:
                st.markdown("---")
                st.subheader(f"{r['job']['title']} at {r['job']['company']}")

                st.write("📊 Fit:")
                st.write(r["fit"])

                st.write("🧠 Apply Decision:")
                st.write(r["decision"])

                # st.write("✍️ Application Content:")
                # st.write(r["application"])

                st.write("📄 Tailored Resume:")
                st.write(r["tailored_resume"])
                
                # Apply link (if available)
                if "apply_link" in r["job"]:
                    st.markdown(f"[👉 Apply Here]({r['job']['apply_link']})")
                                

            # # Step 3
            # learning_insights = learning_agent()
            # improved_resume = resume_agent(resume, jd, learning_insights)

        # Display
        # st.subheader("🧠 Job Understanding")
        # st.write(jd_summary)

        # st.subheader("📊 Fit Analysis")
        # st.write(fit_analysis)
        
        # st.subheader("✍️ Resume Optimization")
        # st.write(improved_resume)
        
        # st.subheader("🧠 Learning Insights")
        # st.write(learning_insights)
        
        



