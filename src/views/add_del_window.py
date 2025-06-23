from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

class AddDelWindow(QDialog):
    def __init__(self, window_name: str, min_width: int, min_height: int, parent=None) -> None:
        super().__init__(parent, Qt.WindowType.Dialog)
        self.setWindowTitle(window_name)
        self.setMinimumSize(min_width, min_height)
        self.setModal(True)
