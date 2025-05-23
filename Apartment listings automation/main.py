import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#URLs to the static version of Zillow and Google Forms
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORMS_URL = "https://forms.gle/aBKCxDCCVeUbNFEMA"

#Grabs the Zillow html data and converts it to text
response = requests.get(ZILLOW_URL)
zillow_page = response.text

#Makes "soup" with the Zillow page, parsing its data into the library.
soup = BeautifulSoup(zillow_page, 'html.parser')

#Grabs all addresses from the available Zillow listings on the page.
addresses = soup.find_all(name='address')
list_of_addresses = [address.getText().replace('\n', '').replace('|', '').strip() for address in addresses]
print(list_of_addresses)

#Grabs all prices from the available Zillow listings on the page.
rent_amounts = soup.find_all(name='span', class_='PropertyCardWrapper__StyledPriceLine')
list_of_rent_amounts = [amount.getText().split('+')[0].split('/')[0] for amount in rent_amounts]
print(list_of_rent_amounts)

#Grabs all links from the available Zillow listings on the page.
links = soup.find_all(name='a', class_='StyledPropertyCardDataArea-anchor')
list_of_links = [link.get('href') for link in links]
print(list_of_links)

#Sets up Selenium functionality
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Option to keep Chrome open
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

#Gets the Google Forms page.
driver.get(FORMS_URL)

#Enters every entry into three fields inquiring about the address, price and link to the listing in question and submits each listing, logging it as a response.
for index in range(len(list_of_addresses)):
    time.sleep(3)
    q_address = driver.find_element(By.CSS_SELECTOR, value='input[aria-describedby="i2 i3"]')
    q_address.send_keys(list_of_addresses[index])
    q_price = driver.find_element(By.CSS_SELECTOR, value='input[aria-describedby="i7 i8"]')
    q_price.send_keys(list_of_rent_amounts[index])
    q_link = driver.find_element(By.CSS_SELECTOR, value='input[aria-describedby="i12 i13"]')
    q_link.send_keys((list_of_links[index]))
    submit_button = driver.find_element(By.CSS_SELECTOR, value='div[aria-label="Submit"]')
    submit_button.click()
    submit_new_response = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href]'))).send_keys(Keys.ENTER)
