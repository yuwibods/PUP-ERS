# app.py
import sys
from PySide6.QtWidgets import QApplication  , QMainWindow, QStackedWidget, QToolBar
from PySide6.QtGui import QAction
from models.db import init_db
from views.login_view import LoginView
from views.student_dashboard import StudentDashboard
from views.professor_dashboard import ProfessorDashboard
from views.admin_dashboard import AdminDashboard
from views.profile_view import ProfileView

GLOBAL_STYLESHEET = """
    QWidget {
        background-color: #1e1e1e;   /* neutral dark workspace */
        color: #f7f5f2;
        font-family: 'Times New Roman';
        font-size: 14px;
    }
    QLabel {
        color: #f7f5f2;
    }
    QPushButton {
        background-color: #38b6ff;
        color: #ffffff;
        font-weight: bold;
        border-radius: 6px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #1f8ed6;
    }
    QLineEdit {
        background-color: #2c2c2c;
        color: #f7f5f2;
        border: 1px solid #38b6ff;
        border-radius: 4px;
        padding: 6px;
    }
    QTableWidget {
        background-color: #2c2c2c;
        color: #f7f5f2;
        gridline-color: #444444;
        selection-background-color: #38b6ff;
        selection-color: #ffffff;
        alternate-background-color: #333333;
    }
    QHeaderView::section {
        background-color: #570b0b;   /* brand maroon for headers */
        color: #f7f5f2;
        font-weight: bold;
        padding: 6px;
        border: none;
    }
    QGroupBox {
        border: 1px solid #444444;
        border-radius: 6px;
        margin-top: 8px;
        padding: 8px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 4px;
        color: #38b6ff;
        font-weight: bold;
    }
    QToolBar {
        background-color: #570b0b;
        spacing: 8px;
        padding: 6px;
        border: none;
    }
    QToolButton {
        color: #38b6ff;
        font-weight: bold;
    }
    QMessageBox {
        background-color: #2c2c2c;
        color: #f7f5f2;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Reservation System")
        self.resize(1200, 800)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        init_db()

        self.login_view = LoginView(self)
        self.stack.addWidget(self.login_view)
        self.stack.setCurrentWidget(self.login_view)

        self.toolbar = QToolBar("Main")
        self.addToolBar(self.toolbar)
        self.act_profile = QAction("Profile", self)
        self.act_notifications = QAction("Notifications", self)
        self.act_logout = QAction("Logout", self)
        self.act_profile.triggered.connect(self.show_profile)
        self.act_notifications.triggered.connect(self.show_notifications)
        self.act_logout.triggered.connect(self.logout)
        self.toolbar.addAction(self.act_profile)
        self.toolbar.addAction(self.act_notifications)
        self.toolbar.addAction(self.act_logout)
        self.toolbar.setVisible(False)

        self.user = None
        self.dashboard = None

    def login_success(self, user):
        self.user = user
        self.toolbar.setVisible(True)

        # Normalize role string to lowercase
        role = user.get("role", "").lower()

        # Decide which dashboard class to use
        if role == "student":
            dashboard_cls = StudentDashboard
        elif role == "professor":
            dashboard_cls = ProfessorDashboard
        elif role == "admin":
            dashboard_cls = AdminDashboard
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Access Denied", f"Unknown role: {user.get('role')}")
            return

        # If we already have a dashboard, remove it before creating a new one
        if self.dashboard is not None:
            self.stack.removeWidget(self.dashboard)
            self.dashboard.deleteLater()

        # Create and show the new dashboard
        self.dashboard = dashboard_cls(self, user)
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)

    def show_profile(self):
        profile_view = ProfileView(self, self.user)
        self.stack.addWidget(profile_view)
        self.stack.setCurrentWidget(profile_view)

    def show_notifications(self):
        # Each dashboard implements show_notifications() to open its notification panel
        if hasattr(self.dashboard, "show_notifications"):
            self.dashboard.show_notifications()

    def logout(self):
        self.toolbar.setVisible(False)
        self.stack.setCurrentWidget(self.login_view)
        self.user = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


