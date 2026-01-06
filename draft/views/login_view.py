from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QPainter
from PySide6.QtCore import Qt
from controllers.auth_controller import AuthController

class LoginView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.ctrl = AuthController()
        self.selected_role = None

        # Preload images once
        self.bg_pixmap = QPixmap("assets/pup_bg_image.png")
        self.logo_pixmap = QPixmap("assets/pup_logo.png")
        self.icon_pixmap = QPixmap("assets/pup_ers_icon.png")
        self.scaled_bg = None

        # --- Root layout ---
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(15)

        # --- Header (top-left corner, transparent) ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.logo = QLabel()
        self.logo.setStyleSheet("background: transparent;")
        self.icon = QLabel()
        self.icon.setStyleSheet("background: transparent;")
        self.title = QLabel("PUP-ERS")
        self.title.setFont(QFont("Times New Roman", 28, QFont.Weight.Bold))
        self.title.setStyleSheet("color: white; background: transparent;")

        header_layout.addWidget(self.logo)
        header_layout.addWidget(self.icon)
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        root.addLayout(header_layout)

        # --- Spacer to push role selection to center ---
        root.addSpacerItem(QSpacerItem(
            20, 60,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding
        ))

        # --- Role selection dropdown ---
        self.role_box = QComboBox()
        self.role_box.setPlaceholderText("Select a role")
        self.role_box.addItems(["Student", "Faculty", "Admin"])
        self.role_box.setFixedWidth(250)
        self.role_box.setStyleSheet("background-color: white; color: black; padding: 6px;")

        btn_confirm_role = QPushButton("Confirm Role")
        btn_confirm_role.setFixedWidth(250)
        btn_confirm_role.setStyleSheet("background-color: white; color: black; padding: 8px; font-weight: bold;")

        role_layout = QVBoxLayout()
        role_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_layout.addWidget(self.role_box)
        role_layout.addWidget(btn_confirm_role)
        root.addLayout(role_layout)

        # --- Middle descriptive text (hidden after role confirmation) ---
        self.desc = QLabel(
            "A Students’ Easy Reservation System for Equipment and Inventory\n"
            "Polytechnic University of the Philippines."
        )
        self.desc.setFont(QFont("Times New Roman", 14))
        self.desc.setStyleSheet("color: white; background: transparent;")
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.desc)

        # --- Auth form (hidden until role confirmed) ---
        self.email = QLineEdit(); self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Password")
        self.btn_login = QPushButton("Sign In")
        self.btn_signup = QPushButton("Sign Up")
        self.btn_forgot = QPushButton("Forgot Password?")

        for w in [self.email, self.password, self.btn_login, self.btn_signup, self.btn_forgot]:
            w.setFixedWidth(250)
            w.setStyleSheet("background-color: white; color: black; padding: 8px;")
            w.hide()

        auth_layout = QVBoxLayout()
        auth_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        auth_layout.addWidget(self.email)
        auth_layout.addWidget(self.password)
        auth_layout.addWidget(self.btn_login)
        auth_layout.addWidget(self.btn_signup)
        auth_layout.addWidget(self.btn_forgot)
        root.addLayout(auth_layout)

        # --- Spacer before disclaimer ---
        root.addSpacerItem(QSpacerItem(
            20, 40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding
        ))

        # --- Disclaimer at bottom ---
        disclaimer = QLabel(
            'By using this service, you understood and agree to the PUP Online Services '
            '<a href="https://www.pup.edu.ph/terms" style="color:#38b6ff;">Terms of Use</a> and '
            '<a href="https://www.pup.edu.ph/privacy" style="color:#38b6ff;">Privacy Statement</a>'
        )
        disclaimer.setFont(QFont("Times New Roman", 10))
        disclaimer.setStyleSheet("color: white; background: transparent;")
        disclaimer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        disclaimer.setOpenExternalLinks(True)
        disclaimer.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        root.addWidget(disclaimer)

        # --- Connections ---
        btn_confirm_role.clicked.connect(self.confirm_role)
        self.btn_login.clicked.connect(self.login)
        self.btn_signup.clicked.connect(self.open_signup)
        self.btn_forgot.clicked.connect(self.forgot_password)

    def resizeEvent(self, event):
        """Rescale background, title font, and icons only when window size changes."""
        if not self.bg_pixmap.isNull():
            self.scaled_bg = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

        # Scale title font relative to window height
        font_size = max(28, int(self.height() * 0.05))
        self.title.setFont(QFont("Times New Roman", font_size, QFont.Weight.Bold))

        # Scale icons to match font size and apply circular mask
        def make_circular(pixmap: QPixmap, diameter: int) -> QPixmap:
            if pixmap.isNull() or diameter <= 0:
                return QPixmap()
            scaled = pixmap.scaled(
                diameter, diameter,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            mask = QPixmap(diameter, diameter)
            mask.fill(Qt.GlobalColor.transparent)
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(Qt.GlobalColor.white)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, diameter, diameter)
            painter.end()
            scaled.setMask(mask.createMaskFromColor(Qt.GlobalColor.transparent))
            return scaled

        icon_size = font_size
        self.logo.setPixmap(make_circular(self.logo_pixmap, icon_size))
        self.icon.setPixmap(make_circular(self.icon_pixmap, icon_size))

        super().resizeEvent(event)

    def paintEvent(self, event):
        """Draw cached background image."""
        painter = QPainter(self)
        if self.scaled_bg and not self.scaled_bg.isNull():
            painter.drawPixmap(self.rect(), self.scaled_bg)
        super().paintEvent(event)

    def confirm_role(self):
        role = self.role_box.currentText()
        if role == "Select Role":
            QMessageBox.warning(self, "Role Required", "Please select a role before proceeding.")
            return
        self.selected_role = role
        QMessageBox.information(self, "Role Confirmed", f"Role '{role}' confirmed. Proceed to Sign In / Sign Up.")

        # Hide descriptive text after role confirmation
        self.desc.hide()

        # Show auth form
        for w in [self.email, self.password, self.btn_login, self.btn_signup, self.btn_forgot]:
            w.show()
        self.role_box.setEnabled(False)

    def login(self):
        user = self.ctrl.login(self.email.text().strip(), self.password.text())
        if user:
            user["role"] = self.selected_role
            self.main.login_success(user)
        else:
            QMessageBox.critical(self, "Login failed", "Invalid credentials.")

    def open_signup(self):
        try:
            success = self.ctrl.signup(
                "New User",
                self.email.text().strip(),
                self.password.text(),
                self.selected_role
            )
            if success:
                QMessageBox.information(self, "Success", "Account created. You can log in now.")
            else:
                QMessageBox.warning(self, "Signup Failed", "Account could not be created. Email may already exist.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def forgot_password(self):
        email = self.email.text().strip()
        if not email:
            QMessageBox.warning(self, "Missing email", "Enter your email first.")
            return
        QMessageBox.information(self, "Reset Password", "Password reset flow goes here.")
