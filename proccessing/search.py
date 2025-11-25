import json
import math
import re
import argparse
from collections import defaultdict
from nltk.stem import WordNetLemmatizer


def load_index():
    dictionary = {}
    postings = {}
    documents = {}
    pagerank = {}

    with open("dictionary.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                term, df = parts
                dictionary[term] = int(df)

    with open("postings.txt", "r", encoding="utf-8") as f:
        for line in f:
            term, json_data = line.split(":", 1)
            postings[term.strip()] = json.loads(json_data.strip())

    with open("../data/collection.json", "r", encoding="utf-8") as f:
        collections = json.load(f)
        for doc in collections:
            doc_id = int(doc["id"])
            url = doc.get("url", "")
            content = doc.get("content", "")
            title = doc.get("title", "")
            links = doc.get("links", [])
            documents[doc_id] = {
                "url": url,
                "content": content,
                "title": title,
                "links": links
            }

    try:
        with open("pagerank.json", "r", encoding="utf-8") as f:
            pagerank = json.load(f)
            max_pr = max(pagerank.values()) if pagerank else 1
            for k in pagerank:
                pagerank[k] = pagerank[k] / max_pr
    except FileNotFoundError:
        pagerank = {doc_id: 0 for doc_id in documents}

    return dictionary, postings, documents, pagerank


def preprocess(text, stopwords=None):
    lemmatizer = WordNetLemmatizer()
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    if stopwords:
        tokens = [t for t in tokens if t not in stopwords]
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens]
    return lemmatized


def compute_tfidf_vectors(postings, N):
    doc_vectors = defaultdict(dict)
    doc_lengths = defaultdict(float)

    for term, docs in postings.items():
        df = len(docs)
        idf = math.log10(N / df) if df != 0 else 0

        for doc_id, data in docs.items():
            tf = data[0]
            w = (1 + math.log10(tf)) * idf if tf > 0 else 0
            doc_vectors[doc_id][term] = w
            doc_lengths[doc_id] += w ** 2

    for doc_id in doc_lengths:
        doc_lengths[doc_id] = math.sqrt(doc_lengths[doc_id])

    return doc_vectors, doc_lengths


def make_snippet(text, query_terms, window=40):
    text_lower = text.lower()
    positions = []

    for term in query_terms:
        idx = text_lower.find(term)
        if idx != -1:
            positions.append(idx)

    if not positions:
        snippet = text[:200]
    else:
        start = max(min(positions) - window, 0)
        end = min(max(positions) + window, len(text))
        snippet = text[start:end]

    for term in query_terms:
        snippet = re.sub(rf"(?i)({re.escape(term)})", r"**\1**", snippet)

    return snippet + "..."


def vector_space_search(query, dictionary, postings, documents, pagerank, w1=0.9, w2=0.1, use_stopwords=False, top_k=10):
    stopwords = set()
    if use_stopwords:
        with open("common_words", "r", encoding="utf-8") as f:
            stopwords = set(w.strip().lower() for w in f.readlines())

    query_terms = preprocess(query, stopwords)
    query_weights = defaultdict(float)
    N = len(documents)

    for term in query_terms:
        if term in dictionary:
            df = dictionary[term]
            idf = math.log10(N / df) if df != 0 else 0
            tf = query_terms.count(term)
            query_weights[term] = (1 + math.log10(tf)) * idf

    query_length = math.sqrt(sum(w ** 2 for w in query_weights.values())) or 1.0
    doc_vectors, doc_lengths = compute_tfidf_vectors(postings, N)

    scores = defaultdict(float)
    for term, q_wt in query_weights.items():
        if term not in postings:
            continue
        for doc_id, data in postings[term].items():
            if doc_id in doc_vectors:
                d_wt = doc_vectors[doc_id].get(term, 0)
                scores[doc_id] += q_wt * d_wt

    for doc_id in scores:
        if doc_lengths[doc_id] > 0:
            scores[doc_id] /= (doc_lengths[doc_id] * query_length)

    final_scores = {}
    for doc_id, cos_score in scores.items():
        pr_score = pagerank.get(str(doc_id), pagerank.get(doc_id, 0))

        url_boost = 0.0
        doc = documents.get(int(doc_id))
        if doc:
            url_lower = doc["url"].lower()
            hits = sum(1 for t in query_terms if t in url_lower)
            if hits > 0:
                url_boost = 0.5 * (hits / len(query_terms))

        final_scores[doc_id] = w1 * cos_score + w2 * pr_score + url_boost

    ranked_docs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    print(f"\nTop {len(ranked_docs)} results for query: \"{query}\"\n")

    for doc_id, score in ranked_docs:
        doc = documents[int(doc_id)]
        title = doc.get("title") or doc["content"][:60].split("\n")[0]
        snippet = make_snippet(doc["content"], query_terms)

        print(f"• Title: {title}")
        print(f"• Link: {doc['url']}")
        print(f"• Snippet: {snippet}\n")

    return ranked_docs



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search documents via Vector Space Model")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("-topk", type=int, default=15)
    parser.add_argument("-w1", type=float, default=0.9)
    parser.add_argument("-w2", type=float, default=0.1)
    args = parser.parse_args()

    dictionary, postings, documents, pagerank = load_index()

    vector_space_search(
        args.query,
        dictionary,
        postings,
        documents,
        pagerank,
        w1=args.w1,
        w2=args.w2,
        use_stopwords=True,
        top_k=args.topk,
    )
