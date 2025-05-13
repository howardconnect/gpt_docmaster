# 📂 GPT DocMaster – AI-Powered Document Assistant

**GPT DocMaster** is a self-hosted, AI-augmented document assistant. It watches any folder you choose (local or networked), automatically extracts and renames files based on their content, and presents a rich web interface for browsing, organizing, and interacting with your documents.

With optional GPT integration and a powerful fallback mode, GPT DocMaster keeps working—even when offline or over quota.

---

## 🚀 Features

### 📡 Real-Time File Monitoring

* Choose a **watch folder** (input) and **archive folder** (organized output)
* Compatible with local or networked drives (NAS, SMB, etc.)
* Auto-renames based on extracted metadata or GPT-generated titles
* Detects and resolves duplicate content and hash conflicts

### 🖼️ Live Web Dashboard

* Card, list, or grid views
* Auto-refreshing display as files are added or removed
* Drag-and-drop uploads directly into the watch folder
* Single search box with server-side filtering (`?q=`)

### 🔍 Document Search & Filters

* Filter by filename, keyword, category, source (`gpt` or `fallback`), and archive status
* Real-time search queries hit `/api/documents?q=` for large datasets

### 🤖 GPT Assistant Chat *(Optional)*

* Natural-language commands: rename, summarize, move, delete, categorize, archive
* `/api/query` endpoint to ask questions of document text via OpenAI
* “Cache all pages” support for deep document reading
* Fallback mode for indexing when GPT is disabled or quota is exceeded

### 🧠 Smart Metadata Indexing

* SQLite-backed DB (`documents`, `thumbnails`, `conflicts` tables)
* Tracks filename, path, summary, keywords, source, token usage, timestamps
* Thumbnail generation for quick previews
* Orphan cleanup to sync DB with folder state

---

## 🛠️ Setup & Running

1. **Clone & install**

   ```bash
   git clone https://github.com/yourname/gpt_docmaster.git
   cd gpt_docmaster
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Create `.env`**

   ```ini
   WATCH_FOLDER=\\mothership\\File Cabinet\\watch_folder
   ARCHIVE_FOLDER=\\mothership\\File Cabinet\\scanned_organized
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Initialize DB**

   ```bash
   python handler.py  # creates tables
   ```

4. **Start services**

   * Terminal 1: `python watcher.py`  (folder watcher)
   * Terminal 2: `python app.py`      (Flask web server)

5. **Open** [http://localhost:5000](http://localhost:5000) in your browser

---

## ✅ Completed

* Folder watcher with create/delete handling and orphan cleanup
* SQLite DB and inspection script (`db_inspect.py`)
* Flask API:

  * `/api/documents` (searchable list)
  * `/stream` (SSE live updates)
* Web UI:

  * Grid/list toggle, single search box
  * Live creation/deletion via Server-Sent Events

## 🚧 In Progress

* GPT Query integration (`/api/query`, `extract_text` utilities)
* Front-end chat panel to ask document questions
* Responsive CSS and mobile layout improvements

## 🐛 Known Issues

* Duplicate search inputs on the page; need to remove extra markup
* Thumbnail 404s on special-character filenames—consider URL-encoding or slugify
* Some CSS tags unclosed causing script to be inside header

## 📝 Next Steps

1. **UI Cleanup**: remove duplicate search bar; ensure proper HTML structure
2. **GPT Query Backend**: finalize `extract_text(path)`, secure `/api/query`
3. **Chat Interface**: build chat pane, wire card clicks to queries
4. **Styling & UX**: mobile breakpoints, loading indicators, error messages
5. **Deployment**: Dockerize & deploy to Synology NAS or DigitalOcean

---

*Last updated: May 13, 2025*
