# 📂 GPT DocMaster – AI-Powered Document Assistant

**GPT DocMaster** is a self-hosted, AI-augmented document assistant. It watches any folder you choose (local or networked), automatically extracts and renames files based on their content, and presents a rich web interface for browsing, organizing, and interacting with your documents.

With optional GPT integration and a powerful fallback mode, GPT DocMaster keeps working — even when offline or over quota.

---

## 🚀 Features

### 📡 Real-Time File Monitoring
- Choose a **watch folder** (input) and **storage folder** (organized output)
- Compatible with local or networked drives (NAS, SMB, etc.)
- Auto-renames files based on extracted content or GPT-generated title
- Detects and resolves duplicate content intelligently

### 🖼️ Live Web Dashboard
- Choose between **card**, **list**, or **grid** views
- Auto-refreshing display of new documents as they arrive
- Drag-and-drop uploads directly into the watch folder
- Filter by category, keyword, GPT usage, and archive status

### 🤖 GPT Assistant Chat *(Optional)*
- Natural-language control:  
  “Rename this,” “Summarize file X,” “Move to folder Y”
- Commands supported:
  - `rename`, `summarize`, `move`, `delete`, `categorize`, `archive`
- “Cache all pages” for deeper GPT reading
- Fallback mode renames and indexes even when GPT is disabled

### 🔍 Document Search + Filters
- Full-text search (FTS5) across title, content, summary
- Filter by:
  - Category
  - Keyword
  - Source: `gpt` or `fallback`
  - Archive status

### 🧠 Smart Metadata Indexing
- SQLite-powered metadata DB with:
  - File name, hash, summary, category, keyword, source, token usage
- Built-in conflict detection for hash duplicates
- Thumbnails and preview images for fast scanning

---

## 🛠️ Setup Instructions

### 1. Clone and install

```bash
git clone https://github.com/yourname/gpt_docmaster.git
cd gpt_docmaster
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
