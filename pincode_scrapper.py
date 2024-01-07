#Level 2: Real-Time Medicinal Quest
#Mission: Craft a dynamic script, preferably in Python (but feel free to flex your language of choice!), 
#to scrape real-time data for a specified medicine. User-entered URL and pincode shall unveil the 
#medicine's availability and delivery date (scrape from tata 1mg).(Try to keep the time between the input 
#and output less than 40 sec).

#Input:
#Make an API having two parameters: 
#Url of the medicine
#Pincode entered by the user 

#Output:
#According to the pincode entered by the user you have to check the price and availability of the medicine in that area.


#scrapper_pincode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_medicine_availability(pincode, url):
    driver = webdriver.Chrome()  # Replace with appropriate webdriver
    wait = WebDriverWait(driver, 20)  # Adjust the wait time as needed

    driver.get(url)

    # Find and click on the dropdown menu to open the location modal
    dropdown_menu = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "style__chevron-icon___2Ve1O"))  # Replace with actual dropdown class
    )
    dropdown_menu.click()

    time.sleep(2)

    # Wait for the pincode modal to appear
    pincode_modal = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "styles__popup-content___2gg2z"))  # Replace with actual modal class
    )

    # Find the pincode input field within the modal
    pincode_input = pincode_modal.find_element(By.NAME, "pincode")  # Replace with actual pincode input name if needed
    pincode_input.clear()
    pincode_input.send_keys(pincode)

    # Click on the 'Check' button within the modal
    check_button = pincode_modal.find_element(By.XPATH, "//button[text()='Check']")  # Replace with the button text if needed
    check_button.click()

    time.sleep(2)


    # Wait for the page to reload with the updated pincode
    # Then scrape the delivery date
       # Wait for the delivery date information to appear
    delivery_date_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='style__padded___2vNu9 style__headerText___3sw_C']/span[contains(@style,'color:#00B62F')]"))  # Replace with actual delivery date element locator
    )

    delivery_date = delivery_date_element.text.strip() if delivery_date_element else None

    driver.quit()

    return delivery_date, pincode, url


if __name__ == "__main__":
    pincode = input("Enter pincode: ")
    url = input("Enter URL: ")

    start_time = time.time()
    delivery_date, pincode, url = scrape_medicine_availability(pincode, url)
    end_time = time.time()

    print(f"Delivery Date: {delivery_date}")
    print(f"Pincode: {pincode}")
    print(f"URL: {url}")
    print(f"Time taken: {end_time - start_time} seconds")
