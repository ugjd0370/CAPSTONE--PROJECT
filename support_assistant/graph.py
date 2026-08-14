from pathlib import Path
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from .prompt import PROMPT_TEMPLATE


# CONFIGURATION

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "zepto_policies"

# LOAD EMBEDDING MODEL

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# CONNECT TO CHROMADB

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

# LANGGRAPH STATE

class SupportState(TypedDict, total=False):
    query: str
    context: str
    sources: list[str]
    answer: str
    confidence: float

# STRUCTURED RESPONSE

class SupportResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

# RETRIEVAL NODE

def retrieve(state: SupportState):
    """
    Retrieve the most relevant Zepto policy documents
    using SentenceTransformer embeddings and ChromaDB.
    """

    query = state["query"]

    # Create query embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    sources = []

    for document, metadata in zip(documents, metadatas):

        context_parts.append(document)

        sources.append(
            metadata["chunk_id"]
        )

    context = "\n\n".join(context_parts)

    return {
        "context": context,
        "sources": sources,
    }

# MOCK LLM / DETERMINISTIC ANSWER NODE

def generate_answer(state: SupportState):
    """
    Deterministic offline answer generation.

    No external LLM or API is used.

    The function examines the retrieved context and
    returns an answer only when the required information
    is present in that context.
    """

    query = state["query"].lower().strip()
    context = state["context"].lower()

    retrieved_sources = state.get("sources", [])

    # PRIORITY DELIVERY

    if (
        "priority delivery" in query
        and "priority delivery" in context
        and "inr 15" in context
    ):
        answer = (
            "Priority delivery costs an additional INR 15."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # CANCELLATION AFTER PACKED

    if (
        (
            "cancel" in query
            or "cancellation" in query
        )
        and "packed" in query
        and "packed" in context
        and "can no longer be cancelled" in context
    ):
        answer = (
            "Orders can be cancelled free of cost before the "
            "order status changes to 'Packed'. Once an order "
            "has been packed, it can no longer be cancelled "
            "through the app."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # REFUND TIMING

    if (
        "refund" in query
        and (
            "how long" in query
            or "when" in query
            or "how many days" in query
            or "take" in query
            or "duration" in query
        )
        and "3–5 business days" in context
    ):
        answer = (
            "Approved refunds are credited to the original "
            "payment method within 3–5 business days, or "
            "instantly to the Zepto wallet if the customer "
            "opts for wallet credit."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # REFUND GENERAL

    if (
        "refund" in query
        and "refund" in context
    ):
        answer = (
            "The retrieved Zepto policy information contains "
            "refund details, including refund processing and "
            "wallet-credit options."
        )

        confidence = 0.9

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # DELIVERY TIME

    if (
        (
            "delivery time" in query
            or "how long" in query
            or "when will" in query
        )
        and "10 to 30 minutes" in context
    ):
        answer = (
            "Zepto delivers orders within 10 to 30 minutes "
            "of order confirmation, depending on the delivery "
            "zone and current order volume."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }


    # DELIVERY FEE
  

    if (
        (
            "delivery fee" in query
            or "delivery charge" in query
            or "delivery charges" in query
        )
        and "inr 25" in context
    ):
        answer = (
            "Orders below INR 149 incur a flat INR 25 delivery "
            "fee. Standard delivery is free on orders over "
            "INR 149."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # ORDER TRACKING

    if (
        (
            "track" in query
            or "tracking" in query
            or "rider" in query
        )
        and "track order" in context
    ):
        answer = (
            "Every Zepto order shows a live rider-tracking map "
            "from the moment it is packed until delivery. "
            "Customers can access it from the 'Track Order' screen."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # DAMAGED / MISSING / SPOILED ITEMS
  
    if (
        (
            "damaged" in query
            or "missing" in query
            or "spoiled" in query
            or "wrong item" in query
        )
        and "report an issue" in context
    ):
        answer = (
            "If an order arrives with damaged, spoiled, or missing "
            "items, customers must report it within 24 hours of "
            "delivery through the 'Report an Issue' button."
        )

        confidence = 1.0

        return {
            "answer": answer,
            "sources": retrieved_sources,
            "confidence": confidence,
        }

    # UNKNOWN / NOT IN POLICY
    
    answer = (
        "The provided Zepto policy information does not "
        "contain the answer."
    )

    confidence = 0.3

    return {
        "answer": answer,
        "sources": [],
        "confidence": confidence,
    }

# BUILD LANGGRAPH

def build_graph():

    graph = StateGraph(SupportState)

    # Add nodes
    graph.add_node(
        "retrieve",
        retrieve
    )

    graph.add_node(
        "generate_answer",
        generate_answer
    )

    # START -> retrieve
    graph.add_edge(
        START,
        "retrieve"
    )

    # retrieve -> generate_answer
    graph.add_edge(
        "retrieve",
        "generate_answer"
    )

    # generate_answer -> END
    graph.add_edge(
        "generate_answer",
        END
    )

    return graph.compile()

# COMPILED SUPPORT GRAPH

support_graph = build_graph()