from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from controllers.reservation_controller import ReservationController
from controllers.notification_controller import NotificationController


class ProfessorDashboard(QWidget):
    def __init__(self, main_window, user):
        super().__init__()

        # --- Role check ---
        if user.get("role") != "Professor":
            QMessageBox.critical(
                main_window,
                "Access Denied",
                "This dashboard is restricted to professors only."
            )
            # Disable the widget so it cannot be used
            self.setDisabled(True)
            return

        self.main = main_window
        self.user = user
        self.res_ctrl = ReservationController()
        self.notif_ctrl = NotificationController()

        root = QVBoxLayout(self)
        hdr = QLabel(f"Welcome, {user['name']} (Professor)")
        hdr.setStyleSheet("font-size: 18px; font-weight: bold; padding-bottom: 6px;")
        hdr.setAlignment(Qt.AlignLeft)
        root.addWidget(hdr)

        root.addWidget(QLabel("Pending Reservations"))
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Student", "Inventory", "Start", "End", "Status"]
        )
        root.addWidget(self.table)

        actions = QHBoxLayout()
        btn_approve = QPushButton("Approve")
        btn_reject = QPushButton("Reject")
        actions.addWidget(btn_approve)
        actions.addWidget(btn_reject)
        root.addLayout(actions)

        btn_approve.clicked.connect(self.approve_selected)
        btn_reject.clicked.connect(self.reject_selected)

        notif_btn = QPushButton("View Notifications")
        notif_btn.clicked.connect(self.show_notifications)
        root.addWidget(notif_btn)

        self.load_pending()

    def load_pending(self):
        rows = self.res_ctrl.pending_for_professor()
        self.table.setRowCount(0)
        for r in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(r["user_id"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(r["inventory_id"])))
            self.table.setItem(row, 3, QTableWidgetItem(r["start_dt"]))
            self.table.setItem(row, 4, QTableWidgetItem(r["end_dt"]))
            self.table.setItem(row, 5, QTableWidgetItem(r["status"]))

    def _selected_res_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

    def approve_selected(self):
        res_id = self._selected_res_id()
        if not res_id:
            QMessageBox.warning(self, "Select reservation", "Choose a reservation first.")
            return
        self.res_ctrl.professor_approve(res_id, self.user["id"])
        QMessageBox.information(self, "Approved", "Reservation moved to admin approval.")
        self.load_pending()

    def reject_selected(self):
        res_id = self._selected_res_id()
        if not res_id:
            QMessageBox.warning(self, "Select reservation", "Choose a reservation first.")
            return
        self.res_ctrl.professor_reject(res_id, self.user["id"])
        QMessageBox.information(self, "Rejected", "Reservation cancelled.")
        self.load_pending()

    def show_notifications(self):
        rows = self.notif_ctrl.unread_for(self.user["id"])
        if not rows:
            QMessageBox.information(self, "Notifications", "No new notifications.")
            return
        msg = "\n".join([f"- {r['message']} ({r['created_at']})" for r in rows])
        QMessageBox.information(self, "Notifications", msg)
        for r in rows:
            self.notif_ctrl.mark_read(r["id"])
