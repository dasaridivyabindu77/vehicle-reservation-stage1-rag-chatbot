import os
from flask import Flask, jsonify, render_template, request, session

from app.chatbot import Chatbot
from app.database import Database
from app.vector_store import StaticVectorStore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def create_app(test_config=None):
    config = test_config or {}
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))
    app.secret_key = config.get("SECRET_KEY", os.environ.get("CHATBOT_SECRET_KEY", "dev-only-change-me"))
    db_path = config.get("DATABASE", os.path.join(DATA_DIR, "chatbot.db"))
    chroma_path = config.get("CHROMA_PATH", os.path.join(DATA_DIR, "chroma"))
    database = Database(db_path)
    database.initialize()
    vector_store = StaticVectorStore(chroma_path, os.path.join(DATA_DIR, "static_knowledge.json"))
    chatbot = Chatbot(vector_store, database)
    app.extensions["chatbot"] = chatbot

    @app.get("/")
    def index():
        if "chat_session_id" not in session:
            session["chat_session_id"] = os.urandom(16).hex()
        return render_template("index.html")

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = payload.get("message", "")
        if not isinstance(message, str) or not message.strip():
            return jsonify({"error": "Message is required."}), 400
        if "chat_session_id" not in session:
            session["chat_session_id"] = os.urandom(16).hex()
        response = chatbot.process(session["chat_session_id"], message.strip())
        return jsonify(response)

    @app.post("/api/reset")
    def reset():
        session_id = session.get("chat_session_id")
        if session_id:
            chatbot.sessions.pop(session_id, None)
        return jsonify({"reply": "Conversation reset.", "session": {}})

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "vector_documents": vector_store.collection.count(), "dynamic_database": "connected"})

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
