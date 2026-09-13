import re

from models.networking import DiscoveredPerson, NetworkingResult
from services.llm_service import call_llm
from services.prompt_service import load_prompt


def _job_field(job, key: str) -> str:
    if not isinstance(job, dict):
        return ""
    return (job.get(key) or "").strip()


def _first_name(full_name: str) -> str:
    if not full_name:
        return "there"
    return full_name.strip().split()[0]


def _contact_context(
    person: DiscoveredPerson, company: str, job_title: str
) -> str:
    snippet = (person.snippet or "").strip()
    if snippet:
        return f"your background in {snippet[:70].rstrip('.,;')}"

    title = (person.title or "").strip().replace(" | LinkedIn", "")
    parts = [part.strip() for part in title.split(" - ") if part.strip()]
    role_part = parts[1] if len(parts) > 1 else ""

    if (
        role_part
        and role_part.lower() not in ("linkedin", "linkedin profile")
        and role_part.lower() != job_title.lower()
    ):
        return f"your experience as {role_part}"

    contact_type = (person.target_type or "").lower()
    if contact_type == "recruiter":
        return f"your recruiting work at {company}" if company else "your recruiting work"
    if contact_type == "hiring manager":
        return f"your leadership at {company}" if company else "your leadership on the team"

    return f"your work at {company}" if company else "your experience in the space"


def _fallback_message(profile, job, person: DiscoveredPerson) -> str:
    company = _job_field(job, "company") or "your company"
    title = _job_field(job, "title") or "the open role"
    first_name = _first_name(person.name)
    context = _contact_context(person, company, title)

    return (
        f"Hi {first_name}, I'm interested in the {title} role at {company}. "
        f"I'd appreciate connecting — {context} stood out to me."
    )[:280]


def _clean_llm_message(content: str) -> str:
    if not content or content.startswith("Error:"):
        return ""

    message = content.strip()
    message = re.sub(r"^```(?:text)?\s*", "", message)
    message = re.sub(r"\s*```$", "", message)
    message = message.strip().strip('"').strip("'")
    return message[:280]


def _draft_single_message(
    profile,
    job,
    person: DiscoveredPerson,
    job_summary: str = "",
):
    prompt = load_prompt(
        "outreach_single_prompt.md",
        name=getattr(profile, "name", ""),
        preferred_roles=", ".join(getattr(profile, "preferred_roles", []) or []),
        skills=", ".join(getattr(profile, "skills", []) or []),
        job_title=_job_field(job, "title"),
        job_company=_job_field(job, "company"),
        job_location=_job_field(job, "location"),
        job_summary=job_summary or _job_field(job, "description"),
        contact_name=person.name or "there",
        contact_title=person.title or "",
        contact_type=person.target_type or "team member",
        contact_snippet=person.snippet or "",
    )

    content = call_llm(prompt, temperature=0.4)
    return _clean_llm_message(content)


def draft_outreach_messages(
    profile,
    job,
    result: NetworkingResult,
    job_summary: str = "",
):
    if not result.people:
        return result

    for person in result.people:
        message = _draft_single_message(profile, job, person, job_summary)
        person.outreach_message = message or _fallback_message(
            profile, job, person
        )

    return result
