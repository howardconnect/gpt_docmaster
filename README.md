# 📂 GPT DocMaster

**GPT DocMaster** is a self-hosted, AI-augmented document assistant that watches a folder in real-time, indexes new files, generates thumbnails, and serves a live-updating web UI.

---

## 🚀 Features

- **Real-time file watching**  
  Watches a configurable `WATCH_FOLDER`, indexes new/deleted files via `watcher.py`.

- **Robust ingestion & thumbnails**  
  - `handler.py` processes PDFs (PyMuPDF), images (Pillow), `.txt` and `.docx` (python-docx).  
  - Slugifies filenames to avoid 404s on special characters.  
  - Stores thumbnails under `static/thumbnails/`.

- **SQLite database backend**  
  - `database.py` defines `Document`, `Thumbnail`, and `Conflict` models via SQLAlchemy.  
  - `init_db()` bootstraps your tables.

- **Flask web UI**  
  - `app.py` serves:
    - `/` → `templates/index.html`  
    - `/api/docs?q=…` → JSON list of documents (with metadata & thumbnail URLs)  
    - `/stream` → Server-Sent Events for live create/delete notifications  
  - **Grid / List** toggle, **live search**, **View/Download** buttons.

- **File-type icons & fallbacks**  
  - Font Awesome icons for `.txt`, `.docx`, and PDF fallback if no thumbnail.  
  - Uniform 200 px slot ensures consistent card size.

---

## 📦 Requirements

- Python 3.10+  
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  Dependencies:
  - Flask  
  - watchdog  
  - SQLAlchemy  
  - python-dotenv  
  - PyMuPDF  
  - Pillow  
  - python-docx

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
WATCH_FOLDER=/path/to/watch
STORAGE_FOLDER=/path/to/archive
PORT=5000
FLASK_ENV=development
# (Optional) OPENAI_API_KEY=your_key_here
```

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone https://github.com/your-org/gpt_docmaster.git
cd gpt_docmaster
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python database.py
```

Start the folder watcher:

```bash
python watcher.py
```

In a second terminal, start the web UI:

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🗂 Project Structure

```
gpt_docmaster/
├── .env
├── .gitignore
├── README.md
├── ON_THE_NEXT_EPISODE.md
├── requirements.txt
├── database.py
├── handler.py
├── watcher.py
├── app.py
├── event_queue.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── thumbnails/
│       └── *.png
└── docs/        ← documentation, if added
```

---

## ⚠️ Known Issues & Limitations

- No GPT integration yet (fallback mode only).
- File serving: View/Download buttons open `/static/docs/…` but there is no `static/docs/` folder by default.
- Size metadata (`size_readable`) is currently a placeholder.
- Mobile responsiveness and error handling (spinners, toast messages) are not implemented.


---

## 🤝 Contributing

Please read `ON_THE_NEXT_EPISODE.md` for planned work and cleanup tasks.  
Feel free to open issues or PRs!
