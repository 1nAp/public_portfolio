import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


#Sets up the Flight Search

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notifications = NotificationManager()
user_data = data_manager.get_customer_emails()
# Sets your origin airport
ORIGIN_CITY_IATA = "LON"


#Updates the Airport Codes in Google Sheet
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

#Searches for flights between tomorrow and 6 months from today using the flightSearch function check_flights().
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: €{cheapest_flight.price}")
    if cheapest_flight.price == "N/A":
        print(f"No direct flights for {destination['city']}. Getting indirect flights...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}. ")
    #Sends a text message with the indicated data if the price of the cheapest flight is lower than the max price
    #indicated in the Google Sheet ("Lowest Price" meaning the price the deal has to beat to be relevant.)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        notifications.send_message(
            cheapest_flight.price,
            cheapest_flight.origin_airport,
            cheapest_flight.destination_airport,
            cheapest_flight.out_date,
            cheapest_flight.return_date
        )
    #Generates a message body for an email depending on whether there are stopovers or not.
    if cheapest_flight.stops == 0:
        message_body = f"""Low price alert! Only EUR {cheapest_flight.price} to fly direct
                       from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport},
                       on {cheapest_flight.out_date} until {cheapest_flight.return_date}."""
    else:
        message_body = f"""Low price alert! Only EUR {cheapest_flight.price} to fly
                  from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport},
                  with {cheapest_flight.stops} stop(s)
                  departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."""
    #Sends an email with the indicated data if the price of the cheapest flight is lower than the max price
    #indicated in the Google Sheet ("Lowest Price" meaning the price the deal has to beat to be relevant.)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        for address in user_data:
            notifications.send_emails(address, message_body)

    #Slowing down requests to avoid rate limit on Amadeus and Sheety.
    time.sleep(2)