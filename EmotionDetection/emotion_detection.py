"""Emotion detection using a Watson NLP emotion model."""

import os
from typing import Any, Dict

import requests


WATSON_NLP_URL = os.getenv(
    "WATSON_NLP_URL", "http://localhost:5000/model/predict"
)


def emotion_detector(text_to_analyze: str) -> Dict[str, Any]:
    """Return emotion scores and the dominant emotion for input text."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 400,
        }

    response = requests.post(
        WATSON_NLP_URL,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 400,
        }
    response.raise_for_status()

    payload = response.json()
    predictions = payload.get("emotionPredictions", [])
    emotions = predictions[0].get("emotion", {}) if predictions else {}
    names = ("anger", "disgust", "fear", "joy", "sadness")
    result: Dict[str, Any] = {name: emotions.get(name) for name in names}
    available = {name: value for name, value in result.items() if value is not None}
    result["dominant_emotion"] = (
        max(available, key=available.get) if available else None
    )
    return result
