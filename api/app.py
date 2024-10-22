import os
import json
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Fetch the Telegram Bot Token from the environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def imageAsDict(imageURL, caption):
    return {
        "type": "photo",
        "media": imageURL,
        "caption": caption,
    }

def sendMediaGroup(chatid, allImages):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"
    media = [imageAsDict(allImages[i]["src"], allImages[i]["prompt"]) for i in range(5)]
    payload = {"chat_id": chatid, "media": media}
    r = requests.post(url, json=payload)
    return r

def sendMessage(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r

@app.post("/")
def index():
    msg = request.get_json()
    chat_id = msg["message"]["chat"]["id"]
    inputText = msg["message"]["text"]
    
    if inputText == "/start":
        sendMessage(chat_id, "Ya, I am Online. Send me a Prompt")
    else:
        BASE_URL = f"https://lexica.art/api/v1/search?q={inputText}"
        response = requests.get(BASE_URL)
        response_text = response.json()
        allImages = response_text.get("images", [])
        if allImages:
            sendMediaGroup(chat_id, allImages)
        else:
            sendMessage(chat_id, "No images found.")
    
    return Response("ok", status=200)
