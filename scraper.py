import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import random
import threading
import urllib.parse
import logging

# Proxy settings (replace these with your actual proxy credentials)
PROXY_USER = 'your-username'
PROXY_PASS = 'your-password'
PROXY_URL = f"socks5h://{PROXY_USER}:{PROXY_PASS}@your-proxy-url:port"
proxies = {
    'http': PROXY_URL,
    'https': PROXY_URL
}

# Load the xls file
df = pd.read_excel('list_data.xlsx')

# Set up logging
logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR)

# Function to guess emails based on business name
def guess_emails(business_name):
    clean_name = re.sub(r'\W+', '', business_name)
    return f'{clean_name}@gmail.com, info@{clean_name}.com'

# Function to search Google for company info
def google_search(company_name):
    time.sleep(random.uniform(1, 3))
    url = 'https://www.google.com/search'
    try:
        response = requests.get(url, params={'q': company_name}, proxies=proxies)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Problem with request: {str(e)}")
        return None
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('div', class_='kCrYT')
        first_link = None
        for link in links:
            a_tag = link.find('a')
            if a_tag is None:  
                continue
            url = a_tag.get('href')  
            url = re.sub(r"/url\?q=([^&]*)&sa=.*", r"\1", url)
            if any(substring in url.lower() for substring in ["directory", "yelp", "google", "facebook", "linkedin"]):
                continue

            words = [word for word in company_name.split() if len(word) > 5]
            domain = urllib.parse.urlparse(url).netloc

            if any(word.lower() in domain.lower() for word in words):
                return url
            if first_link is None:
                first_link = url
        return first_link if first_link is not None else "No relevant link found"
    except Exception as e:
        logging.error(f"Problem parsing response: {str(e)}")
        return None

# Function to scrape websites for contact info
def scrape_website(url):
    time.sleep(random.uniform(1, 3))
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Problem with request: {str(e)}")
        return None
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        email_matches = re.findall(email_pattern, text)
        phone_matches = re.findall(phone_pattern, text)
        contact_link = None
        for a_tag in soup.find_all('a', href=True):
            if "contact" in a_tag.text.lower():
                contact_link = urllib.parse.urljoin(url, a_tag['href'])
                break
        return email_matches, phone_matches, contact_link
    except Exception as e:
        logging.error(f"Problem parsing response: {str(e)}")
        return None
