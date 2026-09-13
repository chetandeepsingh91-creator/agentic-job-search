import re
import unicodedata
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

from agents.resume_tailoring_agent import run as generate_tailored_resume

ACCENT_COLOR = "#1F4E79"
LINK_COLOR = "#0563C1"
TEXT_COLOR = "#2B2B2B"

SECTION_HEADERS = {
    "summary",
    "professional summary",
    "profile",
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "education",
    "skills",
    "technical skills",
    "core competencies",
    "certifications",
    "projects",
    "achievements",
    "additional information",
}


def _register_unicode_fonts() -> bool:
    try:
        import reportlab

        font_dir = Path(reportlab.__file__).parent / "fonts"
        pdfmetrics.registerFont(
            TTFont("DejaVuSans", str(font_dir / "DejaVuSans.ttf"))
        )
        pdfmetrics.registerFont(
            TTFont("DejaVuSans-Bold", str(font_dir / "DejaVuSans-Bold.ttf"))
        )
        return True
    except Exception:
        return False


_UNICODE_FONTS = _register_unicode_fonts()


def _normalize_decision_text(decision: str) -> str:
    text = decision.lower()
    text = re.sub(r"\*+", "", text)
    return text


def is_apply_yes(decision: str) -> bool:
    if not decision or decision.startswith("Error:"):
        return False

    text = _normalize_decision_text(decision)

    apply_answer = re.search(
        r"should\s+(?:the\s+)?candidate\s+apply\s*\??\s*(yes|no)\b",
        text,
        re.IGNORECASE,
    )
    if apply_answer:
        return apply_answer.group(1).lower() == "yes"

    first_answer = re.search(
        r"^\s*(?:\d+\.\s*)?(yes|no)\b",
        text.strip(),
        re.IGNORECASE,
    )
    if first_answer:
        return first_answer.group(1).lower() == "yes"

    return False


def sanitize_filename_part(value: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", (value or "").strip())
    cleaned = re.sub(r"[\s_]+", "_", cleaned)
    return cleaned[:50] or "unknown"


def build_resume_filename(company: str, job_title: str) -> str:
    company_part = sanitize_filename_part(company)
    title_part = sanitize_filename_part(job_title)
    return f"tailored_resume_{company_part}_{title_part}.pdf"


def _clean_resume_text(resume_text: str) -> str:
    text = unicodedata.normalize("NFKC", resume_text or "")

    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "-",
        "\u2023": "-",
        "\u2043": "-",
        "\u00b7": "-",
        "\u202f": " ",
        "\u00a0": " ",
        "\u200b": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[`_~]", "", text)

    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "• ", "* ", "– ")):
            stripped = "- " + stripped[2:].strip()
        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines).strip()


def _linkify_text(text: str) -> str:
    safe = escape(text)

    def _mailto(match):
        email = match.group(1)
        return (
            f'<a href="mailto:{email}" color="{LINK_COLOR}">{email}</a>'
        )

    def _url(match):
        url = match.group(1)
        return f'<a href="{url}" color="{LINK_COLOR}">{url}</a>'

    def _linkedin(match):
        path = match.group(1)
        url = f"https://www.linkedin.com/{path}"
        label = f"linkedin.com/{path}"
        return f'<a href="{url}" color="{LINK_COLOR}">{label}</a>'

    def _github(match):
        path = match.group(1)
        url = f"https://github.com/{path}"
        label = f"github.com/{path}"
        return f'<a href="{url}" color="{LINK_COLOR}">{label}</a>'

    safe = re.sub(
        r"\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b",
        _mailto,
        safe,
    )
    safe = re.sub(r"\b(https?://[^\s<]+)", _url, safe)
    safe = re.sub(
        r"\b(linkedin\.com/(?:in|company)/[^\s|]+)",
        _linkedin,
        safe,
        flags=re.IGNORECASE,
    )
    safe = re.sub(
        r"\b(github\.com/[^\s|]+)",
        _github,
        safe,
        flags=re.IGNORECASE,
    )
    return safe


def _classify_line(line: str, line_index: int) -> str:
    stripped = line.strip()
    if not stripped:
        return "blank"

    lower = stripped.lower().rstrip(":")

    if line_index == 0 and len(stripped) < 80 and "@" not in stripped:
        return "name"

    if line_index <= 2 and (
        "@" in stripped
        or re.search(r"\+?\d[\d\s().-]{7,}\d", stripped)
        or "linkedin.com" in lower
        or "github.com" in lower
    ):
        return "contact"

    if lower in SECTION_HEADERS or (
        stripped.isupper() and 3 < len(stripped) < 50
    ):
        return "section"

    if stripped.startswith("- "):
        return "bullet"

    if stripped.endswith(":") and len(stripped) < 70:
        return "subsection"

    if re.match(r"^[A-Z][^a-z]{0,3}[A-Za-z].*\|\s*.+", stripped):
        return "role"

    return "body"


def _build_pdf_styles():
    base_font = "DejaVuSans" if _UNICODE_FONTS else "Helvetica"
    bold_font = "DejaVuSans-Bold" if _UNICODE_FONTS else "Helvetica-Bold"
    styles = getSampleStyleSheet()
    accent = colors.HexColor(ACCENT_COLOR)
    body = colors.HexColor(TEXT_COLOR)
    link = colors.HexColor(LINK_COLOR)

    return {
        "name": ParagraphStyle(
            "ResumeName",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=18,
            leading=22,
            textColor=accent,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "contact": ParagraphStyle(
            "ResumeContact",
            parent=styles["BodyText"],
            fontName=base_font,
            fontSize=9.5,
            leading=12,
            textColor=body,
            linkColor=link,
            spaceAfter=12,
        ),
        "section": ParagraphStyle(
            "ResumeSection",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=11,
            leading=14,
            textColor=accent,
            spaceBefore=8,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "subsection": ParagraphStyle(
            "ResumeSubsection",
            parent=styles["Heading3"],
            fontName=bold_font,
            fontSize=10.5,
            leading=13,
            textColor=accent,
            spaceBefore=4,
            spaceAfter=2,
        ),
        "role": ParagraphStyle(
            "ResumeRole",
            parent=styles["BodyText"],
            fontName=bold_font,
            fontSize=10,
            leading=13,
            textColor=body,
            spaceBefore=2,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=styles["BodyText"],
            fontName=base_font,
            fontSize=10,
            leading=13,
            textColor=body,
            linkColor=link,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "ResumeBullet",
            parent=styles["BodyText"],
            fontName=base_font,
            fontSize=10,
            leading=13,
            textColor=body,
            linkColor=link,
            leftIndent=14,
            bulletIndent=0,
            spaceAfter=2,
        ),
    }


def _section_rule():
    return HRFlowable(
        width="100%",
        thickness=0.75,
        color=colors.HexColor(ACCENT_COLOR),
        spaceBefore=1,
        spaceAfter=8,
    )


def _resume_text_to_pdf_bytes(resume_text: str) -> bytes:
    cleaned_text = _clean_resume_text(resume_text)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )
    pdf_styles = _build_pdf_styles()
    content = []
    non_empty_index = 0

    for line in cleaned_text.splitlines():
        stripped = line.strip()
        if not stripped:
            content.append(Spacer(1, 6))
            continue

        line_type = _classify_line(stripped, non_empty_index)
        non_empty_index += 1

        if line_type == "section":
            content.append(Paragraph(escape(stripped), pdf_styles["section"]))
            content.append(_section_rule())
        elif line_type == "bullet":
            paragraph_text = _linkify_text(stripped[2:].strip())
            content.append(
                Paragraph(
                    f'<font color="{ACCENT_COLOR}">&bull;</font> {paragraph_text}',
                    pdf_styles["bullet"],
                )
            )
        elif line_type in ("contact", "body"):
            content.append(
                Paragraph(_linkify_text(stripped), pdf_styles[line_type])
            )
        else:
            content.append(
                Paragraph(escape(stripped), pdf_styles[line_type])
            )

    doc.build(content)
    return buffer.getvalue()


def generate_tailored_resume_pdf(
    profile,
    job_description,
    company: str = "",
    job_title: str = "",
):
    resume_text = generate_tailored_resume(profile, job_description)

    if not resume_text or resume_text.startswith("Error:"):
        raise ValueError(
            resume_text or "Tailored resume generation returned no content."
        )

    pdf_bytes = _resume_text_to_pdf_bytes(resume_text)
    filename = build_resume_filename(company, job_title)
    return pdf_bytes, filename, resume_text
