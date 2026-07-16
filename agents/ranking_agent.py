from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run(results):
    prompt = load_prompt(
        "ranking_prompt.md",
        results=results
    )
    return call_llm(prompt)    
