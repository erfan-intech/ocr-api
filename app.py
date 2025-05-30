from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import pytesseract
import re

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        data = request.json['image']
        _, encoded = data.split(",", 1)
        img_data = base64.b64decode(encoded)
        np_img = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        text = pytesseract.image_to_string(img)

        # Very basic detection of medicine name and quantity
        match = re.search(r'([A-Za-z0-9]+)[^\n]*[xX*]\s*(\d+)', text)
        if match:
            name = match.group(1)
            qty = int(match.group(2))
        else:
            name, qty = "Unknown", 0

        return jsonify({"name": name, "qty": qty})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "OCR API is running!"
