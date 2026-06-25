"""BookMind — 多格式电子书解析器"""
import os
import re

def read_file(path: str) -> str:
    """Auto-detect format and extract text."""
    ext = os.path.splitext(path)[1].lower()
    
    if ext == '.txt':
        return _read_txt(path)
    elif ext == '.epub':
        return _read_epub(path)
    elif ext == '.pdf':
        return _read_pdf(path)
    elif ext in ('.md', '.markdown'):
        return _read_txt(path)
    else:
        raise ValueError(f"Unsupported format: {ext}")

def _read_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def _read_pdf(path: str) -> str:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(path)
        text = []
        for page in doc:
            text.append(page.get_text())
        doc.close()
        return '\n\n'.join(text)
    except ImportError:
        # Fallback to pypdf
        from pypdf import PdfReader
        reader = PdfReader(path)
        return '\n\n'.join(page.extract_text() for page in reader.pages)

def _read_epub(path: str) -> str:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    
    book = epub.read_epub(path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            # Remove scripts and styles
            for tag in soup(['script', 'style']):
                tag.decompose()
            text = soup.get_text(separator='\n')
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = text.strip()
            if text:
                chapters.append(text)
    return '\n\n---\n\n'.join(chapters)

def chunk_text(text: str, max_chars: int = 3000) -> list[str]:
    """Split text into chunks for processing."""
    paragraphs = text.split('\n\n')
    chunks = []
    current = []
    current_len = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current_len + len(para) > max_chars and current:
            chunks.append('\n\n'.join(current))
            current = []
            current_len = 0
        current.append(para)
        current_len += len(para)
    
    if current:
        chunks.append('\n\n'.join(current))
    
    return chunks if chunks else [text[:max_chars]]
