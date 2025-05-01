import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

#Loads environment variables from .env file
load_dotenv()

class DataManager:

    def __init__(self):
        """Initializes environmental variables for the Sheety API."""
        self.SHEETY_PRICES_ENDPOINT = os.environ['SHEETY_PRICES_ENDPOINT']
        self.SHEETY_USERS_ENDPOINT = os.environ['SHEETY_USERS_ENDPOINT']
        self.HEADERS_SHEETY = {
            'Authorization': f"Bearer {os.environ['TOKEN_SHEETY']}"
        }
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = []


    def get_destination_data(self):
        """Uses the Sheety API to GET all the data in the Google Sheets "prices" tab and print it out."""
        response = requests.get(url=self.SHEETY_PRICES_ENDPOINT, headers=self.HEADERS_SHEETY)
        data = response.json()
        print(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """Makes a PUT request and uses the row id from sheet_data to update the Google Sheet with the IATA codes."""
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data, headers=self.HEADERS_SHEETY
            )
            print(response.text)

    def get_customer_emails(self):
        """Uses the Sheety API to GET all the data in the Google Sheets "users" tab and print it out.
        This data is generated through a Google Form where users submit names and emails."""
        response = requests.get(url=self.SHEETY_USERS_ENDPOINT, headers=self.HEADERS_SHEETY)
        data = response.json()
        print(data)
        for index in range(len(data['users'])):
            self.customer_data.append(data['users'][index]['whatIsYourEmail?'])
        print(self.customer_data)
        return self.customer_data
