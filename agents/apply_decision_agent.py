from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(profile, job, fit_analysis):
    prompt = load_prompt(
        "apply_decision_prompt.md",
        profile=profile,
        job=job,
        fit_analysis=fit_analysis
    )
    return call_llm(prompt)
