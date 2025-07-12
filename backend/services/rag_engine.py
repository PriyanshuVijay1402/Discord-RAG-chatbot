import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from loguru import logger

load_dotenv()

# Step 1: Load documents
def load_documents(data_dir=None):
    if data_dir is None:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    docs = []
    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            continue
        logger.info(f"Loaded document: {filename}")
        docs.extend(loader.load())

    logger.info(f"Total documents loaded: {len(docs)}")
    if docs:
        logger.info(f"Sample content: {docs[0].page_content[:300]}")
    return docs

# Step 2: Build Chroma vector DB
def build_vector_store():
    logger.info("Building new vector store...")
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    logger.info(f"Total chunks created: {len(chunks)}")

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        chunks,
        embedding=embedding,
        persist_directory="chroma_db"
    )
    return vectordb

# Step 3: Load or rebuild Chroma DB
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
if os.path.exists("chroma_db"):
    try:
        vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding
        )
        retriever = vectordb.as_retriever()
        logger.info("Vector store loaded from disk.")
    except Exception as e:
        logger.warning(f"Failed to load vector DB, rebuilding... ({e})")
        vectordb = build_vector_store()
        retriever = vectordb.as_retriever()
else:
    vectordb = build_vector_store()
    retriever = vectordb.as_retriever()

# Step 4: Initialize OpenRouter-compatible LLM
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",  # You can swap this with another OpenRouter model
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
    max_tokens=1024
)

# Step 5: Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Step 6: RAG API function
def get_rag_answer(query: str) -> str:
    logger.info(f"RAG answering: {query}")
    try:
        result = qa_chain.invoke(query)
        sources = [doc.metadata.get("source", "N/A") for doc in result.get("source_documents", [])]
        logger.info(f"Sources: {sources}")
        return result["result"]
    except Exception as e:
        logger.error(f"RAG failed: {e}")
        return "Sorry, something went wrong."
