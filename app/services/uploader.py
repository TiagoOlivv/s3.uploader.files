from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os

def upload_folder_parallel(s3, bucket, base_path: Path, update_progress):
    all_files = [p for p in base_path.rglob("*") if p.is_file()]
    total_files = len(all_files)
    uploaded_count = [0]

    def upload_file(path: Path):
        try:
            relative_path = path.relative_to(base_path)
            key = str(relative_path).replace(os.sep, "/")
            s3.upload_file(str(path), bucket, key)

            uploaded_count[0] += 1
            progress = int((uploaded_count[0] / total_files) * 100)
            update_progress(progress)
        except Exception as e:
            print(f"Error uploading {path}: {e}")

    with ThreadPoolExecutor() as executor:
        executor.map(upload_file, all_files)

    return uploaded_count[0]
