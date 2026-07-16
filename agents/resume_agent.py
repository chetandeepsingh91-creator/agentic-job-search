from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(resume, jd, learning=None):
    prompt = load_prompt(
        "resume_prompt.md",
        resume=resume,
        job_description=jd
    )
    return call_llm(prompt)
