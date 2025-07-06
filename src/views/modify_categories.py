from PyQt6.QtWidgets import QLabel, QPushButton, QTableWidget, QVBoxLayout

from views.popup_window import PopUpWindow
from views.window_manager import WindowManager

from .add_categories_window import AddCategoriesWindow
from .del_categories_window import DelCategoriesWindow

class ModifyCategoriesWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.db = db
        self.popup_window = WindowManager()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Categories coming soon"))

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(["Name", "Type"])
        layout.addWidget(self.summary_table)

        add_category_btn = QPushButton("Add")
        add_category_btn.clicked.connect(lambda: self.popup_window.open_window(AddCategoriesWindow("Add Categories", 300, 400, self.db)))
        layout.addWidget(add_category_btn)

        del_category_btn = QPushButton("Delete")
        del_category_btn.clicked.connect(lambda: self.popup_window.open_window(DelCategoriesWindow("Delete Categories", 300, 400, self.db)))
        layout.addWidget(del_category_btn)

        self.setLayout(layout)

