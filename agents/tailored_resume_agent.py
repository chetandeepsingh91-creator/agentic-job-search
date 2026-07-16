from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(resume, job_description):
    prompt = load_prompt(
        "tailored_resume_prompt.md",
        resume=resume,
        job_description=job_description
    )
   
    return call_llm(prompt)