from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QThread
from .layout import setup_ui
from .utils import check_all_fields_filled
from utils.s3 import create_s3_client, ensure_bucket_exists
from utils.settings import save_config
from services.uploader_worker import UploaderWorker
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 440)
        self.setWindowTitle("S3 Parallel Image Uploader")
        setup_ui(self)
        self.upload_thread = None
        self.worker = None

    def select_folder(self):
        from PyQt6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.folder_button.setText(folder)
            self.folder_button.setStyleSheet(self.folder_button_active_style)
            check_all_fields_filled(self)

    def start_upload(self):
        region = self.region.text().strip()
        key = self.access_key.text().strip()
        secret = self.secret_key.text().strip()
        bucket = self.bucket_name.text().strip()
        folder = self.folder_path

        if not all([region, key, secret, bucket, folder]):
            QMessageBox.critical(self, "Error", "All fields are required.")
            return

        try:
            s3 = create_s3_client(region, key, secret)
            ensure_bucket_exists(s3, bucket, region)
        except Exception as e:
            QMessageBox.critical(self, "AWS Error", str(e))
            return

        self.upload_button.setEnabled(False)
        self.upload_button.setText("Uploading...")
        self.progress.setValue(0)

        self.upload_thread = QThread()
        self.worker = UploaderWorker(s3, bucket, Path(folder))
        self.worker.moveToThread(self.upload_thread)

        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.upload_complete.connect(self.on_upload_complete)
        self.worker.upload_failed.connect(self.on_upload_failed)

        self.upload_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.upload_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.upload_thread.finished.connect(self.upload_thread.deleteLater)

        self.upload_thread.start()

    def on_upload_complete(self, total_uploaded):
        self.upload_button.setEnabled(True)
        self.upload_button.setText("Start Upload")
        QMessageBox.information(self, "Done", f"Uploaded {total_uploaded} files.")

        if self.save_checkbox.isChecked():
            save_config({
                "region": self.region.text().strip(),
                "access_key": self.access_key.text().strip(),
                "secret_key": self.secret_key.text().strip(),
                "bucket_name": self.bucket_name.text().strip()
            })
        else:
            save_config({})

    def on_upload_failed(self, error_message):
        self.upload_button.setEnabled(True)
        self.upload_button.setText("Start Upload")
        QMessageBox.critical(self, "Upload Failed", error_message)
