"""
Alt Print - Page Counter Service
Automatically counts pages for uploaded documents
"""
import io
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


async def count_pages(file_data: bytes, filename: str, content_type: str) -> Tuple[int, str]:
    """
    Count pages in an uploaded file.
    Returns: (page_count, file_type)
    file_type: one of 'pdf', 'docx', 'image'
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf" or content_type == "application/pdf":
        return await _count_pdf_pages(file_data), "pdf"

    if ext in ("docx", "doc") or content_type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        return await _count_docx_pages(file_data), "docx"

    if ext in ("png", "jpg", "jpeg") or content_type.startswith("image/"):
        return 1, "image"

    return 1, "unknown"


async def _count_pdf_pages(data: bytes) -> int:
    """Count pages in a PDF using pypdf"""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(data))
        return len(reader.pages)
    except Exception as e:
        logger.warning(f"PDF page count failed: {e}")
        return 1


async def _count_docx_pages(data: bytes) -> int:
    """
    Count pages in a DOCX.
    Uses python-docx to approximate: counts paragraphs / ~40 per page.
    For accurate count, we use the extended properties if available.
    """
    try:
        from docx import Document
        from docx.oxml.ns import qn

        doc = Document(io.BytesIO(data))

        # Try to get page count from document extended properties
        app_props = doc.core_properties
        # Extended props are in app.xml
        try:
            app_xml = doc.part.package.part_related_by(
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
            )
            from lxml import etree
            root = etree.fromstring(app_xml.blob)
            ns = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            pages_elem = root.find(f"{{{ns}}}Pages")
            if pages_elem is not None and pages_elem.text:
                return max(1, int(pages_elem.text))
        except Exception:
            pass

        # Fallback: estimate based on content
        paragraph_count = len(doc.paragraphs)
        estimated_pages = max(1, (paragraph_count + 39) // 40)
        return estimated_pages

    except Exception as e:
        logger.warning(f"DOCX page count failed: {e}")
        return 1
