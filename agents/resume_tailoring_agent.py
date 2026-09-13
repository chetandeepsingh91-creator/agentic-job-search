from services.prompt_service import load_prompt
from services.llm_service import call_llm


def run(profile, job_description):
    prompt = load_prompt(
        "tailored_resume_prompt.md",
        resume=profile.resume,
        job_description=job_description,
    )

    return call_llm(prompt)
