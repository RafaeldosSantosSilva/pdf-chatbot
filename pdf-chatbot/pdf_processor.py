import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def get_pdf_text(pdf_docs):
    """
    Extrai texto de múltiplos documentos PDF
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """
    Divide o texto em chunks menores para processamento
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_pdfs(raw_text):
    """
    Processa PDFs, criando embeddings e vector store
    """
    # Dividir texto em chunks
    text_chunks = get_text_chunks(raw_text)
    
    # Criar embeddings
    embeddings = OpenAIEmbeddings()
    
    # Criar vector store
    vector_store = FAISS.from_texts(
        texts=text_chunks, 
        embedding=embeddings
    )
    
    return vector_store