import os
import docx
import PyPDF2


class DocumentParser:
    """
    Handles extracting text from different document types.
    """

    def __init__(self):
        pass

    def parse_document(self, file_path: str) -> str:
        """
        Chooses the correct method to extract text based on file extension.
        Returns the extracted text as a string.
        """
        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return self._parse_pdf(file_path)
        elif extension == ".docx":
            return self._parse_docx(file_path)
        elif extension == ".txt":
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

    def _parse_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _parse_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)

    def _parse_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def parse_document(file_path):
    parser = DocumentParser()
    doc = parser.parse_document(file_path)
    return doc