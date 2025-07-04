from PyQt6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from controllers.db.account_db_service import AccountDBService
from views.popup_window import PopUpWindow

class DelAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.account_db_service = AccountDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        title_lable = QLabel("Delete Accounts")
        title_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lable)

        form_layout = QFormLayout()

        self.select_account_combo = QComboBox()
        accounts = self.account_db_service.select_name_id_all_accounts() # name , id tuple
        account_names = [row[0] for row in accounts] # type: ignore
        self.select_account_combo.addItems(account_names) # type: ignore
        form_layout.addRow("Select Account:", self.select_account_combo)

        self.change_or_del_checkbox = QCheckBox()
        form_layout.addRow("Transfer transactions to separate account:", self.change_or_del_checkbox)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        add_account_btn = QPushButton("Delete Account")
        add_account_btn.clicked.connect(self.del_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def del_account(self):
        return
