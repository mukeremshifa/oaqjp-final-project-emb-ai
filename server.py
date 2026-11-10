"""Flask web server for the emotion detector."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the form and process submitted customer feedback."""
    text = ""
    result = None
    error = None
    if request.method == "POST":
        text = request.form.get("text", "")
        if not text.strip():
            error = "Please enter text to analyze."
        else:
            result = emotion_detector(text)
            if result.get("status_code") == 400:
                error = "The emotion service rejected the submitted text."
                result = None
    return render_template("index.html", text=text, result=result, error=error)


@app.route("/emotionDetector")
def emotion_detector_api():
    """Return formatted emotion results for the course API endpoint."""
    text = request.args.get("textToAnalyze", "")
    if not text.strip():
        return "Invalid input! Please try again."

    result = emotion_detector(text)
    if result.get("status_code") == 400 or result.get("dominant_emotion") is None:
        return "Invalid input! Please try again."

    return (
        "For the given statement, the system response is: "
        f"anger: {result['anger']}, disgust: {result['disgust']}, "
        f"fear: {result['fear']}, joy: {result['joy']}, "
        f"sadness: {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
