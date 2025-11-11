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
            links = doc.get("links", [])
            documents[doc_id] = {
                "url": url,
                "content": content,
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


def compute_tfidf_vectors( postings, N):
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
    doc_vectors, doc_lengths = compute_tfidf_vectors( postings, N)

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
        
        # boost the score if terms from query appear in the url
        url_boost = 0.0
        doc = documents.get(int(doc_id))
        if doc:
            url_lower = doc['url'].lower()
            query_terms_in_url = sum(1 for term in query_terms if term in url_lower)
            if query_terms_in_url > 0:
                url_boost = 0.5 * (query_terms_in_url / len(query_terms)) if len(query_terms) > 0 else 0
        
        final_scores[doc_id] = w1 * cos_score + w2 * pr_score + url_boost

    ranked_docs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    print(f"\nTop {len(ranked_docs)} results for query: \"{query}\" (w1={w1}, w2={w2})")

    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        doc = documents[int(doc_id)]
        print(f"\nRank {rank}")
        print(f"Doc ID: {doc_id}")
        print(f"Score: {score:.4f}")
        print(f"URL: {doc['url']}")
        print(f"Content Preview: {doc['content'][:200]}...")
        if doc["links"]:
            print(f"Links: {', '.join(doc['links'][:3])}")

    return ranked_docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search documents using Vector Space Model + PageRank")
    parser.add_argument("-topk", type=int, default=15, )
    parser.add_argument("-w1", type=float, default=0.9)
    parser.add_argument("-w2", type=float, default=0.1 )
    args = parser.parse_args()

    dictionary, postings, documents, pagerank = load_index()
    print("Enter a query (type ZZEND to quit):")

    while True:
        term = input("> ").strip().lower()
        if term == "zzend":
            break

        vector_space_search(
            term,
            dictionary,
            postings,
            documents,
            pagerank,
            w1=args.w1,
            w2=args.w2,
            use_stopwords=True,
            top_k=args.topk,
        )
