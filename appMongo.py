from pymongo import MongoClient
from tabulate import tabulate


client = MongoClient('localhost', 27017)
db = client.flight_ticket_database
users_collection = db.users

print("Please enter information about the user:")
name = input("Name: ")
email = input("Email: ")


users_collection.insert_one({"name": name, "email": email})

print("Please enter information about the flight you would like to book:")
origin = input("Origin: ")
destination = input("Destination: ")
price = input("Price: ")


users_collection.update_one(
    {"email": email},
    {"$set": {
        "flight_origin": origin,
        "flight_destination": destination,
        "flight_price": price
    }}
)

cancel_flight = input("Would you like to cancel your flight? (y/n): ")
if cancel_flight.lower() == 'y':
    users_collection.delete_one({"email": email})
    print("Flight cancelled.")
else:
    print("Flight booked.")

"""def cancel_flight():
    users_collection.delete_one({"email": email})
    print("Flight cancelled.")

def book_flight():
    print("Flight booked.")

# Switch case equivalent
options = {
    'y': cancel_flight,
    'n': book_flight
}
"""


display_data = input("Would you like to display your ticket? (y/n): ")
if display_data.lower() == 'y':
    show = list(users_collection.find())
    print(tabulate(show, headers=["_id", "name", "email", "flight_origin", "flight_destination", "flight_price"]))

client.close()
