
---

## 🧭 `BUILD_PLAN.md`

```markdown
# 🏗 GPT Gazer 2.0 – Build Plan

This file defines the structured roadmap to build GPT Gazer 2.0 from the ground up, in modular phases. Each section can be completed independently and tested incrementally.

---

## ✅ Phase 1: Core Infrastructure

- [ ] `.env` config with `WATCH_FOLDER`, `STORAGE_FOLDER`, `OPENAI_API_KEY`
- [ ] SQLite DB with `documents` and `conflicts` tables
- [ ] Schema fields:
  - filename, summary, hash, thumbnail_path, category, keyword
  - source (gpt | fallback), archived, date_added, date_modified, tokens_used
- [ ] Create `extract_text_from_file()` for PDFs, DOCX, TXT, HTML, EML
- [ ] Generate thumbnails + previews (cache if exists)
- [ ] Hash each file and store metadata

---

## 📡 Phase 2: Watcher & Fallback Mode

- [ ] Watch folder with `watchdog` for new/deleted files
- [ ] On new file:
  - Extract text
  - Rename using content
  - Generate thumbnail
  - Save metadata to DB
  - Use `source='fallback'` if GPT not used
- [ ] On deletion:
  - Remove from DB
  - Remove thumbnails
- [ ] On startup:
  - Repair missing DB entries or thumbnails
  - Delete orphaned thumbnails

---

## 🌐 Phase 3: Web UI MVP

- [ ] Flask app with:
  - `/` → document dashboard
  - `/open/<filename>` → preview or download
  - `/conflicts` → manual resolution
  - `/setup` → select watch/storage folders
- [ ] Toggle views: List | Card | Grid
- [ ] Live auto-refresh (AJAX or Socket.IO)
- [ ] Display: thumbnail, filename, tags, source, status

---

## 🤖 Phase 4: GPT Integration

- [ ] `summarize_with_gpt(text)` returns:
  - title, summary, tags, category
  - cost + token count
- [ ] Retry-friendly logic if GPT fails
- [ ] Fallback title if GPT quota exceeded
- [ ] Store `tokens_used`, `source='gpt'`

---

## 🧠 Phase 5: GPT Chat Assistant

- [ ] GPT-powered sidebar UI
- [ ] User can type:
  - `summarize file X`
  - `rename to "..."`, `move to folder X`
  - `delete file`, `recategorize as "legal"`
- [ ] GPT interprets and performs actions

---

## 🔍 Phase 6: Search + Filtering

- [ ] Add SQLite full-text search (FTS5)
- [ ] UI search bar with:
  - keyword
  - category
  - source (gpt vs fallback)
  - archived status
- [ ] Backend `/api/search` with query filters

---

## 🧱 Phase 7: Archive + Batch Features

- [ ] Mark file as `archived` → move to subfolder
- [ ] Export document set as ZIP or CSV
- [ ] Filter archived-only view

---

## 🛡 Phase 8: Error Handling + Logs

- [ ] Central `logs/` with rotating system + GPT logs
- [ ] UI indicator for processing failures
- [ ] Track retry count or failure reason per document
- [ ] View logs from the dashboard

---

## 🧪 Phase 9: Power Tools

- [ ] “Cache all pages” of a document on demand
- [ ] Per-document history/audit trail
- [ ] Drag-and-drop upload to watch folder
- [ ] Multi-profile folder configs
- [ ] Scheduled reprocessing of fallback docs

---

## 🌟 Future Enhancements

- [ ] GPT summarization queue with ETA
- [ ] Background tasks via Celery or RQ
- [ ] Multi-user support with login
- [ ] GPT tagging models (e.g. classify by type, client, urgency)

---

## ⏱ Recommended Dev Order

1. Phase 1: Core I/O + DB
2. Phase 2: Fallback-mode watcher
3. Phase 3: Flask UI with auto-refresh
4. Phase 4–5: Add GPT + chat window
5. Phase 6+: Search, archive, GPT tools

---

## 🧭 Setup Scripts (coming soon)

- [ ] `init_db.py` – Create DB tables
- [ ] `setup.py` – Wizard for folder + .env config
- [ ] `run.sh` – One-click startup for app + watcher

