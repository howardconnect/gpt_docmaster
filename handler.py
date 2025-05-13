# handler.py

import os
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image

from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, Document
from event_queue import event_queue  # ← for live updates

# Directory for storing thumbnails
THUMB_DIR = os.path.join("static", "thumbnails")
os.makedirs(THUMB_DIR, exist_ok=True)

def process_new_file(filepath: str):
    """
    Index a new file into the documents table, then generate a thumbnail
    and broadcast a 'created' event.
    """
    session = SessionLocal()
    filename = os.path.basename(filepath)
    try:
        # Skip if already indexed
        existing = session.query(Document).filter_by(filename=filename).first()
        if existing:
            print(f"⚠️  Already indexed: {filename}")
            return

        # Create DB record
        doc = Document(
            filename=filename,
            path=filepath,
            source="fallback",
        )
        session.add(doc)
        session.commit()
        print(f"✅ Indexed document: {filename}")

        # Generate thumbnail
        create_thumbnail(doc.id, filepath, filename)

        # Broadcast creation event
        name, _ = os.path.splitext(filename)
        event_queue.put({
            "action": "created",
            "id": doc.id,
            "filename": filename,
            "thumbnail": f"/static/thumbnails/{name}.png"
        })

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ DB error indexing {filename}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error indexing {filename}: {e}")
    finally:
        session.close()

def process_deleted_file(filepath: str):
    """
    Remove a deleted file from the documents table and its thumbnails,
    then broadcast a 'deleted' event.
    """
    session = SessionLocal()
    filename = os.path.basename(filepath)
    try:
        doc = session.query(Document).filter_by(filename=filename).first()
        if not doc:
            print(f"⚠️  Not in DB (nothing to delete): {filename}")
            return

        # 1) Remove thumbnail files & DB records
        #    Copy list() so we can delete while iterating
        for thumb in list(doc.thumbnails):
            # delete the PNG on disk
            try:
                os.remove(thumb.thumbnail_path)
                print(f"🗑️  File removed: {thumb.thumbnail_path}")
            except OSError:
                pass
            # delete the thumbnail record
            session.delete(thumb)

        # 2) Now delete the document record
        session.delete(doc)
        session.commit()
        print(f"🗑️  Removed document and its thumbnails: {filename}")

        # 3) Broadcast deletion event
        event_queue.put({
            "action": "deleted",
            "filename": filename
        })

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to remove {filename}: {e}")
    finally:
        session.close()


def create_thumbnail(doc_id: int, filepath: str, filename: str):
    """
    Renders the first page of a PDF (or a placeholder) to PNG,
    and stores a record in the thumbnails table.
    """
    session = SessionLocal()
    try:
        name, ext = os.path.splitext(filename.lower())
        thumb_path = os.path.join(THUMB_DIR, f"{name}.png")

        if ext == ".pdf":
            doc = fitz.open(filepath)
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150)
            pix.save(thumb_path)
            doc.close()
        else:
            # Placeholder image
            img = Image.new("RGB", (200, 200), color=(240, 240, 240))
            img.save(thumb_path)

        # Record thumbnail in DB
        from database import Thumbnail
        thumb = Thumbnail(
            document_id=doc_id,
            thumbnail_path=thumb_path,
            created_at=datetime.utcnow(),
        )
        session.add(thumb)
        session.commit()
        print(f"🖼️  Created thumbnail for: {filename}")

    except Exception as e:
        session.rollback()
        print(f"❌ Thumbnail error for {filename}: {e}")
    finally:
        session.close()

def cleanup_orphans(watch_folder: str):
    """
    Remove DB entries (and thumbnails) for any documents
    whose files no longer exist on disk.
    """
    session = SessionLocal()
    try:
        docs = session.query(Document).all()
        for doc in docs:
            # If the file is not under watch_folder or doesn't exist:
            if not os.path.exists(doc.path):
                print(f"🧹 Cleaning up orphan: {doc.filename}")
                process_deleted_file(doc.path)
    finally:
        session.close()
