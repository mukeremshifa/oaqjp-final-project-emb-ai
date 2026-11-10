import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_formatted_emotions(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [
                {"emotion": {"anger": 0.1, "disgust": 0.2, "fear": 0.3, "joy": 0.8, "sadness": 0.4}}
            ]
        }
        post.return_value = response
        result = emotion_detector("I love this product")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.8)

    def test_blank_text_returns_bad_request(self):
        result = emotion_detector(" ")
        self.assertEqual(result["status_code"], 400)
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_all_required_emotions_are_present(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {"emotionPredictions": [{"emotion": {}}]}
        post.return_value = response
        result = emotion_detector("sample")
        self.assertEqual(
            set(result) ,
            {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"},
        )


if __name__ == "__main__":
    unittest.main()
