from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(job, profile):
    prompt = load_prompt(
        "application_prompt.md",
        resume=profile.resume,
        job_description=job
    )
    return call_llm(prompt)
