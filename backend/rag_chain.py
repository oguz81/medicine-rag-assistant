# backend/rag_chain.py

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

DB_DIR = "chroma_db_med"

def get_qa_chain():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    system_prompt = """
You are a cautious assistant that answers questions ONLY using the provided medicine
leaflet text. You DO NOT give medical diagnosis or personalized medical advice.
You only restate what is in the leaflets in simple language.

Rules:
- If the answer is not clearly in the context, say you don't know.
- Always remind: "This is not medical advice. Consult a doctor or pharmacist."
- Cite which document(s) you used if possible.
"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            system_prompt +
            "\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer in a careful, neutral tone:"
        ),
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    return chain

def answer_question(question: str):
    chain = get_qa_chain()
    result = chain({"query": question})
    answer = result["result"]
    sources = list({doc.metadata.get("source", "unknown") for doc in result["source_documents"]})
    return answer, sources

