1. Project Structure

.gitignore
README.md
build_plan.md
folder_structure.md
requirements.txt

database.py          # SQLAlchemy models & init logic
db_inspect.py        # CLI for dumping current DB contents
event_queue.py       # Global Queue for SSE events
handler.py           # File-processing & DB sync (PyMuPDF, PIL)
watcher.py           # Watchdog integration
app.py               # Flask web app & SSE endpoint
static/
  └── thumbnails/   # Generated preview images
templates/
  └── index.html     # Main dashboard template

Missing: tests/ directory for unit/integration tests; no conflicts.html template.

2. database.py (ORM & Schema)

Positive: Declarative models (Document, Thumbnail, Conflict) with relationships; init_db() helper.

To-do:

Fill in stubbed sections (...): define engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///database.db')), call load_dotenv(), import relationship from sqlalchemy.orm.

Add indexes on high-lookup columns (e.g. Document.hash, Conflict.status).

Integrate Alembic or Flask-Migrate for schema migrations.

3. event_queue.py (Live Updates)

Simple Queue for pushing events from handler.py and streaming in app.py.

Consider swapping to a more robust pub/sub if you need multiple consumers or persistence.

4. handler.py (File Processing & DB Sync)

Positive: Uses PyMuPDF for PDF thumbnails, PIL fallback for images; pushes CRUD events to event_queue.

To-do:

Replace ... placeholders in process_new_file, generate_thumbnail, and other methods with actual logic or delegate to small helper functions.

Add robust try/except around all file I/O, metadata extraction, and DB commits; log stack traces on failure.

Refactor cleanup_orphans() into a scheduled job or run on startup before watcher loop.

5. watcher.py (Watchdog Integration)

Positive: Monitors WATCH_FOLDER, prints heartbeat.

To-do:

Implement all WatchHandler event methods (on_created, on_modified, on_deleted, on_moved) instead of stubs (...).

Load both WATCH_FOLDER and ARCHIVE_FOLDER from .env; support fallback mode using a SOURCE_MODE flag.

Replace print with logging, and wrap main loop in if __name__ == '__main__':.

6. app.py (Flask UI & API)

Positive: Serves index.html, static files, and SSE /stream endpoint.

To-do:

Flesh out missing routes for listing documents (/docs), opening files (/open/<id>), resolving conflicts, and archive views.

Create conflicts.html template and associated API endpoints.

Refactor into Blueprints (e.g., main, api, conflicts) for clarity and scalability.

Add custom error handlers (404, 500) and input sanitization.

7. Templates & Static Assets

index.html: Basic SSE-driven update; implement toggles for card, list, grid views, plus search/filter UI.

Missing: conflicts.html, modal dialogs, and empty-state messaging (e.g., “No conflicts”).

style.css: Sparse; recommend adopting Tailwind CSS or a BEM naming convention for maintainability.

Immediate Next Steps

Testing

Add a tests/ folder with pytest.

Write tests for:

DB models (database.py)

Handler logic (mock file events, use temp dirs)

Watcher (watcher.py) simulation

Flask routes via test client.

Core Logic Implementation

Replace all ... in handler.py, watcher.py, and app.py with concrete implementations or helper calls.

Centralize config variables in a config.py loaded via dotenv.

UI/UX Enhancements

Build responsive card, list, and grid views in index.html.

Add live-processing spinners and a clear “No conflicts” message.

Implement the conflict resolution flow in conflicts.html.

Logging & Error Handling

Switch from print to Python’s logging with rotating handlers.

Add try/except around all critical operations and log exceptions with stack traces.

