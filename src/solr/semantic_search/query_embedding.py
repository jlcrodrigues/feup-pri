import requests
from sentence_transformers import SentenceTransformer
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Search for similar documents")
    parser.add_argument("--solr-endpoint", default="http://localhost:8983/solr")
    parser.add_argument("--collection", default="course_unit")
    parser.add_argument("--query-text", required=True)
    parser.add_argument("--num-results", default=10, type=int)
    return parser.parse_args()


def text_to_embedding(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str


def solr_knn_query(endpoint, collection, embedding, num_results=10):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
        "fl": "name",
        "rows": num_results,
        "wt": "json"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()


def display_results(results):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return

    print(f"Found {len(docs)} results:")
    for doc in docs:
        print(f"* {doc.get('id')} {doc.get('name')} [score: {doc.get('score'):.2f}]")
        

def search(solr_endpoint, collection, query_text, num_results=10):
    embedding = text_to_embedding(query_text)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding, num_results)
        return results
    except requests.HTTPError as e:
        raise requests.HTTPError(f"Error {e.response.status_code}: {e.response.text}")


if __name__ == "__main__":
    args = parse_args()
    results = search(
        args.solr_endpoint, args.collection, args.query_text, args.num_results
    )
    display_results(results)
