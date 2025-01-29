from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

def scrape_drugbank(drug_id):
    base_url = "https://go.drugbank.com/drugs/"
    query_url = base_url + f"{drug_id}"
    
    # Configure Chrome options
    options = Options()
    options.add_argument('--disable-gpu')           # Disable GPU usage
    options.add_argument('--no-sandbox')           # Disable sandbox for security
    options.add_argument('--headless')             # Run Chrome in headless mode
    options.add_argument('--disable-dev-shm-usage')# Overcome limited resources in containerized environments
    options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation detection
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36') # Mimic a real browser user agent

    # Initialize the driver
    service = Service(ChromeDriverManager().install())  # Use webdriver_manager for automatic driver setup
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(query_url)
    driver.implicitly_wait(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name = soup.find('h1', class_='align-self-center mr-4')
    desc = soup.find('dd', class_='description')
    us_approved = soup.find('span', class_='badge badge-yes badge-pill')

    # print(name.text, desc.text, us_approved.text)
    driver.quit()

    name_text = name.text if name else "No name available"
    desc_text = desc.text if desc else "No description available"
    us_approved_text = us_approved.text if us_approved else "Not approved"

    return name_text, desc_text, us_approved_text
    
scrape_drugbank("DB00001")