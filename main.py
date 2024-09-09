from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the login page
driver.get("https://www.meindate.de/profiles")

# Allow the page to load
time.sleep(4)  # Adjust sleep time as needed

# Find the username and password fields and enter your credentials
username_field = driver.find_element(By.XPATH, "//*[@id='username_login']")  # Adjust the selector as needed
password_field = driver.find_element(By.XPATH, "//*[@id='password_login']")  # Adjust the selector as needed

username_field.send_keys("<login-credentials-email>")
password_field.send_keys("<login-credentials-password>")

# Submit the login form
login_button = driver.find_element(By.XPATH, "/html/body/nav/div/form/div/div/div[3]/button")  # Adjust the XPath as needed
login_button.click();

# Allow the page to load
time.sleep(2)  # Adjust sleep time as

# Loop to scroll and collect profile data with pagination
profiles = driver.find_elements(By.CSS_SELECTOR, ".search-user-link")  # Replace with appropriate selector
data = []
page_count = 1

while True:  # Loop until there are no more pages
    for profile in profiles:
        username_element = profile.find_element(By.CSS_SELECTOR, ".search-user-name")  # Replace with username selector
        location_element = profile.find_element(By.CSS_SELECTOR, ".search-user-postal-code")  # Replace with location selector
        image_element = profile.find_element(By.CSS_SELECTOR, ".search-user-image")  # Replace with location selector
        username = username_element.text.split("(")[0].strip()
        location = location_element.text
        image = image_element.get_attribute("src")
        age = username_element.text.split("(")[1].replace(")", "")
        
        data.append({"username": username, "location": location, "age": age, "image": image})

    # Click next page button and handle exceptions for termination
    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, ".pagination .page-link[rel='next']")
        next_page_button.click()
        time.sleep(2)  # Adjust wait time for page to load
        profiles = driver.find_elements(By.CSS_SELECTOR, ".search-user-link")  # Update selector if needed for subsequent pages
        page_count += 1
        if page_count > 5:
            break

    except:
        print("Reached the last page")
        break

# Print the collected data
print(data)

#convert the data to a csv file
with open('profiles.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["username", "location", "age", "image"])
    writer.writeheader()
    writer.writerows(data)
    


# Allow some time to observe the result
time.sleep(20)

# Optionally, close the browser
driver.quit()
