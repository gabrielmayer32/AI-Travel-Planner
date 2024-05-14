import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Selenium with ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)

# URL of the TripAdvisor search results for Mauritius
url = "https://www.tripadvisor.fr/Search?q=Ile+Maurice&geo=1&ssrc=e&searchNearby=false&searchSessionId=000e783c7661d549.ssid&blockRedirect=true&offset=0"

# Navigate to the page
driver.get(url)

# Wait for the dynamic content to load
time.sleep(5)  # Adjust the sleep time based on the network speed and server response time

# Get the page source after JavaScript execution
page_source = driver.page_source

# Use BeautifulSoup to parse the content
soup = BeautifulSoup(page_source, 'html.parser')

# Iterate over possible restaurant data-test attributes like "16_list_item", "17_list_item", etc.
for i in range(1, 21):  # Adjust the range as necessary
    restaurant_data_test = f"{i}_list_item"
    restaurant = soup.find('div', attrs={"data-test": restaurant_data_test})
    if restaurant:
        name_tag = restaurant.find('a', class_="aWhIG _S _Z")
        if name_tag:
            name = name_tag.text.strip()
            # Extract the link to the specific restaurant page
            link = "https://www.tripadvisor.fr" + name_tag.get('href')
            print(f"Fetching details for: {name} from {link}")
            
            # Navigate to the restaurant page to get the location
            driver.get(link)
            time.sleep(3)  # Wait for the content to load
            
            # Parse the new page source
            res_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find the location element and extract text
            location_tag = res_soup.find('div', class_="CsAqy u Ci Ph w")
            if location_tag:
                location = location_tag.find('div', class_="biGQs _P pZUbB hmDzD")
                if location:
                    location = location.text.strip()
                else:
                    location = "Location not found"
            else:
                location = "Location element not found"
            
            print(f"Name: {name}, Location: {location}")
        else:
            print(f"Restaurant name not found in {restaurant_data_test}")
    else:
        print(f"No restaurant found for data-test {restaurant_data_test}")

# Close the browser
driver.quit()
