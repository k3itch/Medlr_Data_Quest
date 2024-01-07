#lab_scrapper.py

#problem:
#Level 3: Lab uncle Odyssey
#Mission: Dive into the data realms of 'Labuncle'. 
#Your task is to scrape all available data and consolidate it into an organised CSV/XLSX file.
#(Select any 40 lab’s data you want to scrape).


import traceback
from bs4 import BeautifulSoup
import requests
import csv
import time

def lab_scraper(url):
    try:
        page = requests.get(url)
        time.sleep(2)
        soup = BeautifulSoup(page.text, 'html.parser')

        lab_name = soup.find('h3', {'class': 'common_main'}).contents[0].strip()
        
        price_section = soup.find('div', {'class': 'org_price'})
        mrp = price_section.find('h5', {'class': 'crossedd'}).text.strip()
        discounted_price = price_section.find('h5', {'class': 'new_price'}).text.strip()

        tests_included = []
        test_section = soup.find('div', {'id': 'accordion'})
        test_cards = test_section.find_all('div', {'class': 'card'})
        for card in test_cards:
            test_name = card.find('div', {'class': 'card-body'}).text.strip()
            tests_included.append(test_name)

        return lab_name, mrp, discounted_price, tests_included

    except Exception as e:
        error_type, error_info, error_obj = sys.exc_info()
        print('ERROR FOR LINK', url, '\n')
        print(error_type, ' Line: ', traceback.extract_tb(error_info)[-1].lineno)
        return None

urls = ['https://www.labuncle.com/packages/good-health-package-1433',
        'https://www.labuncle.com/packages/health-champion-radiology-package-1677',
        'https://www.labuncle.com/packages/basic-whole-body-health-checkup-package-1543',
        'https://www.labuncle.com/packages/good-health-package-with-vitamins-1434',
        'https://www.labuncle.com/packages/full-body-health-checkup-package-1656',
        'https://www.labuncle.com/packages/whole-body-health-checkup-package-1657',
        'https://www.labuncle.com/packages/whole-body-radiology-package-1678',
        'https://www.labuncle.com/packages/comprehensive-full-body-radiology-package-1679']

all_data = []

for url in urls:
    output = lab_scraper(url)
    if output:
        all_data.append(output)

# Open the file in write mode
with open('lab_scraper.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the column names
    writer.writerow(["lab_name", "mrp", "discounted_price", "tests_included"])
    
    # Write the data
    for data in all_data:
        writer.writerow([
            data[0],
            data[1],
            data[2],
            ', '.join(data[3])  # Joining the list of tests as a string
        ])
