from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"

COLLECTION_NAME = "zepto_policies"


def load_documents():
    documents = []

    for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        documents.append(
            {
                "id": file_path.stem,
                "text": text,
            }
        )

    return documents


def main():
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading documents...")

    documents = load_documents()

    print(f"Found {len(documents)} documents.")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = []
    texts = []
    metadatas = []

    for document in documents:
        chunk_id = f"{document['id']}_chunk_0"

        ids.append(chunk_id)
        texts.append(document["text"])

        metadatas.append(
            {
                "document_id": document["id"],
                "chunk_id": chunk_id,
            }
        )

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("Ingestion complete.")
    print(f"Stored {len(ids)} chunks.")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"ChromaDB path: {CHROMA_DIR}")


if __name__ == "__main__":
    main()