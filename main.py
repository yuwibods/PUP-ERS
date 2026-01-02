from reservation.reservation import reserve_item, cancel_reservation, view_reservations

reserve_item("Mica", "Laptop")
reserve_item("Lyndon", "Projector")

cancel_reservation("Mica", "Laptop")

print(view_reservations())
