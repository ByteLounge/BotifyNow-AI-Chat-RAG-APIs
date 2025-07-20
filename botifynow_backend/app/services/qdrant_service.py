import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Filter, FieldCondition, MatchValue
import uuid
import os

# ✅ OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Qdrant in-memory DB
qdrant = QdrantClient(":memory:")

COLLECTION_NAME = "documents"

# ✅ Create collection if not exists
def create_collection():
    existing_collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing_collections:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance="Cosine")  # stays 1536 for new embeddings too
        )

# ✅ Generate unique document ID
def generate_doc_id():
    return str(uuid.uuid4())

# ✅ Generate OpenAI embeddings
def embed_text(text: str):
    try:
        embedding = openai.Embedding.create(
            model="text-embedding-3-small",  # ✅ Supported in all new projects
            input=text
        )
        return embedding["data"][0]["embedding"]
    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")

# ✅ Store document in Qdrant
def store_document(doc_id: str, text: str):
    create_collection()
    vector = embed_text(text)
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"doc_id": doc_id, "text": text}
            )
        ]
    )

# ✅ Search documents with optional filtering
def search_document(query: str, document_id: str = None):
    create_collection()
    query_vector = embed_text(query)

    query_filter = None
    if document_id:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="doc_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )

    search_result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3,
        query_filter=query_filter
    )

    return " ".join([hit.payload["text"] for hit in search_result])
