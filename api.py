import os
import sys
os.add_dll_directory(os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib'))

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


app = FastAPI(title="OmniDoc-RAG API")

class QueryRequest(BaseModel):
    question: str

class SourceInfo(BaseModel):
    file_name: str
    page_num: int
    score: float
    snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]

print("Initializing OmniDoc-RAG Pipeline... Please wait.")

vectorstore = None
vector_retriever = None
bm25_retriever = None
chunks = []

pdf_path = "data/report.pdf"
if os.path.exists(pdf_path):
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


prompt_template = """You are a precise AI assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question at the end. 
If the answer cannot be found completely within the provided context, you MUST output exact text: 
"The answer is not available in the provided documents."
Do not add any extra explanations, sentences, or guesses.

Context:
{context}

Question: {question}
Helpful Answer:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
llm = ChatOllama(model="gemma3:12b")
chain = prompt | llm

print("OmniDoc-RAG Pipeline Ready! Server is running.")

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    global vectorstore, vector_retriever, bm25_retriever, chunks
    os.makedirs("data", exist_ok=True)
    
    all_chunks = []
    filenames = []
    
    for file in files:
        file_path = os.path.join("data", file.filename)
        filenames.append(file.filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif file.filename.endswith(".csv"):
            loader = CSVLoader(file_path)
        else:
            continue 
            
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
        all_chunks.extend(text_splitter.split_documents(documents))
        
    if all_chunks:
        chunks = all_chunks
        
        embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory="chroma_db")
        
        vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        bm25_retriever = BM25Retriever.from_documents(chunks)
        bm25_retriever.k = 5
    
    return {"message": "Documents processed successfully", "filenames": filenames}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    global vector_retriever, bm25_retriever
    if not vector_retriever or not bm25_retriever:
        return QueryResponse(answer="Please upload and process a document first.", sources=[])
        
    query = request.question
    
    vector_results = vector_retriever.invoke(query)
    bm25_results = bm25_retriever.invoke(query)

    unique_docs = {}
    for doc in vector_results + bm25_results:
        if doc.page_content not in unique_docs:
            unique_docs[doc.page_content] = doc

    combined_results = list(unique_docs.values())
    if not combined_results:
        return QueryResponse(answer="The answer is not available in the provided documents.", sources=[])

    pairs = [[query, doc.page_content] for doc in combined_results]
    
    scores = cross_encoder.predict(pairs)
    scored_docs = zip(scores, combined_results)
    sorted_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)
    top_3_docs = sorted_docs[:3]

    context_parts = []
    sources = []
    
    for score, doc in top_3_docs:
        page_num = doc.metadata.get('page', 0) + 1 
        
        source_path = doc.metadata.get('source', 'Unknown Document')
        file_name = os.path.basename(source_path)
        
        context_parts.append(f"--- Document: {file_name} | Page {page_num} ---\n{doc.page_content}")
        
        snippet = doc.page_content[:150].replace('\n', ' ') + "..."
        sources.append(SourceInfo(file_name=file_name, page_num=page_num, score=float(score), snippet=snippet))
        
    context_text = "\n\n".join(context_parts)

    response = chain.invoke({"context": context_text, "question": query})
    
    answer_text = response.content if hasattr(response, 'content') else str(response)

    # --- Backend Post-processing Logic (ලේඛනයේ නැතිනම් නිවැරදි කිරීම සඳහා) ---
    lower_answer = answer_text.lower()
    if any(phrase in lower_answer for phrase in ["don't know", "not available", "not contain", "no information", "cannot find", "do not contain", "discuss"]):
        answer_text = "The answer is not available in the provided documents."
        sources = []  # උත්තරයක් නැති විට Sources පෙන්වීම සම්පූර්ණයෙන්ම වළකයි

    return QueryResponse(answer=answer_text, sources=sources)