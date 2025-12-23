from pydantic import BaseModel


class GenerateRequest(BaseModel):
    query: str


class GenerateResponse(BaseModel):
    success: bool
    message: str
    file_path: str | None = None


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    found: bool
    content: str | None = None
    message: str | None = None