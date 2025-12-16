from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import os

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(__file__)
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore")
COLLECTION_NAME = "book_docs"
TOP_K = 4

# =========================
# LOAD EMBEDDING MODEL
# =========================
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# VECTOR DB
# =========================
qdrant = QdrantClient(path=VECTORSTORE_PATH)

# =========================
# CHATBOT CLASS
# =========================
class Chatbot:
    def __init__(self):
        collections = [c.name for c in qdrant.get_collections().collections]
        if COLLECTION_NAME not in collections:
            raise RuntimeError(
                "Vector collection not found. Please run ingest.py first."
            )

    def ask(self, question: str):
        query_vector = embedder.encode(question).tolist()

        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=TOP_K
        )

        if not results:
            return {
                "answer": "I could not find relevant information in the book."
            }

        context = "\n\n".join(
            hit.payload["text"] for hit in results
        )

        # Simple extractive answer (offline & free)
        return {
            "question": question,
            "answer": context
        }
