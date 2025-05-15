# app.py

import os
import json
from flask import Flask, jsonify, render_template, Response, request
from dotenv import load_dotenv

from database import SessionLocal, Document
from event_queue import event_queue

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/documents", methods=["GET"])
def list_documents():
    """
    Return a JSON list of indexed documents, optionally filtered
    by a query string `?q=term` that matches filenames (case-insensitive).
    """
    q = request.args.get("q", "").strip()
    session = SessionLocal()
    try:
        query = session.query(Document)
        if q:
            # Case-insensitive LIKE
            query = query.filter(Document.filename.ilike(f"%{q}%"))
        docs = query.all()

        payload = []
        for d in docs:
            name, _ = os.path.splitext(d.filename)
            thumb_url = None
            if d.thumbnails:
                candidate = os.path.join(app.static_folder, "thumbnails", f"{name}.png")
                if os.path.exists(candidate):
                    thumb_url = f"/static/thumbnails/{name}.png"

            payload.append({
                "id": d.id,
                "filename": d.filename,
                "title": d.title,
                "source": d.source,
                "added_at": d.added_at.isoformat(),
                "updated_at": d.updated_at.isoformat(),
                "thumbnail": thumb_url,
            })
        return jsonify(payload)
    finally:
        session.close()

@app.route("/stream")
def stream():
    """
    Server-Sent Events endpoint for live updates.
    """
    print("📡 SSE client connected at /stream")

    def event_stream():
        while True:
            msg = event_queue.get()          # blocks until an event is pushed
            yield f"data: {json.dumps(msg)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    # debug + auto-reload enabled
    app.run(host="0.0.0.0", port=5000, debug=True)