import time

start = time.time()
print("App start...")

import streamlit as st

@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")
    
def get_vector_store():
    from vector_store import add_to_vector_store
    return add_to_vector_store
    
    
from agents import job_understanding_agent, fit_agent, resume_agent, learning_agent, job_crawler_agent, ranking_agent, apply_decision_agent, application_agent, tailored_resume_agent
from memory import add_to_memory

print("Imports done:", time.time() - start)

st.set_page_config(page_title="AI Job Agent", layout="wide")

st.title("🤖 Multi-Agent Job Search System")

role = st.text_input("🎯 Target Role", value="Product Manager")

resume = st.text_area("📄 Paste Resume", height=250)

if st.button("Run AI Job Copilot 🚀"):

    if not resume:
        st.warning("Please add resume")
    else:
        with st.spinner("Finding and evaluating jobs..."):

            jobs = job_crawler_agent(role)
            st.write(jobs)
            # results = []
            final_results = []
            
            

            for job in jobs:
                jd = job.get("description", "")
                    
                jd_summary = job_understanding_agent(jd)
                fit = fit_agent(resume, jd_summary)
                
                decision = apply_decision_agent(job, fit)
                
                tailored_resume = tailored_resume_agent(resume, jd_summary)
                
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
        
        



