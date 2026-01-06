# RESERVATION FLOW SYSTEM

# === IMPORT ===
from datetime import datetime

# === DATA STORAGE === This will show how many quantity of the items
items = {
    "projector": 2,
    "speaker portable": 2,
    "speaker big": 2,
    "mic with wire": 2,
    "mic wireless": 2,
    "whitescreen": 2
}
reservations = []


# === FUNCTION 1: SHOW ITEMS === This will show the storage
def show_items():
    for item, qty in items.items():
        print(f"• {item}: {qty} available")


# === FUNCTION 2: MAKE RESERVATION === This will make your reservation
def make_reservation():
    print("\nMAKE RESERVATION")

    name = input("Your name: ")
    item = input("Item (projector, Speaker portable, Speaker big, Mic with wire, Mic wireless, Whitescreen): ").lower()
    qty = int(input("How many? "))

    # Ask for date
    date_str = input("What date? (MM/DD/YYYY): ")

    # Ask for time slot
    print("\nEnter time in AM/PM format (e.g., 8:30 AM, 2:00 PM)")
    start_time = input("Start time: ")
    end_time = input("End time: ")

    # Check availability
    if item not in items:
        print("Item doesn't exist!")
    elif qty > items[item]:
        print(f"Only {items[item]} available!")
    else:
        # Store reservation
        reservation = {
            "name": name,
            "item": item,
            "qty": qty,
            "date": date_str,
            "start_time": start_time.upper(),
            "end_time": end_time.upper()
        }

        items[item] -= qty
        reservations.append(reservation)

        print(f"\n✅ Reservation confirmed!")
        print(f"Name: {name}")
        print(f"Item: {item} x{qty}")
        print(f"Date: {date_str}")
        print(f"Time: {start_time.upper()} to {end_time.upper()}")


# === FUNCTION 3: VIEW RESERVATIONS ===
def view_reservations():
    print("\nVIEW RESERVATIONS")
    name = input("Your name: ")

    found = False
    for r in reservations:
        if r["name"] == name:
            print(f"• {r['item']} x{r['qty']}")
            print(f"  Date: {r['date']}")
            print(f"  Time: {r['start_time']} to {r['end_time']}")
            found = True

    if not found:
        print("No reservations found")


# === FUNCTION 4: CANCEL RESERVATION ===
def cancel_reservation():
    print("\nCANCEL RESERVATION")
    name = input("Your name: ")
    item = input("Item to cancel: ")

    for r in reservations:
        if r["name"] == name and r["item"] == item:
            items[item] += r["qty"]
            reservations.remove(r)
            print(f"Cancelled {r['qty']} {item}(s)")
            print(f"Was reserved for: {r['date']} at {r['start_time']}-{r['end_time']}")
            return

    print("Reservation not found")


# === MAIN MENU ===
def main():
    print("RESERVATION SYSTEM")

    while True:
        print("\nMENU:")
        print("1. Available items")
        print("2. Make reservation")
        print("3. View my reservations")
        print("4. Cancel reservation")
        print("5. Exit")

        choice = input("\nChoose (1-5): ")

        if choice == "1":
            show_items()
        elif choice == "2":
            make_reservation()
        elif choice == "3":
            view_reservations()
        elif choice == "4":
            cancel_reservation()
        elif choice == "5":
            print("Byee")
            break
        else:
            print("Please enter 1-5 only!")


main()
