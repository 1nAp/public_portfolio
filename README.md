This program uses the Sheety and Amadeus APIs to find lucrative flight deals going from a pre-disclosed departure city to locations of interest.

The locations and data for sending people notifications is stored within a Google Sheet with a linked Google Form which receives responses to log people's names and email-addresses.

The program also send text-messages to a pre-defined number using TWILIO. I've removed the numbers because the ones used in this case were my own.

None of the code will work as the API data and passwords etc. are all environmental variables. I have not uploaded these, as they belong to my own accounts.

Here's an indication of what my .env file WOULD contain:

TOKEN_SHEETY = The Sheety API token
AMADEUS_API = The Amadeus API token
AMADEUS_SECRET = The Amadeus API secret for authentification
SHEETY_USERNAME = Your Sheety username
SHEETY_PASSWORD = Your Sheety password
TWILIO_SID = Your Twilio SID
TWILIO_AUTH_TOKEN = Your Twilio authentification token
SHEETY_PRICES_ENDPOINT = https://api.sheety.co/uniqueID/flightDeals/prices <-------- "uniqueID" would be replaced by a unique ID based on your own google sheet.
SHEETY_USERS_ENDPOINT = https://api.sheety.co/uniqueID/flightDeals/users <-------- "uniqueID" would be replaced by a unique ID based on your own google sheet.
EMAIL = Your email
EMAIL_PASSWORD = Your email password (not your actual password, the one you would generate to enable externally sending email via your email-address.)
SMTP_ADDRESS = the smtp address for the email server you use. E.g. smtp.gmail.com for gmail.