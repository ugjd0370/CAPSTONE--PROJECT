# Zepto Support Assistant

## Module 3 - Offline RAG-Based Customer Support Assistant

This project is an offline RAG-based customer support assistant for Zepto.

It uses:
- Sentence Transformers for embeddings
- ChromaDB for vector search
- LangGraph for the workflow
- FastAPI for the API
- Pydantic for structured responses
- Deterministic mock logic for offline answer generation

## Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── graph.py
├── ingest.py
├── main.py
├── prompt.py
├── requirements.txt
├── Dockerfile
└── README.md

## Architecture

```text
User Question
      │
      ▼
FastAPI /support
      │
      ▼
LangGraph
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB
      │
      ▼
Top-3 Relevant Documents
      │
      ▼
Context Construction
      │
      ▼
Deterministic Mock Generator
      │
      ▼
Structured JSON Response
```
Technologies Used
Python
FastAPI
Uvicorn
LangGraph
ChromaDB
Sentence Transformers
Pydantic
Docker

Embedding model:
all-MiniLM-L6-v2

1. ENVIRONMENT SETUP

From the project root:
cd C:\Users\TOUCH\Desktop\CAPSTONE--PROJECT
Activate the virtual environment:
.\.venv\Scripts\Activate.ps1
Install dependencies:
pip install -r .\support_assistant\requirements.txt

2. PREPARE DOCUMENTS

The policy documents are stored inside:
support_assistant/docs/
The project contains eight policy documents:

1.doc_01.txt
2.doc_02.txt
3.doc_03.txt
4.doc_04.txt
5.doc_05.txt
6.doc_06.txt
7.doc_07.txt
8.doc_08.txt

3.BUILD THE VECTOR BASE

Run the ingestion script from the project root:
python .\support_assistant\ingest.py

Expected output:
Loading embedding model...
Loading documents...
Found 8 documents.
Generating embeddings...
Ingestion complete.
Stored 8 chunks.
Collection: zepto_policies
ChromaDB path: ...\support_assistant\chroma_db
This process:
Reads the policy documents.
Creates one chunk per document.
Generates normalized embeddings.
Stores the embeddings and metadata in ChromaDB.

4. TEST THE LANGGRAPH PIPELINE

Run:
python -c "from support_assistant.graph import support_graph; print(support_graph.invoke({'query':'How much is priority delivery?'}))"

Expected result:

{
    'query': 'How much is priority delivery?',
    'context': '...',
    'sources': [
        'doc_01_chunk_0',
        'doc_05_chunk_0',
        'doc_04_chunk_0'
    ],
    'answer': 'Priority delivery costs an additional INR 15.',
    'confidence': 1.0
}
5. TEST CANCELLATION POLICY 

Run:
python -c "from support_assistant.graph import support_graph; print(support_graph.invoke({'query':'Can I cancel my order after it is packed?'}))"

Expected answer:
Orders can be cancelled free of cost before the order status changes to 'Packed'. Once an order has been packed, it can no longer be cancelled through the app.

Expected confidence:
1.0

6. TEST REFUND POLICY

Run:

python -c "from support_assistant.graph import support_graph; print(support_graph.invoke({'query':'How long does a refund take?'}))"
Expected answer:
Approved refunds are credited to the original payment method within
3–5 business days, or instantly to the Zepto wallet if the customer
opts for wallet credit.
Expected confidence:
1.0

7. TEST UNSUPPORTED QUESTIONS

The assistant must not invent information that is not contained in the policy documents.
For example:
python -c "from support_assistant.graph import support_graph; print(support_graph.invoke({'query':'What is Zepto CEO salary?'}))"
Expected response:

{
    'answer': 'The provided Zepto policy information does not contain the answer.',
    'sources': [],
    'confidence': 0.3
}

This demonstrates the grounding / refusal behavior.

8. RUN FASTAPI R

From the project root:
uvicorn support_assistant.main:app --reload
Expected output:
Uvicorn running on http://127.0.0.1:8000
Application startup complete.

9. OPEN SWAGGER API DOCUMENTATION 

Open the following URL in a browser:
http://127.0.0.1:8000/docs
The API provides:
GET /
POST /support

10. HEALTH CHECK 

Request:
GET /
Expected response:
{
  "message": "Zepto Support Assistant is running"
}

11. SUPPORT API 

Endpoint:
POST /support
Request:
{
  "query": "How much is priority delivery?"
}
Expected response:
{
  "answer": "Priority delivery costs an additional INR 15.",
  "sources": [
    "doc_01_chunk_0",
    "doc_05_chunk_0",
    "doc_04_chunk_0"
  ],
  "confidence": 1.0
}

12.EXAMPLE API TESTS 
Priority Delivery
Request:
{
  "query": "How much is priority delivery?"
}
Response:
{
  "answer": "Priority delivery costs an additional INR 15.",
  "sources": [
    "doc_01_chunk_0",
    "doc_05_chunk_0",
    "doc_04_chunk_0"
  ],
  "confidence": 1.0
}
Cancellation
Request:

{
  "query": "Can I cancel my order after it is packed?"
}
Response:
{
  "answer": "Orders can be cancelled free of cost before the order status changes to 'Packed'. Once an order has been packed, it can no longer be cancelled through the app.",
  "sources": [
    "doc_05_chunk_0",
    "doc_02_chunk_0",
    "doc_06_chunk_0"
  ],
  "confidence": 1.0
}
Refund
Request:
{
  "query": "How long does a refund take?"
}
Response:
{
  "answer": "Approved refunds are credited to the original payment method within 3–5 business days, or instantly to the Zepto wallet if the customer opts for wallet credit.",
  "sources": [
    "doc_02_chunk_0",
    "doc_06_chunk_0",
    "doc_05_chunk_0"
  ],
  "confidence": 1.0
}
Unsupported Question
Request:
{
  "query": "What is Zepto CEO salary?"
}

Response:
{
  "answer": "The provided Zepto policy information does not contain the answer.",
  "sources": [],
  "confidence": 0.3
}

13.STRUCTURED OUTPUT 

Every successful /support response follows this schema:
{
  "answer": "string",
  "sources": ["string"],
  "confidence": 0.0
}

Where:
answer contains the grounded response.
sources contains retrieved document/chunk IDs.
confidence is a number between 0 and 1.

14.OFFLINE/ MOCK LLM DESIGN

The answer generation step intentionally uses deterministic mock logic instead of an external LLM API.
This makes the project:
Fully offline during evaluation
Deterministic
Reproducible
Free from API authentication requirements
Suitable for automated grading
The retrieval stage still uses real embeddings and ChromaDB vector search.

15. LANGGRAPH FLOW 

The LangGraph workflow contains two main nodes:
START
  │
  ▼
retrieve
  │
  ▼
generate_answer
  │
  ▼
END
Retrieve Node

The retrieve node:

Takes the user query.
Generates its embedding.
Queries ChromaDB.
Retrieves the top 3 relevant chunks.
Builds the context.
Records source chunk IDs.
Generate Answer Node

The generate node:
Reads the query.
Reads the retrieved context.
Applies deterministic mock response logic.
Produces the answer.
Produces confidence.
Returns source IDs when the answer is grounded.

16. GROUNDING BEHAVIOUR

The assistant follows a strict grounding rule:
Do not answer using information that is not present in the retrieved policy context.
If the requested information cannot be answered from the policy corpus, the assistant returns:
The provided Zepto policy information does not contain the answer.
and clears the source list.

17. DOCKER

A Dockerfile is included for containerized execution.
Build the image:
docker build -t zepto-support-assistant .\support_assistant
Run the container:
docker run -p 8000:8000 zepto-support-assistant
The API can then be accessed at:
http://127.0.0.1:8000
Swagger documentation:
http://127.0.0.1:8000/docs

18.DEPENDICIES

The project dependencies are listed in:
requirements.txt
Main dependencies:
fastapi
uvicorn
langgraph
pydantic
chromadb
sentence-transformers
python-dotenv

19.VALIDATION SUMMARY

The following scenarios have been tested successfully:
Test Case	Expected Behavior	Status
Priority delivery	Returns INR 15	PASS
Cancel after packed	Returns cancellation policy	PASS
Refund timing	Returns 3–5 business days / wallet option	PASS
Unsupported CEO salary question	Refuses to invent answer	PASS
FastAPI /support	HTTP 200	PASS
Structured JSON	answer, sources, confidence	PASS
ChromaDB retrieval	Top-3 chunks retrieved	PASS
LangGraph	Retrieval → generation flow	PASS
Offline generation	No external LLM API required	PASS

20.RUNNING THE COMPLETE PROJECT 

From the project root:
Step 1 — Activate environment
.\.venv\Scripts\Activate.ps1
Step 2 — Install dependencies
pip install -r .\support_assistant\requirements.txt
Step 3 — Ingest documents
python .\support_assistant\ingest.py
Step 4 — Test LangGraph
python -c "from support_assistant.graph import support_graph; print(support_graph.invoke({'query':'How much is priority delivery?'}))"
Step 5 — Start API
uvicorn support_assistant.main:app --reload
Step 6 — Open Swagger
http://127.0.0.1:8000/docs
Conclusion

This project demonstrates a complete offline RAG customer-support pipeline:

Policy Documents
      ↓
Embeddings
      ↓
ChromaDB Vector Store
      ↓
Semantic Retrieval
      ↓
LangGraph
      ↓
Deterministic Answer Generation
      ↓
Pydantic Structured Output
      ↓
FastAPI

The system provides grounded customer-support answers while refusing to fabricate information that is not present in the Zepto policy corpus.





