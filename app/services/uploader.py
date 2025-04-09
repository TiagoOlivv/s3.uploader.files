from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os

def get_all_files(base_path: Path):
    return [f for f in base_path.rglob("*") if f.is_file()]

def upload_file(s3, bucket: str, base_path: Path, file_path: Path):
    relative_path = file_path.relative_to(base_path)
    s3.upload_file(str(file_path), bucket, str(relative_path))

def upload_folder_parallel(s3, bucket: str, base_path: Path, update_progress):
    files = get_all_files(base_path)
    total_files = len(files)
    completed = 0

    import multiprocessing
    max_workers = max(1, multiprocessing.cpu_count())

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(upload_file, s3, bucket, base_path, f) for f in files]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error uploading file: {e}")
            completed += 1
            progress = int((completed / total_files) * 100)
            update_progress(progress)

    return completed
