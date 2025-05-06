import export
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

# URL of random item I want to monitor
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

# Uses the requests module to get a hold of the URL
response = requests.get(
    url=URL,
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
        "Accept-Language":"en-US,en;q=0.9",
    }
)
# Converts the URL to readable html text
amazon_page = response.text

# Setup of environmental values
smtp = os.environ['SMTP_ADDRESS']
email_address = os.environ['EMAIL_ADDRESS']
email_password = os.environ['EMAIL_PASSWORD']
recipient_email = os.environ['EMAIL_ADDRESS']

# Instantiates a BeautifulSoup object using html parsing, so that we may easily use BeautifulSoup to search the page elements.
soup = BeautifulSoup(amazon_page, 'html.parser')

# Gets the title of the product on the url page and replaces unnecessary characters.
title_of_product_raw = soup.find(id="productTitle").getText().replace("\r\n", " ")
title_of_product = title_of_product_raw.replace("  ", "")
print(title_of_product)

# Gets the price of the product on the url page and replaces unnecessary characters.
# Normally you'd leave the currency sign and then remove it from my email message, but I just wanted static currency
# for this project.
raw_price = soup.find(name="span", class_="aok-offscreen")
price = float(raw_price.getText().replace("$", ""))
print(price)

#If the price is below the acceptable threshold for purchase, sends an email from me to myself with the message body.
if price < 100:
    with smtplib.SMTP(smtp) as connection:
        connection.starttls()
        connection.login(user=email_address,
                         password=email_password
        )
        connection.sendmail(from_addr=email_address,
                            to_addrs=recipient_email,
                            msg=f"Subject: Amazon Price Alert!\n\n{title_of_product} is now $ {price}. Buy it here: {URL}".encode()
        )