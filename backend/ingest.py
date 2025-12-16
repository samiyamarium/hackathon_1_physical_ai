import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import google.generativeai as genai

# =========================
# LOAD .env
# =========================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "book_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

TOP_K = 4

# =========================
# EMBEDDING MODEL
# =========================
embedder = SentenceTransformer(EMBEDDING_MODEL)

# =========================
# QDRANT CLIENT
# =========================
if QDRANT_URL and QDRANT_API_KEY:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), "vectorstore")
    qdrant = QdrantClient(path=VECTORSTORE_PATH)

# =========================
# GEMINI CONFIG (optional)
# =========================
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# =========================
# CHATBOT CLASS
# =========================
class Chatbot:
    def __init__(self):
        collections = [c.name for c in qdrant.get_collections().collections]
        if QDRANT_COLLECTION not in collections:
            raise RuntimeError("Vector collection not found. Run ingest.py first.")

    def ask(self, question: str):
        query_vector = embedder.encode(question).tolist()
        results = qdrant.search(collection_name=QDRANT_COLLECTION, query_vector=query_vector, limit=TOP_K)

        if not results:
            return {"answer": "I could not find relevant information in the book."}

        context = "\n\n".join(hit.payload["text"] for hit in results)

        # Optional: add Gemini summary if API key is present
        if GEMINI_API_KEY:
            response = genai.chat(messages=[{"content": f"Answer the question concisely using this context:\n{context}\nQuestion: {question}"}])
            answer = response.last
        else:
            answer = context

        return {"question": question, "answer": answer}
