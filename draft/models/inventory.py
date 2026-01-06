# models/inventory.py
from .db import get_db

class InventoryModel:
    @staticmethod
    def search(name="", category=""):
        conn = get_db()
        cur = conn.cursor()
        query = "SELECT * FROM inventory WHERE 1=1"
        params = []
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if category:
            query += " AND category LIKE ?"
            params.append(f"%{category}%")
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def all():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def add(name, category, quantity, status="available"):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory (name,category,quantity,status) VALUES (?,?,?,?)",
                    (name, category, quantity, status))
        conn.commit()
        conn.close()

    @staticmethod
    def update(inv_id, name=None, category=None, quantity=None, status=None):
        conn = get_db()
        cur = conn.cursor()
        fields, params = [], []
        if name is not None:
            fields.append("name=?"); params.append(name)
        if category is not None:
            fields.append("category=?"); params.append(category)
        if quantity is not None:
            fields.append("quantity=?"); params.append(quantity)
        if status is not None:
            fields.append("status=?"); params.append(status)
        if fields:
            params.append(inv_id)
            cur.execute(f"UPDATE inventory SET {', '.join(fields)} WHERE id=?", params)
            conn.commit()
        conn.close()

    @staticmethod
    def delete(inv_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM inventory WHERE id=?", (inv_id,))
        conn.commit()
        conn.close()
