# handler.py Reference

## Overview
`handler.py` provides the core logic for integrating your filesystem watcher
with the SQLite database and thumbnail storage. It supports:

- **Indexing** new documents  
- **Generating** high‐quality thumbnails for PDFs, images, text, and Word docs  
- **Cleaning up** deleted files and orphaned DB records  
- **Broadcasting** create/delete events via SSE for your front‐end

---

## Public API

### `_slugify(name: str) → str`
Convert an arbitrary filename into a URL‐safe lowercase slug.

### `process_new_file(filepath: str) → None`
Handles a newly added file:
1. Inserts a `Document` row (unless already indexed).  
2. Calls `create_thumbnail(...)` and records the thumbnail.  
3. Emits an SSE `"created"` event with the new thumbnail URL.

### `process_deleted_file(filepath: str) → None`
Handles file removal:
1. Deletes all thumbnail files & records for that document.  
2. Deletes the `Document` row.  
3. Emits an SSE `"deleted"` event.

### `cleanup_orphans(watch_folder: str) → None`
Scans all `Document` rows and removes any whose underlying file
no longer exists on disk.

### `create_thumbnail(doc_id: int, filepath: str, filename: str) → str`
Generates a PNG thumbnail, writes a `Thumbnail` DB row, and returns
the slug basename (for constructing URLs).

Supported extensions:
- `.pdf`   → first page @ 300dpi  
- `.png`, `.jpg`, etc. → resized to 400×400  
- `.txt`   → first 20 lines → 800×600 canvas  
- `.docx`  → first 5 paragraphs → 800×600 canvas  
- others   → generic “FILE” placeholder  

---

## Internal Helpers

- `_generate_pdf_thumbnail(src, dst)`  
- `_generate_image_thumbnail(src, dst)`  
- `_generate_txt_thumbnail(src, dst)`  
- `_generate_docx_thumbnail(src, dst)`  
- `_render_text_to_image(text, dst, size)`  
- `_copy_fallback_icon(dst)`

Each helper focuses on a single file type and is invoked by `create_thumbnail()`.

---

## Error Handling
- **Database errors** roll back their session and print a warning.  
- **Thumbnail errors** are caught per‐file so one bad document won’t stop the watcher.

---

## Integration Points
- **`watcher.py`** should call `process_new_file()` and `process_deleted_file()`.  
- **Front‐end** listens to SSE events pushed into `event_queue` for live updates.

---

> **Tip**: If you need to support more file types (e.g. PowerPoint), simply add
> a new `_generate_<ext>_thumbnail` helper and update `create_thumbnail()`.
