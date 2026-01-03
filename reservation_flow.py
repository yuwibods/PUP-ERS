# RESERVATION FLOW SYSTEM

# === DATA STORAGE ===
items = {"Projector": 2}
reservations = []

# === FUNCTION 1: SHOW ITEMS ===  this will show the available items
def show_items():
    print("\n AVAILABLE ITEMS ")
    for item, qty in items.items():
        print(f"• {item}: {qty} available")

# === FUNCTION 2: MAKE RESERVATION === this will make your reservation
def make_reservation():
    print("\n MAKE RESERVATION ")
    
    name = input("Your name: ")
    item = input("Item (Projector): ")
    qty = int(input("How many? "))
    
    if item not in items:
        print("item doesn't exist!")
    elif qty > items[item]:
        print(f"Only {items[item]} available!")
    else:
        items[item] -= qty
        reservations.append({"name": name, "item": item, "qty": qty})
        print(f"✅ Reserved {qty} {item}(s)!")

# === FUNCTION 3: VIEW RESERVATIONS === you can confirm if you have reservation here
def view_reservations():
    print("\n--- MY RESERVATIONS ---")
    name = input("Your name: ")
    
    found = False
    for r in reservations:
        if r["name"] == name:
            print(f"• {r['item']} x{r['qty']}")
            found = True
    
    if not found:
        print("No reservations found")

# === FUNCTION 4: CANCEL RESERVATION === you can cancel reservation here
def cancel_reservation():
    print("\n--- CANCEL RESERVATION ---")
    name = input("Your name: ")
    item = input("Item to cancel: ")
    
    for r in reservations:
        if r["name"] == name and r["item"] == item:
            items[item] += r["qty"]
            reservations.remove(r)
            print(f"Cancelled {r['qty']} {item}(s)")
            return
    
    print("Reservation not found")

# === MAIN MENU ===1-5
def main():
    print("   RESERVATION SYSTEM")
    
    while True:
        print("\nMENU:")
        print("1. See available items")
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
            print("\nThank you! Goodbye!")
            break
        else:
            print("Please enter 1-5 only!")

main()
