import os
import json
import time
from flask import Flask, request, jsonify, send_from_directory
import redis

app = Flask(__name__)

STATIC_DIR = os.getenv("STATIC_DIR", os.path.join(os.path.dirname(__file__), "static"))

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

CHAT_KEY = "chat:messages"
MAX_MESSAGES = 100


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/health")
def health():
    redis_client.ping()
    return jsonify({"status": "ok"})


@app.route("/messages", methods=["GET"])
def get_messages():
    raw = redis_client.lrange(CHAT_KEY, 0, -1)
    messages = [json.loads(m) for m in raw]
    return jsonify(messages)


@app.route("/messages", methods=["POST"])
def post_message():
    data = request.get_json()
    if not data or not data.get("user") or not data.get("text"):
        return jsonify({"error": "Fields 'user' and 'text' are required"}), 400

    message = {
        "user": data["user"],
        "text": data["text"],
        "timestamp": time.time(),
    }

    redis_client.rpush(CHAT_KEY, json.dumps(message))
    redis_client.ltrim(CHAT_KEY, -MAX_MESSAGES, -1)

    return jsonify(message), 201


@app.route("/messages", methods=["DELETE"])
def clear_messages():
    redis_client.delete(CHAT_KEY)
    return jsonify({"status": "chat cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
