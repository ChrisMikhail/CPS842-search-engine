import re
import json
import os
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import networkx as nx


def build_inverted_index(json_path, use_stopwords=False):
    stopword_path = os.path.join(os.path.dirname(__file__), "common_words")
    with open(stopword_path, "r", encoding="utf-8") as stopword_file:
        stopwords = set(w.strip().lower() for w in stopword_file.readlines()) if use_stopwords else None

    lemmatizer = WordNetLemmatizer()
    inverted_index = defaultdict(lambda: defaultdict(lambda: [0, []]))

    with open(json_path, "r", encoding="utf-8") as f:
        documents = json.load(f)


    for doc in documents:
        doc_id = doc.get("id")
        content = doc.get("content", "")
        process_document(doc_id, content, inverted_index, stopwords, lemmatizer)


    link_mapping = build_link_mapping(documents)

    pagerank_scores = compute_pagerank(link_mapping)

    return inverted_index, link_mapping, pagerank_scores


def process_document(doc_id, content, inverted_index, stopwords, lemmatizer):
    content = content.replace("-", " ")
    tokens = re.findall(r"[a-zA-Z]+", content.lower())

    position = 0
    for token in tokens:
        position += 1
        if stopwords and token in stopwords:
            continue

        lemma = lemmatizer.lemmatize(token)
        entry = inverted_index[lemma][doc_id]
        entry[0] += 1
        entry[1].append(position)


def build_link_mapping(documents):
   
    url_to_id = {doc["url"]: doc["id"] for doc in documents}
    link_mapping = {}

    for doc in documents:
        doc_id = doc["id"]
        links = doc.get("links", [])
        linked_ids = [url_to_id[link] for link in links if link in url_to_id]
        link_mapping[doc_id] = linked_ids

    return link_mapping


def compute_pagerank(link_mapping, alpha=0.85, max_iter=100, tol=1e-6):
   
    G = nx.DiGraph()

  
    for src, dst_list in link_mapping.items():
        for dst in dst_list:
            G.add_edge(src, dst)

   
    for node in link_mapping.keys():
        if node not in G:
            G.add_node(node)


    return nx.pagerank(G, alpha=alpha, max_iter=max_iter, tol=tol)


def save_index(inverted_index):
    sorted_terms = sorted(inverted_index.keys())
    with open("dictionary.txt", "w", encoding="utf-8") as df, open(
        "postings.txt", "w", encoding="utf-8"
    ) as pf:
        for term in sorted_terms:
            postings = inverted_index[term]
            sorted_postings = dict(sorted(postings.items(), key=lambda x: x[1][0], reverse=True))
            df.write(f"{term}\t{len(postings)}\n")
            pf.write(f"{term}: {json.dumps(sorted_postings)}\n")


def save_link_mapping(link_mapping):
    with open("doc_links.json", "w", encoding="utf-8") as f:
        json.dump(link_mapping, f, indent=2)


def save_pagerank(pagerank_scores):
    with open("pagerank.json", "w", encoding="utf-8") as f:
        json.dump(pagerank_scores, f, indent=2)


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "..", "data", "collection.json")

    inverted_index, link_mapping, pagerank_scores = build_inverted_index(json_path, use_stopwords=True)
    save_index(inverted_index)
    save_link_mapping(link_mapping)
    save_pagerank(pagerank_scores)
