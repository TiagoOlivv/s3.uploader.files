from PyQt6.QtWidgets import (
    QVBoxLayout, QLineEdit, QLabel, QPushButton, QProgressBar, QCheckBox
)

from .styles import STYLE_SHEET
from .utils import check_all_fields_filled
from utils.settings import save_config, load_config


def setup_ui(self):
    self.setStyleSheet(STYLE_SHEET)

    self.layout = QVBoxLayout()

    self.region = QLineEdit()
    self.access_key = QLineEdit()
    self.secret_key = QLineEdit()
    self.bucket_name = QLineEdit()

    self.inputs = [self.region, self.access_key, self.secret_key, self.bucket_name]
    for field in self.inputs:
        field.textChanged.connect(lambda: check_all_fields_filled(self))

    self.folder_path = None
    self.folder_button = QPushButton("Click to select folder")
    self.folder_button.clicked.connect(self.select_folder)
    self.folder_button_active_style = """
        QPushButton {
            text-align: left;
            color: #ffffff;
            background-color: #3c3f41;
            border: 1px solid #5c5c5c;
        }
    """

    self.upload_button = QPushButton("Start Upload")
    self.upload_button.setEnabled(False)
    self.upload_button.clicked.connect(self.start_upload)

    self.progress = QProgressBar()
    self.progress.setValue(0)

    add_form_row(self, "AWS Region:", self.region)
    add_form_row(self, "Access Key:", self.access_key)
    add_form_row(self, "Secret Key:", self.secret_key)
    add_form_row(self, "Bucket Name:", self.bucket_name)

    self.layout.addWidget(QLabel("Folder to Upload:"))
    self.layout.addWidget(self.folder_button)
    self.layout.addWidget(self.upload_button)
    self.layout.addWidget(self.progress)

    self.save_checkbox = QCheckBox("Save credentials")
    self.layout.addWidget(self.save_checkbox)

    config = load_config()
    if config:
        self.region.setText(config.get("region", ""))
        self.access_key.setText(config.get("access_key", ""))
        self.secret_key.setText(config.get("secret_key", ""))
        self.bucket_name.setText(config.get("bucket_name", ""))
        self.save_checkbox.setChecked(True)

    self.setLayout(self.layout)

def add_form_row(self, label_text, widget):
    label = QLabel(label_text)
    self.layout.addWidget(label)
    self.layout.addWidget(widget)
