from pydantic import BaseModel


class GenerateRequest(BaseModel):
    query: str


class GenerateResponse(BaseModel):
    status: str
    content: str | None = None
    message: str | None = None


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    found: bool
    content: str | None = None
    message: str | None = None