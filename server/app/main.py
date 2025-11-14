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
    title: str
    link: str
    score: int
    snippet: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
async def process_queries(q:str | None = None) -> list[QueryResult]:
    print(q)
    results = [QueryResult(title="Lionel Messi", link="https://www.transfermarkt.us/lionel-messi/profil/spieler/28003", score = 1, snippet = "testing this snippet right now"),QueryResult(title="Cristiano Ronaldo", link="https://www.transfermarkt.us/cristiano-ronaldo/profil/spieler/8198", score = 1, snippet = "testing this snippet right now"), ]
    return results