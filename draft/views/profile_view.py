# views/profile_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt
from controllers.auth_controller import AuthController
from views.student_dashboard import StudentDashboard
from views.professor_dashboard import ProfessorDashboard
from views.admin_dashboard import AdminDashboard

class ProfileView(QWidget):
    def __init__(self, main_window, user):
        super().__init__()
        self.main = main_window
        self.user = user
        self.auth = AuthController()

        root = QVBoxLayout(self)

        # Header
        hdr_layout = QHBoxLayout()
        hdr = QLabel(f"Profile & Preferences — {user['name']}")
        hdr.setStyleSheet("font-size: 18px; font-weight: bold; padding-bottom: 6px;")
        hdr.setAlignment(Qt.AlignLeft)
        hdr_layout.addWidget(hdr)

        # Back button
        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #38b6ff; color: #570b0b; font-weight: bold;")
        btn_back.clicked.connect(self.go_back)
        hdr_layout.addWidget(btn_back, alignment=Qt.AlignRight)

        root.addLayout(hdr_layout)

        # Update Password Section
        box = QGroupBox("Update Password")
        layout = QVBoxLayout(box)
        self.cur_pass = QLineEdit(); self.cur_pass.setEchoMode(QLineEdit.Password); self.cur_pass.setPlaceholderText("Current Password")
        self.new_pass = QLineEdit(); self.new_pass.setEchoMode(QLineEdit.Password); self.new_pass.setPlaceholderText("New Password")
        self.confirm_pass = QLineEdit(); self.confirm_pass.setEchoMode(QLineEdit.Password); self.confirm_pass.setPlaceholderText("Confirm New Password")
        btn_update = QPushButton("Update Password")
        layout.addWidget(self.cur_pass)
        layout.addWidget(self.new_pass)
        layout.addWidget(self.confirm_pass)
        layout.addWidget(btn_update)
        root.addWidget(box)

        # Notification Preferences
        prefs = QGroupBox("Notification Preferences")
        p_layout = QVBoxLayout(prefs)
        self.chk_email = QCheckBox("Email notifications"); self.chk_email.setChecked(True)
        self.chk_inapp = QCheckBox("In-app notifications"); self.chk_inapp.setChecked(True)
        btn_save_prefs = QPushButton("Save Preferences")
        p_layout.addWidget(self.chk_email)
        p_layout.addWidget(self.chk_inapp)
        p_layout.addWidget(btn_save_prefs)
        root.addWidget(prefs)

        btn_update.clicked.connect(self.update_password)
        btn_save_prefs.clicked.connect(self.save_prefs)

    def update_password(self):
        if not self.cur_pass.text() or not self.new_pass.text() or not self.confirm_pass.text():
            QMessageBox.warning(self, "Missing fields", "Please fill in all password fields.")
            return
        if self.new_pass.text() != self.confirm_pass.text():
            QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
            return
        ok = self.auth.change_password(self.user["id"], self.cur_pass.text(), self.new_pass.text())
        if ok:
            QMessageBox.information(self, "Success", "Password updated successfully.")
            self.cur_pass.clear(); self.new_pass.clear(); self.confirm_pass.clear()
        else:
            QMessageBox.critical(self, "Error", "Invalid current password.")

    def save_prefs(self):
        try:
            self.auth.update_prefs(self.user["id"], self.chk_email.isChecked(), self.chk_inapp.isChecked())
            QMessageBox.information(self, "Saved", "Preferences updated.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def go_back(self):
        """Return to the correct dashboard based on user role."""
        role = self.user.get("role", "student")
        if role == "student":
            dashboard = StudentDashboard(self.main, self.user)
        elif role == "professor":
            dashboard = ProfessorDashboard(self.main, self.user)
        else:
            dashboard = AdminDashboard(self.main, self.user)

        self.main.stack.addWidget(dashboard)
        self.main.stack.setCurrentWidget(dashboard)
