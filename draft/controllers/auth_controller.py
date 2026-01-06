# controllers/auth_controller.py
from models.user import UserModel


class AuthController:
    def login(self, email, password):
        user = UserModel.by_email(email)
        if user and user["password"] == password:
            return {"id": user["id"], "name": user["name"], "role": user["role"]}
        return None

    def signup(self, name, email, password, role):
        # Map UI role labels to DB values
        role_map = {
            "Student": "student",
            "Faculty": "professor",
            "Admin": "admin"
        }
        normalized_role = role_map.get(role, role.lower())
        return UserModel.create(name, email, password, normalized_role)

    def change_password(self, user_id, current_password, new_password):
        user = UserModel.by_id(user_id)
        if not user or user["password"] != current_password:
            return False
        UserModel.change_password(user_id, new_password)
        return True

    def update_prefs(self, user_id, notify_email, notify_inapp):
        UserModel.update_prefs(user_id, notify_email, notify_inapp)

    def send_otp(self, email, otp):
        print(f"[OTP] Sending {otp} to {email}")

    def update_password_by_email(self, email, new_password):
        from models.db import get_db
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
        conn.commit()
        conn.close()
        return True
