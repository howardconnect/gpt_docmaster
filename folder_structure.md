gpt_docmaster/
├── app.py                 # Flask web UI
├── watcher.py             # Realtime folder watcher
├── handler.py             # File ingestion + DB logic
├── utils/
│   ├── file_ops.py        # Thumbnails, renaming, hashing
│   ├── gpt_client.py      # GPT fallback logic
│   └── extractors.py      # Text extraction tools
├── templates/             # Web UI HTML
├── static/thumbnails/     # Document previews
├── database.db            # SQLite file
├── .env                   # Config values
