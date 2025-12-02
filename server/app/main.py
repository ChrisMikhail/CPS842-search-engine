from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import re
from urllib.parse import urlparse

processing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../proccessing'))
sys.path.insert(0, os.path.dirname(processing_path))

os.chdir(processing_path)

from proccessing.search import search_documents


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
    score: float
    snippet: str
    positions: list[int]| None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
async def process_queries(
    q: str | None = None, 
    topk: int = 15,
    w1: float = 0.9,
    w2: float = 0.1
) -> list[QueryResult]:
    
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    results = search_documents(q, topk=topk, w1=w1, w2=w2)
    
    query_results = []
    for result in results:
        from urllib.parse import urlparse
        parsed_url = urlparse(result['url'])
        site_name = parsed_url.netloc or "Unknown"
        
        # extract title from URL path, gets last segment after /
        url_path = parsed_url.path.rstrip('/')
        if '/' in url_path:
            title = url_path.split('/')[-1]
        else:
            title = url_path or result['title']
        title = title.replace('_', ' ').strip() + ' - Minecraft Wiki'
        
        snippet = result['snippet']
        
        query_results.append(QueryResult(
            title=title,
            site_name=site_name,
            link=result['url'],
            link_icon=f"https://www.google.com/s2/favicons?domain={parsed_url.netloc}",
            score=round(result['score'], 4),
            snippet=snippet,
            positions=None
        ))
    
    return query_results