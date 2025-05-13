# watcher.py

import os
import time
from dotenv import load_dotenv
import handler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent

# DEBUG
print("🔧 watcher.py is starting up...")

# Load environment variables
load_dotenv()
WATCH_FOLDER = os.getenv("WATCH_FOLDER")
print(f"🔍 Loaded WATCH_FOLDER = {WATCH_FOLDER!r}")

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

    def on_moved(self, event: FileMovedEvent):
        if event.is_directory:
            return
        src, dest = event.src_path, event.dest_path
        if src.startswith(WATCH_FOLDER) and not dest.startswith(WATCH_FOLDER):
            print(f"🔀 File moved out: {src}")
            handler.process_deleted_file(src)
        elif not src.startswith(WATCH_FOLDER) and dest.startswith(WATCH_FOLDER):
            print(f"🔀 File moved in: {dest}")
            handler.process_new_file(dest)

if __name__ == "__main__":
    if not WATCH_FOLDER:
        print("⚠️  ERROR: WATCH_FOLDER not set in .env! Exiting.")
        exit(1)
    if not os.path.isdir(WATCH_FOLDER):
        print(f"❌ ERROR: Watch folder does not exist:\n   {WATCH_FOLDER!r}")
        exit(1)

    # Orphan cleanup
    print("🧹 Running orphan cleanup…")
    from handler import cleanup_orphans
    cleanup_orphans(WATCH_FOLDER)

    # Start observer
    print(f"👀 Now watching folder: {WATCH_FOLDER}")
    observer = Observer()
    observer.schedule(WatchHandler(), WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        # Block forever, printing a heartbeat so you know it's alive
        while True:
            print("…waiting for file events…", end="\r", flush=True)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher")
        observer.stop()

    observer.join()
