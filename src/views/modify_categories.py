from PyQt6.QtWidgets import QLabel, QVBoxLayout
from views.popup_window import PopUpWindow
from views.window_manager import WindowManager


class ModifyCategoriesWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.db = db
        self.popup_window = WindowManager()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Categories coming soon"))

        self.setLayout(layout)

