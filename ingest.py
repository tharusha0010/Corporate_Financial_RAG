import os
import sys
os.add_dll_directory(os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib'))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

pdf_path = "data/report.pdf"
print(f"Loading document from: {pdf_path}...")

try:
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Successfully loaded {len(documents)} pages from the PDF.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    print("Splitting the document into chunks...")
    chunks = text_splitter.split_documents(documents)
    print(f"Document successfully split into {len(chunks)} chunks.")

    print("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    persist_directory = "chroma_db"
    print(f"Creating vector database at {persist_directory}...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    print("Data Ingestion and Vector Storage completed successfully!")

except Exception as e:
    print(f"An error occurred: {e}")