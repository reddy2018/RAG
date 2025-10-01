# ingest.py
import os
from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Set OPENAI_API_KEY in environment (or .env)")

DATA_DIR = Path("data")
PERSIST_DIR = "chroma_db"

def load_documents(data_dir):
    docs = []
    for p in data_dir.glob("**/*"):
        if p.is_file() and p.suffix.lower() in (".md", ".txt"):
            loader = TextLoader(str(p), encoding="utf-8")
            docs.extend(loader.load())
    return docs

def main():
    docs = load_documents(DATA_DIR)
    print(f"Loaded {len(docs)} documents")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = splitter.split_documents(docs)
    print(f"Split into {len(docs)} chunks")

    embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY env var
    # Create and persist Chroma collection
    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=PERSIST_DIR)
    vectordb.persist()
    print("Ingestion complete. Vector DB persisted to", PERSIST_DIR)

if __name__ == "__main__":
    main()
