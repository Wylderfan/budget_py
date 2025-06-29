from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

class PopUpWindow(QDialog):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(parent, Qt.WindowType.Dialog)
        self.db = db
        self.setWindowTitle(window_name)
        self.setMinimumSize(min_width, min_height)
        self.setModal(True)

    def get_db(self):
        return self.db

