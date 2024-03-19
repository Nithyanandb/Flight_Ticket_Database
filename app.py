import mysql.connector
from tabulate import tabulate
conn = mysql.connector.connect(host="localhost", user="root", password="21ap21pu", database="flight_ticket_database")
c = conn.cursor()



print("Please enter information about the user:")
name = input("Name: ")
email = input("Email: ")


c.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))


print("Please enter information about the flight you would like to book:")
origin = input("Origin: ")
destination = input("Destination: ")
price = input("Price: ")


c.execute("INSERT INTO users (flight_origin, flight_destination, flight_price) VALUES (%s, %s, %s)", (origin, destination, price))


c.execute("UPDATE users SET flight_origin = %s, flight_destination = %s, flight_price = %s WHERE email = %s", (origin, destination, price, email))


cancel_flight = input("Would you like to cancel your flight? (y/n): ")
if cancel_flight.lower() == 'y':
    c.execute("DELETE FROM users WHERE email = %s", (email,))
    print("Flight cancelled.")
else:
    print("Flight booked.")

display_data = input("Would you like to display your ticket? (y/n): ")
if display_data.lower() == 'y':
    display = "select * from users"
    c.execute(display)
    show = c.fetchall()
    print(tabulate(show, headers=["name", "email", "flight_origin", "flight_destination", "flight_price"]))


conn.commit()
conn.close()
