import sqlite3
import os

db_path = "database/pii_redactor.db"
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n--- Files Table Content ---")
cursor.execute("SELECT id, original_filename, stored_input_path, stored_output_path, visual_output_path, file_type FROM files")
rows = cursor.fetchall()

for row in rows:
    fid, name, inp, outp, vis, ftype = row
    print(f"\nFile ID: {fid}")
    print(f"Name: {name}")
    print(f"Type: {ftype}")
    print(f"Input Path: {inp} (Exists: {os.path.exists(inp)})")
    print(f"Output Path: {outp} (Exists: {os.path.exists(outp) if outp else 'N/A'})")
    print(f"Visual Path: {vis} (Exists: {os.path.exists(vis) if vis else 'N/A'})")
    if vis and os.path.exists(vis):
        print(f"Visual Size: {os.path.getsize(vis)} bytes")

conn.close()
