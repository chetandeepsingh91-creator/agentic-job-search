from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(jd):
    prompt = load_prompt(
        "job_understanding_prompt.md",
         job_description=jd
    )
    
    return call_llm(prompt)
