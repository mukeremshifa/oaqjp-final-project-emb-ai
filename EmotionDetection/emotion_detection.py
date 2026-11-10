"""Emotion detection using a Watson NLP emotion model."""

import os
from typing import Any, Dict

import requests


WATSON_NLP_URL = os.getenv(
    "WATSON_NLP_URL",
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict",
)
WATSON_MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"


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
        headers={"grpc-metadata-mm-model-id": WATSON_MODEL_ID},
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
