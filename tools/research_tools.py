import os
import io
import requests
import json
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_source: str) -> str:
    """Extracts text from a local PDF file path or a public PDF URL."""
    try:
        if pdf_source.startswith("http"):
            response = requests.get(pdf_source)
            f = io.BytesIO(response.content)
        else:
            f = open(pdf_source, "rb")
        
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return f"--- START OF PDF ({pdf_source}) ---\n{text[:8000]}... [Truncated for brevity]\n--- END OF PDF ---"
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def scrape_web_page(url: str) -> str:
    """Scrapes text content from a URL to gather research data."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")
        lines = (line.strip() for line in text.splitlines())
        content = "\n".join(line for line in lines if line)
        return f"--- START OF WEB PAGE ({url}) ---\n{content[:8000]}... [Truncated for brevity]\n--- END OF WEB PAGE ---"
    except Exception as e:
        return f"Error scraping web page: {str(e)}"

def list_available_resources() -> str:
    """
    Lists all local PDF research documents available in the 'resources' directory.
    Use this to see what internal data is available for scouting.
    """
    res_path = "resources"
    if not os.path.exists(res_path):
        return "No local resources directory found."
    
    files = [f for f in os.listdir(res_path) if f.endswith('.pdf')]
    if not files:
        return "No PDF documents found in resources."
    
    output = "Available Local Research PDFs:\n"
    for f in files:
        output += f"- resources/{f}\n"
    return output

def index_research_finding(topic: str, summary: str, source: str) -> str:
    """Saves a structured research finding to the Intelligence Bureau's Knowledge Base (kb.json)."""
    kb_path = "kb.json"
    data = []
    if os.path.exists(kb_path):
        with open(kb_path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    
    data.append({
        "topic": topic,
        "summary": summary,
        "source": source,
        "timestamp": "now"
    })
    
    with open(kb_path, "w") as f:
        json.dump(data, f, indent=4)
    
    return f"Successfully indexed finding for '{topic}' in kb.json"
