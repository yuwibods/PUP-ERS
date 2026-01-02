reservations = []

def reserve_item(user, item_name):
    reservations.append({
        "user": user,
        "item": item_name,
        "status": "reserved"
    })

def cancel_reservation(user, item_name):
    for r in reservations:
        if r["user"] == user and r["item"] == item_name:
            r["status"] = "cancelled"
            return

def view_reservations():
    return reservations
