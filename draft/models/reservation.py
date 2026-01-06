# models/reservation.py
from .db import get_db

class ReservationModel:
    @staticmethod
    def create(user_id, inventory_id, start_dt, end_dt):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (user_id, inventory_id, start_dt, end_dt)
            VALUES (?,?,?,?)
        """, (user_id, inventory_id, start_dt, end_dt))
        conn.commit()
        conn.close()

    @staticmethod
    def by_student(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM reservations
            WHERE user_id=?
            ORDER BY created_at DESC
        """, (user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def by_status(status):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reservations WHERE status=? ORDER BY created_at DESC", (status,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get(res_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reservations WHERE id=?", (res_id,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def update_status(res_id, status):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE reservations SET status=? WHERE id=?", (status, res_id))
        conn.commit()
        conn.close()

    @staticmethod
    def modify_times(res_id, start_dt, end_dt):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE reservations SET start_dt=?, end_dt=? WHERE id=?",
                    (start_dt, end_dt, res_id))
        conn.commit()
        conn.close()
