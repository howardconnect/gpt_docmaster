# watcher.py

import os
import time
from dotenv import load_dotenv
import handler

# DEBUG: confirm startup
print("🔧 watcher.py is starting up...")

# Load environment variables
load_dotenv()
WATCH_FOLDER = os.getenv("WATCH_FOLDER")
print(f"🔍 Loaded WATCH_FOLDER = {WATCH_FOLDER!r}")

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"🆕 File created: {event.src_path}")
        handler.process_new_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"❌ File deleted: {event.src_path}")
        handler.process_deleted_file(event.src_path)

if __name__ == "__main__":
    if not WATCH_FOLDER:
        print("⚠️  ERROR: WATCH_FOLDER not set in .env! Exiting.")
        exit(1)

    if not os.path.isdir(WATCH_FOLDER):
        print(f"❌ ERROR: Watch folder does not exist:\n   {WATCH_FOLDER!r}")
        exit(1)

    # Cleanup any DB entries for files that are gone
    print("🧹 Running orphan cleanup…")
    from handler import cleanup_orphans
    cleanup_orphans(WATCH_FOLDER)

    print(f"👀 Now watching folder: {WATCH_FOLDER}")
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    ...

