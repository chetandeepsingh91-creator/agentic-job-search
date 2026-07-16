from pathlib import Path
from pypdf import PdfReader
from docx import Document


class ResumeParser:

    @staticmethod
    def extract_text(uploaded_file):

        suffix = Path(uploaded_file.name).suffix.lower()

        if suffix == ".pdf":
            return ResumeParser._extract_pdf(uploaded_file)

        elif suffix == ".docx":
            return ResumeParser._extract_docx(uploaded_file)

        else:
            raise ValueError("Unsupported file type.")

    @staticmethod
    def _extract_pdf(file):

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    @staticmethod
    def _extract_docx(file):

        document = Document(file)

        paragraphs = []

        for p in document.paragraphs:
            paragraphs.append(p.text)

        return "\n".join(paragraphs)