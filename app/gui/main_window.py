from PyQt6.QtWidgets import QWidget, QMessageBox
from .layout import setup_ui
from .utils import check_all_fields_filled
from utils.s3 import create_s3_client, ensure_bucket_exists
from utils.settings import save_config
from services.uploader import upload_folder_parallel
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 440)
        self.setWindowTitle("S3 Parallel Files Uploader")

        setup_ui(self)

    def select_folder(self):
        self.progress.setValue(0)

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

        uploaded_count = upload_folder_parallel(
            s3=s3,
            bucket=bucket,
            base_path=Path(folder),
            update_progress=self.progress.setValue
        )

        self.upload_button.setEnabled(True)
        self.upload_button.setText("Start Upload")
        QMessageBox.information(self, "Done", f"Uploaded {uploaded_count} files.")

        if self.save_checkbox.isChecked():
            save_config({
                "region": region,
                "access_key": key,
                "secret_key": secret,
                "bucket_name": bucket
            })
        else:
            save_config({})
