import os
import sys
from unittest.mock import MagicMock

sys.modules['langchain_community.chat_models.vertexai'] = MagicMock()
sys.modules['langchain_community.embeddings.vertexai'] = MagicMock()

os.add_dll_directory(os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib'))

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

evaluator_llm = ChatOllama(model="gemma3:12b")
evaluator_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

data = {
    "question": ["What is the amount of deferred revenue?"],
    "answer": ["According to the provided text, the amounts of deferred revenue as of December 31, 2023 and 2022 were $3,536 million and $2,913 million respectively."],
    "contexts": [
        [
            "We record as deferred revenue any non-refundable amounts that are collected from customers related to fees charged for prepayments, which is recogni...",
            "$ 2,913 $ 2,382 Additions 1,201 1,178 Net changes in liability for pre-existing contracts 17 ( 67 ) Revenue recognized ( 595 ) ( 580 ) Defer..."
        ]
    ]
}

dataset = Dataset.from_dict(data)

print("\n--- Starting RAGAS Evaluation ---")
print("Evaluating Faithfulness and Answer Relevancy. Please wait...\n")

result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)

print("\n=== FINAL EVALUATION SCORES ===")
print(f"Faithfulness Score     : {result['faithfulness']}")
print(f"Answer Relevancy Score : {result['answer_relevancy']}")
print("===============================\n")