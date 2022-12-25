from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_web_driver = "C:\Developement\chromedriver.exe"
driver = webdriver.Chrome(service=Service(executable_path=chrome_web_driver))
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.CSS_SELECTOR, "#cookie")
store_elements = driver.find_elements(By.CSS_SELECTOR, "#store div")
five_min = time.time() + 60         # * 5
time_out = time.time() + 5
most_expensive_item_price = 0
item_to_buy = ""

while True:
    cookie.click()

    if time.time() > time_out:
        for div in driver.find_elements(By.CSS_SELECTOR, "#store div"):
            # Check if item is available or not
            if div.get_attribute("class") != "grayed":
                print(f"Div: {div}")
                print(f'Div id: {div.get_attribute("id")}')
                item = div.find_element(By.CSS_SELECTOR, "b")
                # print(item.text)

                # Get only valid list of items in menu
                if len(item.text.split(" - ")) > 1:
                    current_item_price = item.text.split(" - ")[1]
                    if "," in current_item_price:
                        current_item_price = item.text.split(" - ")[1].replace(",", "")

                    # Finding out most expensive available item
                    if int(current_item_price) > most_expensive_item_price:
                        most_expensive_item_price = int(current_item_price)

                        # Checking if we can afford to buy or not
                        current_balance = driver.find_element(By.CSS_SELECTOR, "#money").text
                        if "," in current_balance:
                            current_balance = driver.find_element(By.CSS_SELECTOR, "#money").text.replace(",", "")

                        if int(current_balance) > int(current_item_price):
                            item_to_buy = item
        print(f"Iteration Done for {item_to_buy.text}")
        try:
            item_to_buy.click()
        except StaleElementReferenceException:
            pass

        time_out = time.time() + 5

    # Terminate loop after 5 mins and print final cookie per sec count
    if time.time() > five_min:
        cookie_per_second = driver.find_element(By.CSS_SELECTOR, "#cps").text
        print(cookie_per_second)
        break


print("\nTime Over")
