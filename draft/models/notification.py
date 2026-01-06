# models/notification.py
from .db import get_db

class NotificationModel:
    @staticmethod
    def create(user_id, message):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO notifications (user_id, message) VALUES (?,?)", (user_id, message))
        conn.commit()
        conn.close()

    @staticmethod
    def unread_for(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM notifications WHERE user_id=? AND is_read=0 ORDER BY created_at DESC", (user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def mark_read(notif_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE notifications SET is_read=1 WHERE id=?", (notif_id,))
        conn.commit()
        conn.close()
