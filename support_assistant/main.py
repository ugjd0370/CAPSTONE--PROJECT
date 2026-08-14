from fastapi import FastAPI
from pydantic import BaseModel, Field

from .graph import support_graph


app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline RAG-based Zepto customer support assistant",
    version="1.0.0",
)


class SupportRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Customer support question",
    )


class SupportResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


@app.get("/")
def root():
    return {
        "message": "Zepto Support Assistant is running"
    }


@app.post(
    "/support",
    response_model=SupportResponse,
)
def support(request: SupportRequest):

    result = support_graph.invoke(
        {
            "query": request.query
        }
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "confidence": result["confidence"],
    }