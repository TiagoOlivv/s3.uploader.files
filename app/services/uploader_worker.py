from PyQt6.QtCore import QObject, pyqtSignal
from services.uploader import upload_folder_parallel
from pathlib import Path

class UploaderWorker(QObject):
    progress_updated = pyqtSignal(int)
    upload_complete = pyqtSignal(int)
    upload_failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, s3, bucket, base_path):
        super().__init__()
        self.s3 = s3
        self.bucket = bucket
        self.base_path = base_path

    def run(self):
        try:
            total_uploaded = upload_folder_parallel(
                s3=self.s3,
                bucket=self.bucket,
                base_path=self.base_path,
                update_progress=self.progress_updated.emit
            )
            self.upload_complete.emit(total_uploaded)
        except Exception as e:
            self.upload_failed.emit(str(e))
        finally:
            self.finished.emit()
