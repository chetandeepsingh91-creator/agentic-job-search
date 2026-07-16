from pathlib import Path


PROMPTS_DIR = Path("prompts")


def load_prompt(prompt_file: str, **kwargs) -> str:
    """
    Load a prompt template and replace placeholders.

    Example:
        load_prompt(
            "fit_prompt.md",
            resume=resume_text,
            job_description=jd_text
        )
    """

    file_path = PROMPTS_DIR / prompt_file

    with open(file_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

    return prompt