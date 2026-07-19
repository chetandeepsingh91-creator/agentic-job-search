from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(profile, jd_summary):
   
   prompt = load_prompt(
        "fit_prompt.md",
        resume=profile.resume,
        job_description=jd_summary
    )
    
   return call_llm(prompt)    
