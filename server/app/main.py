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
    site_name: str
    link: str
    link_icon: str
    score: int
    snippet: str
    positions: list[int]| None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
async def process_queries(q:str | None = None) -> list[QueryResult]:
    print(q)
    results = [
        QueryResult(title="Lionel Messi - Player profile 2025 | Transfermarkt", site_name="Transfermarkt", link="https://www.transfermarkt.us/lionel-messi/profil/spieler/28003", link_icon="https://img.a.transfermarkt.technology/portrait/big/28003-1740766555.jpg?lm=1", score = 1, snippet = "Testing Messi snippet here"),
        QueryResult(title="Cristiano Ronaldo - Player profile 2025 | Transfermarkt", site_name="Transfermarkt", link="https://www.transfermarkt.us/cristiano-ronaldo/profil/spieler/8198", link_icon="https://img.a.transfermarkt.technology/portrait/big/28003-1740766555.jpg?lm=1", score = 1, snippet = "Testing Ronaldo snippet here"),
        QueryResult(title="Neymar - Player profile 2025 | Transfermarkt", site_name="Transfermarkt", link="https://www.transfermarkt.us/neymar/profil/spieler/68290", link_icon="https://img.a.transfermarkt.technology/portrait/big/28003-1740766555.jpg?lm=1", score = 1, snippet = "Testing Neymar snippet here"),
        ]
    return results