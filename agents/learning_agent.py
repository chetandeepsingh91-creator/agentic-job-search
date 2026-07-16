from memory import load_memory
from services.prompt_service import load_prompt
from services.llm_service import call_llm

def run():
    memory = load_memory()

    if len(memory) < 2:
        return "Not enough data to learn yet."

    recent_data = memory[-5:]

    prompt = load_prompt(
        "learning_prompt.md",
        recent_data=recent_data
    )

    return call_llm(prompt)
