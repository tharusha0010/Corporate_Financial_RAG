import os
import sys
os.add_dll_directory(os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib'))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

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

context_text = "\n\n".join([doc.page_content for score, doc in sorted_docs[:3]])

prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Helpful Answer:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

llm = ChatOllama(model="gemma3:12b")
chain = prompt | llm

print(f"\nQuery: {query}")
print("\nGenerating answer via Gemma 3...\n")
response = chain.invoke({"context": context_text, "question": query})

print("--- Final Answer ---")
print(response.content)
print("--------------------")