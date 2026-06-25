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
    """Read PDF with OCR fallback for scanned documents."""
    text = ""
    
    # Try PyMuPDF first
    try:
        import fitz
        doc = fitz.open(path)
        texts = []
        for page in doc:
            t = page.get_text()
            if t.strip():
                texts.append(t)
        doc.close()
        if texts and any(len(t) > 50 for t in texts):
            return '\n\n'.join(texts)
    except ImportError:
        pass
    
    # Try pypdf as second fallback
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        texts = []
        for page in reader.pages:
            t = page.extract_text()
            if t.strip():
                texts.append(t)
        if texts and any(len(t) > 50 for t in texts):
            return '\n\n'.join(texts)
    except ImportError:
        pass
    
    # OCR fallback for scanned PDFs
    try:
        import pytesseract
        from PIL import Image
        import io
        
        # Try PyMuPDF for rendering
        import fitz
        doc = fitz.open(path)
        texts = []
        for i, page in enumerate(doc):
            # Render page to image
            pix = page.get_pixmap(dpi=200)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            # OCR
            t = pytesseract.image_to_string(img, lang='chi_sim+eng')
            if t.strip():
                texts.append(f"[OCR Page {i+1}]\n{t}")
        doc.close()
        if texts:
            return '\n\n'.join(texts)
    except ImportError:
        pass
    except Exception as e:
        pass
    
    # Ultimate fallback
    if not text:
        # Try pdfminer
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(path)
            if text.strip():
                return text
        except ImportError:
            pass
    
    return text or "[无法提取文本]"

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
