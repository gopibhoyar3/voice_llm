import os
import numpy as np
import faiss
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, CSVLoader, JSONLoader, PyPDFLoader

load_dotenv()

embedding_dim = 1536
index = faiss.IndexFlatL2(embedding_dim)

documents = []
embeddings_model = OpenAIEmbeddings()

def load_and_split_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    elif ext == ".json":
        loader = JSONLoader(file_path)
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"❌ Unsupported file type: {ext}")

    raw_docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(raw_docs)

    if not split_docs:
        raise ValueError("❌ No content extracted from document.")
    
    return split_docs

def index_document(file_path: str):
    global documents

    chunks = load_and_split_file(file_path)
    chunk_texts = [chunk.page_content for chunk in chunks]

    if not chunk_texts:
        raise ValueError("❌ No text found to index.")

    print(f"📄 Indexing {len(chunk_texts)} chunks from {file_path}")

    embeddings = embeddings_model.embed_documents(chunk_texts)
    vectors_np = np.array(embeddings, dtype=np.float32)

    index.add(vectors_np)
    documents.extend(chunk_texts)

def retrieve_relevant_chunks(query: str, top_k: int = 3):
    if not documents:
        raise ValueError("❌ No documents indexed yet.")

    query_embedding = embeddings_model.embed_query(query)
    query_vector = np.array([query_embedding], dtype=np.float32)

    distances, indices = index.search(query_vector, top_k)
    relevant_chunks = [documents[i] for i in indices[0] if i < len(documents)]

    print(f"🔎 Retrieved top {len(relevant_chunks)} relevant chunks for query: {query}")
    return relevant_chunks
