import sys
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
