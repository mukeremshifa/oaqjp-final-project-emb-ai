# Final Project

An AI-based customer-feedback emotion detector using a Watson NLP-compatible
emotion prediction service and Flask.

## Run

```powershell
python -m pip install -r requirements.txt
$env:WATSON_NLP_URL = "http://localhost:5000/model/predict"
python server.py
```

Open <http://localhost:5001>. The Watson NLP service URL can be changed with
`WATSON_NLP_URL`.

## Test and static analysis

```powershell
python -m unittest discover -s tests -v
python -m py_compile server.py EmotionDetection\emotion_detection.py
```
