from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryResult(BaseModel):
    link: str
    score: int
    snippet: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search")
async def process_queries(q = None) -> list[QueryResult]:
    results = [QueryResult(link=".....", score = 1, snippet = "testing this snippet right now")]
    return results