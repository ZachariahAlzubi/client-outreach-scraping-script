# Automated Web Scraping Script with Proxy Integration

## Overview
This project performs automatic web scraping using proxies to gather business information from the web. It uses Google search results to find company URLs and then scrapes these websites for contact information such as emails and phone numbers.

## Features
- Scrapes business names and finds corresponding contact info (emails, phone numbers, etc.).
- Uses a proxy for anonymous web scraping.
- Handles timeouts and logging for errors and issues.
- Saves the scraped data to an Excel file.

## Requirements
- pandas
- requests
- BeautifulSoup (bs4)
- re
- logging
- threading
- xlrd (for reading Excel files)
- openpyxl (for writing Excel files)

## Setup
1. Install the required dependencies:
   ```bash
   pip install pandas requests beautifulsoup4 openpyxl xlrd
Ensure you have a proxy setup, and update the credentials in scraper.py:

PROXY_USER = 'your-username'
PROXY_PASS = 'your-password'
Make sure the file list_data.xlsx is in the same directory as your script, containing business names in the column "Legal Business Name".
Running the Script

Run the main script:
python main.py
The script will prompt you for the number of business names to process. It will then search for each business name, scrape their website for contact information, and save the results to a new Excel file called scraped_data.xlsx.
Logging

The script includes logging for errors and issues that occur during scraping. Check the scraping_errors.log file for any error details.
Notes

For best results, update the list of websites to exclude from scraping based on your specific needs.
Disclaimer

This project is for educational purposes only. Please ensure that your scraping activities comply with the legal guidelines and terms of service of the websites you are scraping.