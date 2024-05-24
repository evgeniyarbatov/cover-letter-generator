import requests

from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

from langchain.text_splitter import RecursiveCharacterTextSplitter

def pdf_text(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()   
    return text

def url_text(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

    text = []
    for lines in soup.findAll('div', {'class': 'description__text'}):
        text.append(lines.get_text())
    
    lines = (line.strip() for line in text)
    text = '\n'.join(line for line in lines if line)   

    return text

def get_documents(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap  = 0, length_function = len, add_start_index = True,)
    return splitter.create_documents([text])