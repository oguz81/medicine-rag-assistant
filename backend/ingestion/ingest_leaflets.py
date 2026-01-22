# ingestion/ingest_leaflets.py

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DATA_DIR = Path("/home/oguz/MLProjects/medicine-rag-assistant/data/leaflets")
DB_DIR = "chroma_db_med"

def load_documents():
    docs = []
    for pdf_path in DATA_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()
        # Add metadata: which file
        for d in pdf_docs:
            d.metadata["source"] = pdf_path.name
        docs.extend(pdf_docs)
    return docs

def main():
    print("Loading PDFs...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents from PDFs.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY from env

    print("Creating Chroma DB...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    vectordb.persist()
    print(f"Saved vector DB to {DB_DIR}")

if __name__ == "__main__":
    main()

