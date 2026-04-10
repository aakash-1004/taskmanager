from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Config from environment variables with defaults
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "taskmanager")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
tasks = db["tasks"]

# ── Health Check ──────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ── Get All Tasks ─────────────────────────────────────
@app.route("/tasks", methods=["GET"])
def get_tasks():
    result = []
    for task in tasks.find():
        task["_id"] = str(task["_id"])
        result.append(task)
    return jsonify(result), 200

# ── Create Task ───────────────────────────────────────
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    task = {
        "title": data["title"],
        "done": False
    }
    inserted = tasks.insert_one(task)
    task["_id"] = str(inserted.inserted_id)
    return jsonify(task), 201

# ── Update Task ───────────────────────────────────────
@app.route("/tasks/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    tasks.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "updated"}), 200

# ── Delete Task ───────────────────────────────────────
@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    tasks.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#Task Manager API
