import os
import json
from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

from config import CHROMA_DB_DIR


class KnowledgeBase:
    def __init__(self, collection_name: str = "qa_kb"):
        # NEW Chroma API
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def _embed(self, texts: List[str]):
        embeddings = self.embedder.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


    def clear(self):
        name = self.collection.name
        self.client.delete_collection(name)
        self.collection = self.client.get_or_create_collection(name)

    def add_documents(self, docs: List[Dict[str, Any]]):
        """
        docs: list of {id, text, metadata}
        """
        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        metadatas = [d["metadata"] for d in docs]
        embeddings = self._embed(texts)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        emb = self._embed([query_text])[0]
        results = self.collection.query(
            query_embeddings=[emb],
            n_results=top_k
        )

        contexts = []
        for i in range(len(results["documents"][0])):
            contexts.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
        return contexts


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def read_file_as_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".md", ".txt"]:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    elif ext == ".html":
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        text_content = soup.get_text(separator="\n")
        return text_content + "\n\n" + "HTML_SOURCE_START\n" + html + "\nHTML_SOURCE_END"
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
