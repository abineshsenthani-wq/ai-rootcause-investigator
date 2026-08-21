import re
from typing import Dict, Any

class QuestionRouter:
    """Classifies user natural language questions into analytical intents."""

    INTENTS = {
        "TREND": [r"trend", r"over time", r"growth", r"history", r"timeline"],
        "ANOMALY": [r"anomaly", r"anomalies", r"outlier", r"unusual", r"spike", r"strange"],
        "CORRELATION": [r"correlat", r"relationship", r"associated", r"co-vary"],
        "SEGMENT_ANALYSIS": [r"region", r"product", r"segment", r"category", r"channel", r"where", r"which"],
        "RECOMMENDATION": [r"recommend", r"action", r"do next", r"fix", r"what should"],
        "ROOT_CAUSE": [r"why", r"cause", r"reason", r"driver", r"explain"]
    }

    @classmethod
    def route_question(cls, question: str) -> str:
        q_lower = question.lower()

        for intent, patterns in cls.INTENTS.items():
            for pat in patterns:
                if re.search(pat, q_lower):
                    return intent

        return "SUMMARY"
