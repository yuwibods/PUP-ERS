# models/user.py
from .db import get_db
import sqlite3

class UserModel:
    @staticmethod
    def by_email(email):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def by_id(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def create(name, email, password, role):
        conn = get_db()
        try:
            cur = conn.cursor()
            # Check if email already exists
            cur.execute("SELECT id FROM users WHERE email=?", (email,))
            existing = cur.fetchone()
            if existing:
                return False  # Email already taken

            cur.execute(
                "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                (name, email, password, role)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print("DB Error:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def change_password(user_id, new_password):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_prefs(user_id, notify_email, notify_inapp):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET notify_email=?, notify_inapp=? WHERE id=?",
                    (int(notify_email), int(notify_inapp), user_id))
        conn.commit()
        conn.close()
