import os
import json

from flask import Flask, jsonify, render_template, Response, request, url_for
from dotenv import load_dotenv
from sqlalchemy import or_

from database import SessionLocal, Document
from event_queue import event_queue

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/docs", methods=["GET"])
def api_list_docs():
    q = request.args.get("q", "").strip()
    session = SessionLocal()
    try:
        query = session.query(Document)
        if q:
            pattern = f"%{q}%"
            query = query.filter(
                or_(
                    Document.filename.ilike(pattern),
                    Document.title.ilike(pattern)
                )
            )
        docs = query.order_by(Document.added_at.desc()).all()

        result = []
        for d in docs:
            thumb_url = None
            if d.thumbnails:
                thumb = d.thumbnails[-1]
                fname = os.path.basename(thumb.thumbnail_path)
                thumb_url = url_for("static", filename=f"thumbnails/{fname}")

            result.append({
                "id":            d.id,
                "filename":      d.filename,
                "title":         d.title or d.filename,
                "source":        d.source,
                "added_at":      d.added_at.isoformat(),
                "updated_at":    d.updated_at.isoformat(),
                "thumbnail_url": thumb_url,
            })

        return jsonify(result)
    finally:
        session.close()


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            msg = event_queue.get()
            yield f"data: {json.dumps(msg)}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV", "").lower() == "development"
    port       = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
