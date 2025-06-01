from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import pytesseract

app = Flask(__name__)
CORS(app)  # ✅ This line enables cross-origin requests

@app.route("/")
def home():
    return "OCR API is working"

@app.route("/ocr", methods=["POST"])
def ocr():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        base64_image = data["image"].split(",")[1]
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)

        # Basic parsing logic (adjust as needed)
        lines = text.strip().split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        if not lines:
            return jsonify({"name": "", "qty": 0})

        # Very basic: first line = name, last number = qty
        name = lines[0]
        qty = 1
        for word in reversed(lines[-1].split()):
            if word.isdigit():
                qty = int(word)
                break

        return jsonify({"name": name, "qty": qty})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
