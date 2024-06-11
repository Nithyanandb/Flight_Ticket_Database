from pymongo import MongoClient
from tabulate import tabulate


client = MongoClient('localhost', 27017)
db = client.flight_ticket_database
flights_collection = db.flights
users_collection = db.users

def display_available_flights():
    available_flights = list(flights_collection.find({}, {"_id": 0, "flight_number": 1, "origin": 1, "destination": 1, "price": 1, "available_seats": 1}))
    if available_flights:
        print(tabulate(available_flights, headers="keys"))
    else:
        print("No available flights.")

print("Please enter information about the user:")
name = input("Name: ")
email = input("Email: ")

users_collection.insert_one({"name": name, "email": email})

print("Available flights:")
display_available_flights()


flight_number = input("Please enter the flight number you would like to book: ")


selected_flight = flights_collection.find_one({"flight_number": flight_number})

if selected_flight and selected_flight["available_seats"] > 0:
  
    users_collection.update_one(
        {"email": email},
        {"$set": {
            "flight_number": flight_number,
            "flight_origin": selected_flight["origin"],
            "flight_destination": selected_flight["destination"],
            "flight_price": selected_flight["price"]
        }}
    )

    flights_collection.update_one(
        {"flight_number": flight_number},
        {"$inc": {"available_seats": -1}}
    )
    print("Flight booked.")
else:
    print("Flight not available or no seats left.")


cancel_flight = input("Would you like to cancel your flight? (yes/no): ").lower()
if cancel_flight == 'yes':
    user_info = users_collection.find_one({"email": email})
    if user_info and "flight_number" in user_info:
        flight_number = user_info["flight_number"]
        flights_collection.update_one(
            {"flight_number": flight_number},
            {"$inc": {"available_seats": 1}}
        )
        users_collection.delete_one({"email": email})
        print("Flight cancelled.")
    else:
        print("No flight booking found for the user.")
else:
    print("Flight booking retained.")


display_data = input("Would you like to display your ticket? (y/n): ").lower()
if display_data == 'y':
    user_ticket = users_collection.find_one({"email": email})
    if user_ticket:
        ticket_info = [
            [
                user_ticket.get("_id"),
                user_ticket.get("name"),
                user_ticket.get("email"),
                user_ticket.get("flight_origin"),
                user_ticket.get("flight_destination"),
                user_ticket.get("flight_price")
            ]
        ]
        print(tabulate(ticket_info, headers=["_id", "name", "email", "flight_origin", "flight_destination", "flight_price"]))
    else:
        print("No ticket found for this user.")


client.close()
