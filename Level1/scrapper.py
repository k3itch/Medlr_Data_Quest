#scrapper.py

#Level 1: Pharmacy Exploration
#Mission: Scrape all medicines (Name, MRP, Discounted Price, Quantity, Salts, Manufacturer, and URL) 
#starting from both 'B' and 'F' on Pharmeasy and Netmeds  into a CSV/XLSX 
#(You can select any 1000 data rows for each alphabet and any 4 columns).


import time
import requests
from bs4 import BeautifulSoup
import csv
import sys

# Function for scraping PharmEasy data
def scrape_pharmeasy_data(url):
    try:
        page = requests.get(url)
        page.raise_for_status()  # Raises an exception for 4XX/5XX status codes
    except requests.exceptions.RequestException as e:
        print('Error accessing the URL:', url)
        print(e)
        return None

    time.sleep(2)

    soup = BeautifulSoup(page.content, 'html.parser')

    name = ''
    mrp = ''
    marketer = ''
    salts = ''
    discounted_price = ''

    try:
        name = soup.find('div', {'class': 'MedicineOverviewSection_nameContainer__du_iv'}).text.strip()
    except AttributeError:
        pass

    try:
        mrp_element = soup.find('span', {'class': 'PriceInfo_striked__Hk2U_'})
        mrp = mrp_element.text.strip() if mrp_element else 'N/A'
    except AttributeError:
        pass

    try:
        marketer = soup.find('div', {'class': 'MedicineOverviewSection_brandName__rJFzE'}).text.strip()
    except AttributeError:
        pass

    table = soup.find('table', {'class': 'DescriptionTable_seoTable__wKp77'})
    if table:
        rows = table.find_all('tr')
        for row in rows:
            if row.find('td', {'class': 'DescriptionTable_field__l5jJ3'}).text.strip() == 'Offer Price':
                try:
                    discounted_price = row.find('td', {'class': 'DescriptionTable_value__0GUMC'}).text.strip()
                except AttributeError:
                    pass
            elif row.find('td', {'class': 'DescriptionTable_field__l5jJ3'}).text.strip() == 'Contains':
                try:
                    salts = row.find('td', {'class': 'DescriptionTable_value__0GUMC'}).text.strip()
                    break
                except AttributeError:
                    pass

    return [name, mrp, discounted_price, marketer, salts, url]


url_list_pharmeasy = [
    'https://pharmeasy.in/online-medicine-order/browse?alphabet=b',
    'https://pharmeasy.in/online-medicine-order/browse?alphabet=f'
]

url_list_netmeds = [
    'https://www.netmeds.com/prescriptions/bacterial-infections',
    'https://www.netmeds.com/prescriptions/bactomin-375mg-tablet-10-s'
    # Add more Netmeds URLs if needed
]

data = []

# Scraping PharmEasy data
for url in url_list_pharmeasy:
    try:
        page = requests.get(url)
        page.raise_for_status()  # Raises an exception for 4XX/5XX status codes
    except requests.exceptions.RequestException as e:
        print('Error accessing the URL:', url)
        print(e)
        continue

    time.sleep(2)

    soup = BeautifulSoup(page.content, 'html.parser')

    medicine_links = soup.find_all('a', class_='BrowseList_medicine__cQZkc')
    urls = []

    for link in medicine_links:
        href = link.get('href')
        if href.startswith('/online-medicine-order/'):
            full_url = f'https://pharmeasy.in{href}'
            urls.append(full_url)

    for link_url in urls:
        pharmeasy_data = scrape_pharmeasy_data(link_url)
        if pharmeasy_data:
            data.append(pharmeasy_data)

# Scraping Netmeds data
for url in url_list_netmeds:
    netmeds_data = scrape_netmeds_data(url)
    if netmeds_data:
        data.append(netmeds_data)

# Writing scraped data to CSV file

column_names = ["Name", "MRP", "Discounted Price", "Marketer", "Salts", "URL"]

with open('output2.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the column names
    writer.writerow(column_names)

    # Write the data
    for row in data:
        writer.writerow(row)
