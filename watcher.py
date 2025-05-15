# watcher.py

import os
import time
from dotenv import load_dotenv
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

from handler import process_new_file, process_deleted_file, cleanup_orphans

# Load your WATCH_FOLDER from .env (fallback to this UNC path)
load_dotenv()
WATCH_FOLDER = os.getenv(
    "WATCH_FOLDER",
    r"\\mothership\File Cabinet\watch_folder"
)

class WatchHandler(FileSystemEventHandler):
    """Catch all FS events and dispatch to your handler functions."""

    def on_any_event(self, event):
        # Debug-print every event so you can see what’s happening
        print(f"EVENT: {event.event_type} — {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            print(f"➕ Created: {event.src_path}")
            process_new_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            dest = getattr(event, "dest_path", event.src_path)
            print(f"🔀 Moved: {event.src_path} → {dest}")
            process_new_file(dest)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ Modified: {event.src_path}")
            process_new_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"➖ Deleted: {event.src_path}")
            process_deleted_file(event.src_path)


def main():
    print("🔧 watcher.py starting…")
    print(f"🔍 WATCH_FOLDER = '{WATCH_FOLDER}'\n")

    # 1) Remove stale DB entries
    print("🧹 Running orphan cleanup…")
    cleanup_orphans(WATCH_FOLDER)

    # 2) One-time startup scan
print("📂 Initial scan of existing files…")
for fname in os.listdir(WATCH_FOLDER):
        full = os.path.join(WATCH_FOLDER, fname)
        if os.path.isfile(full):
            print(f"  • Startup index: {fname}")
            process_new_file(full)

    # Regenerate missing thumbnails
print("🔄 Checking for missing thumbnails…")
from database import SessionLocal, Document
session = SessionLocal()
try:
        for doc in session.query(Document).all():
            needs = False
            if not doc.thumbnails:
                needs = True
            else:
                latest = doc.thumbnails[-1]
                if not os.path.exists(latest.thumbnail_path):
                    needs = True
            if needs:
                print(f"  • Regenerating thumb for: {doc.filename}")
                from handler import create_thumbnail
                create_thumbnail(doc.id, doc.path, doc.filename)
finally:
        session.close()

    # 3) Begin watching
print(f"\n👀 Now watching folder for changes…\n")
observer = Observer()
observer.schedule(WatchHandler(), WATCH_FOLDER, recursive=False)
observer.start()

try:
        while True:
            time.sleep(1)
except KeyboardInterrupt:
        print("\n🛑 Stopping watcher…")
        observer.stop()
observer.join()


if __name__ == "__main__":
    main()
