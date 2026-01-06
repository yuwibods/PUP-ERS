from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QGroupBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from controllers.reservation_controller import ReservationController
from controllers.inventory_controller import InventoryController
from controllers.notification_controller import NotificationController


class AdminDashboard(QWidget):
    def __init__(self, main_window, user):
        super().__init__()

        # --- Role check ---
        if user.get("role") != "Admin":
            # If a non-admin somehow tries to open this view, show an error and block
            QMessageBox.critical(
                main_window,
                "Access Denied",
                "This dashboard is restricted to administrators only."
            )
            # Optionally hide/disable the widget
            self.setDisabled(True)
            return

        self.main = main_window
        self.user = user
        self.res_ctrl = ReservationController()
        self.inv_ctrl = InventoryController()
        self.notif_ctrl = NotificationController()

        root = QVBoxLayout(self)
        hdr = QLabel(f"Welcome, {user['name']} (Admin)")
        hdr.setStyleSheet("font-size: 18px; font-weight: bold; padding-bottom: 6px;")
        hdr.setAlignment(Qt.AlignLeft)
        root.addWidget(hdr)

        # --- Inventory Management ---
        inv_box = QGroupBox("Inventory Dashboard & Management")
        inv_layout = QVBoxLayout(inv_box)

        self.inv_name = QLineEdit(); self.inv_name.setPlaceholderText("Name")
        self.inv_cat = QLineEdit(); self.inv_cat.setPlaceholderText("Category")
        self.inv_qty = QLineEdit(); self.inv_qty.setPlaceholderText("Quantity")
        self.inv_status = QComboBox(); self.inv_status.addItems(["available", "unavailable", "maintenance"])

        btn_add = QPushButton("Add Inventory")
        btn_update = QPushButton("Update Selected Inventory")
        btn_delete = QPushButton("Delete Selected Inventory")
        btn_refresh = QPushButton("Refresh Inventory")

        inv_layout.addWidget(self.inv_name)
        inv_layout.addWidget(self.inv_cat)
        inv_layout.addWidget(self.inv_qty)
        inv_layout.addWidget(self.inv_status)
        inv_layout.addWidget(btn_add)
        inv_layout.addWidget(btn_update)
        inv_layout.addWidget(btn_delete)
        inv_layout.addWidget(btn_refresh)
        root.addWidget(inv_box)

        self.inv_table = QTableWidget(0, 5)
        self.inv_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Quantity", "Status"])
        root.addWidget(self.inv_table)

        # --- Connections ---
        btn_add.clicked.connect(self.add_inventory)
        btn_update.clicked.connect(self.update_inventory)
        btn_delete.clicked.connect(self.delete_inventory)
        btn_refresh.clicked.connect(self.refresh_inventory)

        self.inv_table.cellClicked.connect(self.select_inventory)

        self.refresh_inventory()

    # ... rest of methods unchanged ...