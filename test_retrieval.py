import os
import sys
os.add_dll_directory(os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib'))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder

pdf_path = "data/report.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
chunks = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

query = "What is the total revenue?"

vector_results = vector_retriever.invoke(query)
bm25_results = bm25_retriever.invoke(query)

unique_docs = {}
for doc in vector_results + bm25_results:
    if doc.page_content not in unique_docs:
        unique_docs[doc.page_content] = doc

combined_results = list(unique_docs.values())

pairs = [[query, doc.page_content] for doc in combined_results]
scores = cross_encoder.predict(pairs)

scored_docs = zip(scores, combined_results)
sorted_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)

print(f"\nQuery: {query}")
print("\nTop 3 Reranked Results:\n")
for i, (score, doc) in enumerate(sorted_docs[:3]):
    print(f"--- Result {i+1} (Score: {score:.4f}) ---")
    print(doc.page_content)
    print("-" * 50)