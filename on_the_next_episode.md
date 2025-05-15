
---

## `ON_THE_NEXT_EPISODE.md`

```markdown
# 🎬 On the Next Episode

A roadmap & housekeeping checklist for anyone jumping into GPT DocMaster next.

---

## 1. Core Features to Build

- **GPT Query Backend**  
  - Implement `extract_text(path)` → send to OpenAI API  
  - Secure `/api/query` endpoint with rate limits

- **Chat Interface**  
  - Sidebar or modal to chat with GPT about a selected document  
  - Display context, streaming responses, message history

- **Search & Filtering**  
  - Faceted search: by extension, date range, keywords  
  - Tagging & sorting options

- **Archive Folder Support**  
  - Move processed files to `STORAGE_FOLDER`  
  - UI toggle to view archived vs. active

- **Token & Cost Tracking**  
  - Record API calls, display usage per document  
  - Warn when near quota

---

## 2. UI/UX Enhancements

- Mobile‐responsive breakpoints (cards stack on small screens)  
- Loading indicators (spinners) for thumbnails & GPT queries  
- Better “No conflicts” / “No matches” messaging  
- Conflict resolution UI for `/conflicts.html`

---

## 3. Code Cleanup & Refactoring

- **Remove/Archive** unused scripts & docs:  
  - `db_inspect.py`  
  - `folder_structure.md`  
  - `build_plan.md`  
  - `starting_wed.md`

- **Modularize handlers**:  
  - Move thumbnail & slugify logic into `utils/`  
  - Separate DB operations into `services/`

- **Error handling & logging**:  
  - Switch from `print` to `logging` with rotating file handlers  
  - Wrap all file/DB operations in `try/except`

- **Tests & CI**:  
  - Unit tests for `handler.py` & `database.py`  
  - Integration tests for API endpoints  
  - GitHub Actions for linting and test runs

---

## 4. Deployment & Packaging

- **Dockerize** the full stack (Flask + Watcher)  
- Provide a single `docker-compose.yml`  
- Environment variable management  
- Publish to GitHub Packages or Docker Hub

---

## 5. Documentation

- Move detailed roadmaps (`folder_structure.md`, `build_plan.md`) into a `docs/` directory  
- Maintain updated API reference (endpoints, payloads)  
- Add architecture diagrams (e.g. sequence flow, data model)

---

> With these tasks completed, GPT DocMaster will evolve from a neat proof-of-concept into a fully featured, production-ready document assistant. Let’s make it happen!  
