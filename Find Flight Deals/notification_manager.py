from twilio.rest import Client
import requests
import os
import smtplib

class NotificationManager:
    """This class is responsible for sendings notifications with the flight deal details. Initializes various environmental variables so that emails and text messages may be sent."""
    def __init__(self):
        self._sid = os.environ["TWILIO_SID"]
        self._auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.email_address = os.environ['EMAIL']
        self.email_password = os.environ['EMAIL_PASSWORD']
        self.smtp = os.environ['SMTP_ADDRESS']




    def send_message(self, price, departure, destination, departure_date, return_date):
        """Sends a text message to the indicated phone number using a TWILIO number."""
        client = Client(self._sid, self._auth_token)
        #Change the "from_" and "to" phone numbers to the number you'd like to send the message from,
        #and the number you'd like to receive the message with.
        message = client.messages.create(
            body=f"Low price alert! Only £{price} to fly from {departure} to {destination}, on {departure_date} until {return_date}",
            from_="+1717171717",
            to="+4512345678",
        )

        print(message.status)

    def send_emails(self, recipient_email, message_body):
        """Sends an email to the recipient_email indicated in the Google Sheet."""
        with smtplib.SMTP(self.smtp) as connection:
            connection.starttls()
            connection.login(user=self.email_address,
                             password=self.email_password)
            connection.sendmail(from_addr=self.email_address,
                                to_addrs=f"{recipient_email}",
                                msg=f"Subject: Cheap flight deals!\n\n{message_body}")
            print(f"Email sent to {recipient_email}")