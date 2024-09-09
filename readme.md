

# Selenium Web Scraping Script - Python

This script automates the process of logging into a website, scraping profile data, and saving the data to a CSV file using Selenium WebDriver.

#### Prerequisites

- Python 3.x
- Selenium library
- WebDriver Manager for Chrome
- Google Chrome browser

#### Installation
1. Install the required Python packages:
    ```sh
    pip install selenium webdriver-manager
    ```

#### Script Overview

1. **Import Libraries**
    ```python
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import csv
    ```

2. **Initialize WebDriver**
    ```python
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    ```

3. **Open the Login Page**
    ```python
    driver.get("https://www.meindate.de/profiles")
    time.sleep(4)  # Allow the page to load
    ```

4. **Login to the Website**
    ```python
    username_field = driver.find_element(By.XPATH, "//*[@id='username_login']")
    password_field = driver.find_element(By.XPATH, "//*[@id='password_login']")
    username_field.send_keys("<login-credentials-email>")
    password_field.send_keys("<login-credentials-password>")
    login_button = driver.find_element(By.XPATH, "/html/body/nav/div/form/div/div/div[3]/button")
    login_button.click()
    time.sleep(2)  # Allow the page to load
    ```

5. **Scrape Profile Data**
    ```python
    profiles = driver.find_elements(By.CSS_SELECTOR, ".search-user-link")
    data = []
    page_count = 1

    while True:
        for profile in profiles:
            username_element = profile.find_element(By.CSS_SELECTOR, ".search-user-name")
            location_element = profile.find_element(By.CSS_SELECTOR, ".search-user-postal-code")
            image_element = profile.find_element(By.CSS_SELECTOR, ".search-user-image")
            username = username_element.text.split("(")[0].strip()
            location = location_element.text
            image = image_element.get_attribute("src")
            age = username_element.text.split("(")[1].replace(")", "")
            
            data.append({"username": username, "location": location, "age": age, "image": image})

        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, ".pagination .page-link[rel='next']")
            next_page_button.click()
            time.sleep(2)  # Allow the page to load
            profiles = driver.find_elements(By.CSS_SELECTOR, ".search-user-link")
            page_count += 1
            if page_count > 5:
                break
        except:
            print("Reached the last page")
            break
    ```

6. **Save Data to CSV**
    ```python
    with open('profiles.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "location", "age", "image"])
        writer.writeheader()
        writer.writerows(data)
    ```

7. **Close the Browser**
    ```python
    time.sleep(20)  # Allow some time to observe the result
    driver.quit()
    ```

#### Notes
- Adjust the sleep times (`time.sleep()`) as needed to ensure the page loads completely.
- Update the XPath and CSS selectors based on the actual structure of the target website.
- Replace `<login-credentials-email>` and `<login-credentials-password>` with actual login credentials.
- The script currently limits the scraping to 5 pages. Adjust `page_count` logic as needed.