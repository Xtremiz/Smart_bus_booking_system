SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad", "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur", "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas", "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore", "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad", "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30}
]

bookings = []
issued_booking_ids = set()
next_booking_number = 1001


def find_route(route_id):
    for route in routes:
        if route["route_id"] == route_id.strip().upper():
            return route
    return None


def find_booking(booking_id):
    for booking in bookings:
        if booking["booking_id"] == booking_id.strip().upper():
            return booking
    return None


def read_positive_integer(prompt):
    try:
        number = int(input(prompt).strip())
        if number > 0:
            return number
    except ValueError:
        pass

    print("Enter a valid positive whole number.")
    return None


def print_route(route, number=None):
    prefix = "{}. ".format(number) if number is not None else ""
    status = "Fully Booked" if route["available_seats"] == 0 else "Seats Available"

    print("{}{} | {} -> {} | {} | Rs. {} | Seats {}/{} | {}".format(
        prefix, route["route_id"], route["departure_city"],
        route["destination_city"], route["departure_time"],
        route["ticket_price"], route["available_seats"],
        route["total_seats"], status
    ))


def display_routes(routes):
 
    print("AVAILABLE BUS ROUTES")

    print(
        "{:<5} {:<6} {:<18} {:<18} {:<11} {:>9} {:>10}".format(
            "No.", "ID", "From", "To", "Departure", "Fare", "Seats"
        )
    )
   

    shown = 0
    for index, route in enumerate(routes, start=1):
        if  route["available_seats"] == 0:
            continue

        status = "FULL" if route["available_seats"] == 0 else "Available"
        seat_text = "{}/{}".format(
            route["available_seats"], route["total_seats"]
        )
        print(
            "{:<5} {:<6} {:<18} {:<18} {:<11} Rs.{:>6} {:>10}".format(
                index,
                route["route_id"],
                route["departure_city"],
                route["destination_city"],
                route["departure_time"],
                route["ticket_price"],
                seat_text,
            )
        )
        if status == "FULL":
            print("      Status: Fully booked")
        shown += 1

    if shown == 0:
        print("No routes match this filter.")

def search_route():
    term = input("Enter route ID or city: ").strip().lower()

    if not term:
        print("Search cannot be empty.")
        return

    found = False

    for route in routes:
        if term == route["route_id"].lower():
            print_route(route)
            found = True
            break

        if (term in route["departure_city"].lower()
                or term in route["destination_city"].lower()):
            print_route(route)
            found = True
    else:
        if not found:
            print("No matching route found.")


def create_booking_id():
    global next_booking_number

    while True:
        booking_id = "B{}".format(next_booking_number)
        next_booking_number += 1

        if booking_id not in issued_booking_ids:
            issued_booking_ids.add(booking_id)
            return booking_id


def book_ticket():
    name = input("Passenger name: ").strip()

    if not name:
        print("Passenger name cannot be empty.")
        return

    age = read_positive_integer("Passenger age: ")
    if age is None:
        return

    route = find_route(input("Route ID: "))
    if route is None:
        print("Route not found.")
        return

    seats = read_positive_integer("Number of seats: ")
    if seats is None:
        return

    if seats > route["available_seats"]:
        print("Not enough seats. Available: {}".format(
            route["available_seats"]))
        return

    booking_id = create_booking_id()
    total_fare = route["ticket_price"] * seats

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }

    bookings.append(booking)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID:", booking_id)
    print("Passenger:", name)
    print("Seats:", seats)
    print("Total fare: Rs.", total_fare)


def view_bookings():
    if not bookings:
        print("No bookings found.")
        return

    for number, booking in enumerate(bookings, 1):
        route = find_route(booking["route_id"])

        print("{}. {} | {} | {} -> {} | Seats: {} | Fare: Rs. {} | {}".format(
            number, booking["booking_id"],
            booking["passenger_name"], route["departure_city"],
            route["destination_city"], booking["seats"],
            booking["total_fare"], booking["status"]
        ))


def cancel_booking():
    booking_id = input("Booking ID to cancel: ").strip().upper()
    booking = find_booking(booking_id)

    if booking is None:
        print("Booking ID not found.")
        return

    if booking["status"] != "Confirmed":
        print("Booking is already cancelled.")
        return

    route = find_route(booking["route_id"])

    if route is None:
        print("Route not found.")
        return

    if route["available_seats"] + booking["seats"] > route["total_seats"]:
        print("Seat data is inconsistent. Cancellation stopped.")
        return

    route["available_seats"] += booking["seats"]
    booking["status"] = "Cancelled"

    print("Booking cancelled:", booking_id)
    print("Seats restored:", booking["seats"])


def view_seat_availability():
    choice = input("Show (1) all routes or (2) available routes? ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice.")
        return

    shown = False

    for route in routes:
        available = route["available_seats"]
        total = route["total_seats"]

        if choice == "2" and available == 0:
            continue

        if available == total:
            status = "All seats available"
        elif available == 0:
            status = "Fully Booked"
        else:
            status = "Partially Booked"

        print("{} | Seats {}/{} | {}".format(
            route["route_id"], available, total, status))
        shown = True

    if not shown:
        print("No routes have seats available.")


def generate_booking_report():
    confirmed = [b for b in bookings if b["status"] == "Confirmed"]
    cancelled = [b for b in bookings if b["status"] == "Cancelled"]

    reserved_seats = 0
    revenue = 0

    for route in routes:
        for booking in confirmed:
            if booking["route_id"] == route["route_id"]:
                reserved_seats += booking["seats"]
                revenue += booking["total_fare"]

    full_routes = sum(
        1 for route in routes if route["available_seats"] == 0
    )

    print("\nBOOKING REPORT")
    print("Total bookings:", len(bookings))
    print("Confirmed bookings:", len(confirmed))
    print("Cancelled bookings:", len(cancelled))
    print("Reserved seats:", reserved_seats)
    print("Confirmed revenue: Rs.", revenue)
    print("Fully booked routes:", full_routes)


def show_route_schedule():
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")

    for city in SUPPORTED_CITIES:
        print("\n" + city)
        found = False

        for route in routes:
            if route["departure_city"] == city:
                print("{} -> {} | {}".format(
                    route["route_id"],
                    route["destination_city"],
                    route["departure_time"]
                ))
                found = True

        if not found:
            print("No scheduled departures.")


def main():
    while True:
        print(
            "\nSMART BUS RESERVATION SYSTEM\n"
            "1. View Available Routes\n"
            "2. Search for a Route\n"
            "3. Book a Ticket\n"
            "4. View My Bookings\n"
            "5. Cancel a Booking\n"
            "6. View Seat Availability\n"
            "7. Reports / Route Schedule\n"
            "8. Exit"
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_routes(routes)
        elif choice == "2":
            search_route()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            view_seat_availability()
        elif choice == "7":
            print("1. Generate Booking Report\n2. View Route Schedule")
            subchoice = input("Choose an option: ").strip()

            if subchoice == "1":
                generate_booking_report()
            elif subchoice == "2":
                show_route_schedule()
            else:
                print("Invalid choice. Enter 1 or 2.")

        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 8.")
            continue

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()