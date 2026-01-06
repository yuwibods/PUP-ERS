# views/calendar_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import QDate
from PySide6.QtGui import QColor
from controllers.reservation_controller import ReservationController

STATUS_COLORS = {
    "pending_prof": QColor("#ff914d"),
    "pending_admin": QColor("#ff914d"),
    "approved": QColor("#3cb371"),
    "cancelled": QColor("#ff4d4d"),
    "return_requested": QColor("#38b6ff"),
    "returned": QColor("#6a5acd"),
    "modified": QColor("#f5c518")
}

class CalendarView(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.res_ctrl = ReservationController()

        layout = QVBoxLayout(self)
        header = QHBoxLayout()
        header.addWidget(QLabel("Weekly Calendar View"))
        btn_add = QPushButton("+")
        btn_add.setToolTip("Quick reserve")
        btn_add.clicked.connect(self.quick_reserve)
        header.addWidget(btn_add)
        layout.addLayout(header)

        self.table = QTableWidget(12, 7)
        self.table.setHorizontalHeaderLabels(
            [QDate.currentDate().addDays(i).toString("ddd dd") for i in range(7)]
        )
        self.table.setVerticalHeaderLabels([f"{h}:00" for h in range(8, 20)])
        layout.addWidget(self.table)

        self.table.cellDoubleClicked.connect(self.cell_clicked)
        self.load_week_view()

    def load_week_view(self):
        self.table.clearContents()
        reservations = self.res_ctrl.student_history(self.user["id"])
        for r in reservations:
            try:
                start_date = r["start_dt"].split(" ")[0]
                start_hour = int(r["start_dt"].split(" ")[1][:2])
                date_obj = QDate.fromString(start_date, "yyyy-MM-dd")
                day_offset = QDate.currentDate().daysTo(date_obj)
                if 0 <= day_offset < 7:
                    col = day_offset
                    row = start_hour - 8
                    if 0 <= row < 12:
                        item = QTableWidgetItem(f"Res {r['id']} ({r['status']})")
                        color = STATUS_COLORS.get(r["status"], QColor("#a64b4b"))
                        item.setBackground(color)
                        self.table.setItem(row, col, item)
            except Exception:
                continue

    def cell_clicked(self, row, col):
        day = QDate.currentDate().addDays(col).toString("yyyy-MM-dd")
        hour = 8 + row
        QMessageBox.information(self, "Time Block", f"Selected: {day} {hour:02d}:00\nUse dashboard to reserve.")

    def quick_reserve(self):
        QMessageBox.information(self, "Quick Reserve", "Use the Student Dashboard to select item and time.")
