from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(job, resume):
    prompt = load_prompt(
        "application_prompt.md",
        resume=resume,
        job_description=job
    )
    return call_llm(prompt)
