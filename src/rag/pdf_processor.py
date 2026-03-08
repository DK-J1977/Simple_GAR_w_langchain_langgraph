"""
PDF processing module for extracting text and tables from PDF documents.
Supports both text extraction and table extraction using multiple libraries.
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

try:
    import pdfplumber
    import pypdf
    from pypdf import PdfReader
except ImportError as e:
    logging.error(f"Required PDF library not installed: {e}")
    raise

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Process PDF files to extract text and tables."""

    def __init__(self):
        """Initialize PDF processor."""
        self.supported_extensions = ['.pdf']

    def extract_text_pypdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as a string
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF from {pdf_path}: {e}")
            return ""

    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as a string
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber from {pdf_path}: {e}")
            return ""

    def extract_tables_pdfplumber(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using pdfplumber.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of dictionaries containing table data and metadata
        """
        tables_data = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables, 1):
                        if table:
                            # Convert table to text representation
                            table_text = self._table_to_text(table)
                            tables_data.append({
                                'page': page_num,
                                'table_number': table_num,
                                'data': table,
                                'text': table_text
                            })
        except Exception as e:
            logger.error(f"Error extracting tables from {pdf_path}: {e}")

        return tables_data

    def _table_to_text(self, table: List[List[str]]) -> str:
        """
        Convert a table (list of lists) to formatted text.

        Args:
            table: Table data as list of lists

        Returns:
            Formatted text representation of the table
        """
        if not table:
            return ""

        text_lines = []
        for row in table:
            # Clean and join cells
            clean_row = [str(cell).strip() if cell else "" for cell in row]
            text_lines.append(" | ".join(clean_row))

        return "\n".join(text_lines)

    def process_pdf(self, pdf_path: str, extract_tables: bool = True) -> Dict[str, Any]:
        """
        Process a PDF file and extract both text and tables.

        Args:
            pdf_path: Path to the PDF file
            extract_tables: Whether to extract tables (default: True)

        Returns:
            Dictionary containing extracted text and tables
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Try pdfplumber first (better for tables), fallback to pypdf
        text = self.extract_text_pdfplumber(pdf_path)
        if not text:
            logger.info("pdfplumber extraction failed, trying pypdf...")
            text = self.extract_text_pypdf(pdf_path)

        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'text': text,
            'tables': []
        }

        if extract_tables:
            result['tables'] = self.extract_tables_pdfplumber(pdf_path)

        return result

    def process_directory(self, directory_path: str, extract_tables: bool = True) -> List[Dict[str, Any]]:
        """
        Process all PDF files in a directory.

        Args:
            directory_path: Path to directory containing PDFs
            extract_tables: Whether to extract tables (default: True)

        Returns:
            List of dictionaries containing extracted data from all PDFs
        """
        results = []
        directory = Path(directory_path)

        for pdf_file in directory.glob("*.pdf"):
            logger.info(f"Processing {pdf_file.name}...")
            try:
                result = self.process_pdf(str(pdf_file), extract_tables=extract_tables)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")

        return results
