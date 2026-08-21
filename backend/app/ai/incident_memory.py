import json
import os
import numpy as np
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "incident_memory.json")

class HistoricalIncidentMemory:
    """
    RAG-based Historical Incident Memory store for vector indexing and retrieving
    similar past anomalies and root-cause investigations.
    """

    @classmethod
    def _load_memory(cls) -> List[Dict[str, Any]]:
        path = os.path.abspath(MEMORY_FILE)
        if not os.path.exists(path):
            # Seed default baseline historical incidents
            seed = [
                {
                    "id": "inc_2025_01",
                    "dataset_name": "Sales Q2 2025",
                    "metric": "revenue",
                    "percentage_change": -24.1,
                    "summary": "Revenue dropped 24% due to West region logistics delays and delivery carrier stockouts.",
                    "primary_driver": "delivery_days",
                    "facts": ["West region dropped -41.8%", "Delivery days spiked by +31%"],
                    "recommendations": ["Audit West fulfillment carrier SLA"]
                },
                {
                    "id": "inc_2025_02",
                    "dataset_name": "E-Commerce Black Friday",
                    "metric": "conversion_rate",
                    "percentage_change": -18.5,
                    "summary": "Conversion rate dropped 18.5% due to payment gateway checkout latency.",
                    "primary_driver": "checkout_latency_ms",
                    "facts": ["Checkout latency increased from 400ms to 2800ms"],
                    "recommendations": ["Scale payment gateway API concurrency"]
                }
            ]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(seed, f, indent=2)
            return seed

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @classmethod
    def _save_memory(cls, memory: List[Dict[str, Any]]) -> None:
        path = os.path.abspath(MEMORY_FILE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)

    @classmethod
    def save_incident(cls, investigation: Dict[str, Any], dataset_name: str = "Uploaded Dataset") -> Dict[str, Any]:
        memory = cls._load_memory()
        event = investigation.get("event", {})
        facts = investigation.get("facts", [])
        recs = investigation.get("recommendations", [])
        ai_summary = investigation.get("ai_explanation", "")

        inc_id = f"inc_{len(memory) + 1:04d}"
        incident_doc = {
            "id": inc_id,
            "dataset_name": dataset_name,
            "metric": event.get("metric", "revenue"),
            "percentage_change": event.get("percentage_change", 0.0),
            "summary": ai_summary[:200] if ai_summary else f"Metric shift of {event.get('percentage_change', 0):.1f}%",
            "primary_driver": facts[0] if facts else "Unknown",
            "facts": facts,
            "recommendations": recs
        }

        memory.append(incident_doc)
        cls._save_memory(memory)
        return incident_doc

    @classmethod
    def search_similar_incidents(cls, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        memory = cls._load_memory()
        if not memory:
            return []

        # Construct corpus of text strings
        corpus = [
            f"{doc.get('metric')} {doc.get('summary')} {' '.join(doc.get('facts', []))}"
            for doc in memory
        ]

        try:
            vectorizer = TfidfVectorizer().fit(corpus + [query_text])
            doc_vectors = vectorizer.transform(corpus)
            query_vec = vectorizer.transform([query_text])

            scores = cosine_similarity(query_vec, doc_vectors).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]

            matches = []
            for idx in top_indices:
                similarity = float(scores[idx])
                if similarity > 0.05:
                    doc = memory[idx].copy()
                    doc["similarity_score"] = round(similarity, 4)
                    doc["similarity_label"] = (
                        "High Precedent Match" if similarity > 0.4
                        else ("Moderate Match" if similarity > 0.2 else "Low Similarity")
                    )
                    matches.append(doc)
            return matches
        except Exception:
            return memory[:top_k]
