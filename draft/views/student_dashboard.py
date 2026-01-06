from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from controllers.inventory_controller import InventoryController
from controllers.reservation_controller import ReservationController
from views.calendar_view import CalendarView


class StudentDashboard(QWidget):
    def __init__(self, main_window, user):
        super().__init__()

        # --- Role check ---
        if user.get("role") != "Student":
            QMessageBox.critical(
                main_window,
                "Access Denied",
                "This dashboard is restricted to students only."
            )
            # Disable the widget so it cannot be used
            self.setDisabled(True)
            return

        self.main = main_window
        self.user = user
        self.inv_ctrl = InventoryController()
        self.res_ctrl = ReservationController()

        root = QVBoxLayout(self)

        hdr = QLabel(f"Welcome, {user['name']} (Student)")
        hdr.setStyleSheet("font-size: 18px; font-weight: bold; padding-bottom: 6px;")
        hdr.setAlignment(Qt.AlignLeft)
        root.addWidget(hdr)

        # --- Inventory search ---
        box = QGroupBox("Inventory discovery & selection")
        b_layout = QVBoxLayout(box)
        self.q_name = QLineEdit(); self.q_name.setPlaceholderText("Search name")
        self.q_cat = QLineEdit(); self.q_cat.setPlaceholderText("Category")
        btn_search = QPushButton("Search")
        b_layout.addWidget(self.q_name)
        b_layout.addWidget(self.q_cat)
        b_layout.addWidget(btn_search)
        root.addWidget(box)

        self.inv_table = QTableWidget(0, 4)
        self.inv_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Quantity"])
        root.addWidget(self.inv_table)

        # --- Reservation scheduling ---
        rbox = QGroupBox("Reservation scheduling & tracking")
        r_layout = QVBoxLayout(rbox)
        self.start_dt = QLineEdit(); self.start_dt.setPlaceholderText("Start (YYYY-MM-DD HH:MM)")
        self.end_dt = QLineEdit(); self.end_dt.setPlaceholderText("End (YYYY-MM-DD HH:MM)")
        btn_reserve = QPushButton("Reserve selected item")
        r_layout.addWidget(self.start_dt)
        r_layout.addWidget(self.end_dt)
        r_layout.addWidget(btn_reserve)
        root.addWidget(rbox)

        # --- Reservation history ---
        hist_hdr = QLabel("Personal reservation history")
        hist_hdr.setStyleSheet("font-size: 16px; font-weight: bold; padding: 6px 0;")
        root.addWidget(hist_hdr)

        self.hist_table = QTableWidget(0, 5)
        self.hist_table.setHorizontalHeaderLabels(["ID", "Item", "Start", "End", "Status"])
        root.addWidget(self.hist_table)

        act = QHBoxLayout()
        btn_modify = QPushButton("Modify pending")
        btn_cancel = QPushButton("Cancel pending")
        btn_return = QPushButton("Request return")
        act.addWidget(btn_modify)
        act.addWidget(btn_cancel)
        act.addWidget(btn_return)
        root.addLayout(act)

        # --- Calendar view ---
        cal_hdr = QLabel("Interactive Calendar View")
        cal_hdr.setStyleSheet("font-size: 16px; font-weight: bold; padding: 6px 0;")
        root.addWidget(cal_hdr)

        self.calendar_view = CalendarView(user)
        root.addWidget(self.calendar_view)

        # --- Connections ---
        btn_search.clicked.connect(self.search_inventory)
        btn_reserve.clicked.connect(self.reserve_selected)
        btn_modify.clicked.connect(self.modify_pending)
        btn_cancel.clicked.connect(self.cancel_pending)
        btn_return.clicked.connect(self.request_return)

        self.refresh_history()
        self.refresh_calendar()

    # ---- Calendar refresh ----
    def refresh_calendar(self):
        if hasattr(self.calendar_view, "load_week_view"):
            self.calendar_view.load_week_view()
        elif hasattr(self.calendar_view, "load_day_view"):
            self.calendar_view.load_day_view()

    # ---- Inventory search ----
    def search_inventory(self):
        rows = self.inv_ctrl.search(self.q_name.text(), self.q_cat.text())
        self.inv_table.setRowCount(0)
        for r in rows:
            row = self.inv_table.rowCount()
            self.inv_table.insertRow(row)
            self.inv_table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
            self.inv_table.setItem(row, 1, QTableWidgetItem(r["name"]))
            self.inv_table.setItem(row, 2, QTableWidgetItem(r["category"]))
            self.inv_table.setItem(row, 3, QTableWidgetItem(str(r["quantity"])))

    def _selected_inventory_id(self):
        row = self.inv_table.currentRow()
        if row < 0:
            return None
        return int(self.inv_table.item(row, 0).text())

    # ---- Reservation actions ----
    def reserve_selected(self):
        item_id = self._selected_inventory_id()
        if not item_id:
            QMessageBox.warning(self, "Select item", "Choose an inventory item first.")
            return
        try:
            self.res_ctrl.create(self.user["id"], item_id, self.start_dt.text(), self.end_dt.text())
            QMessageBox.information(self, "Reservation", "Reservation created—pending professor approval.")
            self.refresh_history()
            self.refresh_calendar()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def refresh_history(self):
        rows = self.res_ctrl.student_history(self.user["id"])
        self.hist_table.setRowCount(0)
        for r in rows:
            row = self.hist_table.rowCount()
            self.hist_table.insertRow(row)
            self.hist_table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
            self.hist_table.setItem(row, 1, QTableWidgetItem(str(r["inventory_id"])))
            self.hist_table.setItem(row, 2, QTableWidgetItem(r["start_dt"]))
            self.hist_table.setItem(row, 3, QTableWidgetItem(r["end_dt"]))
            self.hist_table.setItem(row, 4, QTableWidgetItem(r["status"]))

    def _selected_history_id(self):
        row = self.hist_table.currentRow()
        if row < 0:
            return None
        return int(self.hist_table.item(row, 0).text())

    def modify_pending(self):
        res_id = self._selected_history_id()
        if not res_id:
            QMessageBox.warning(self, "Select reservation", "Choose a reservation from history.")
            return
        self.res_ctrl.modify_pending(res_id, self.user["id"], notes="Updated by student")
        QMessageBox.information(self, "Updated", "Reservation updated (if pending).")
        self.refresh_history()
        self.refresh_calendar()

    def cancel_pending(self):
        res_id = self._selected_history_id()
        if not res_id:
            QMessageBox.warning(self, "Select reservation", "Choose a reservation from history.")
            return
        self.res_ctrl.cancel_pending(res_id, self.user["id"])
        QMessageBox.information(self, "Cancelled", "Reservation cancelled (if pending).")
        self.refresh_history()
        self.refresh_calendar()

    def request_return(self):
        res_id = self._selected_history_id()
        if not res_id:
            QMessageBox.warning(self, "Select reservation", "Choose a reservation from history.")
            return
        self.res_ctrl.request_return(res_id, self.user["id"])
        QMessageBox.information(self, "Requested", "Return requested.")
        self.refresh_history()
        self.refresh_calendar()