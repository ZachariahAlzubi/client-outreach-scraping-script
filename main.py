import pandas as pd
from scraper import google_search, scrape_website, guess_emails
import time
import random
import logging

# Load dataset
df = pd.read_excel('list_data.xlsx')

# Prompt the user for the number of links to process
num_links = int(input("Enter the number of links to process: "))

# Iterate over the DataFrame
for index, row in df.head(num_links).iterrows():
    start_time = time.time()
    print(f"Processing link {index+1} of {num_links}...")
    
    # Get the Google search result
    link = google_search(row['Legal Business Name'])
    if link is None:
        continue
    print(f"Found link: {link} (Time taken: {time.time() - start_time} seconds)")
    df.loc[index, 'Link'] = link
    
    # Scrape the website for contact information
    start_time = time.time()
    contact_info = scrape_website(link)
    if contact_info is None:
        continue
    print(f"Found contact info: {contact_info} (Time taken: {time.time() - start_time} seconds)")
    
    email_matches = ', '.join(contact_info[0]) if contact_info[0] else guess_emails(row['Legal Business Name'])
    df.loc[index, 'Emails'] = email_matches
    df.loc[index, 'Phone Numbers'] = ', '.join(contact_info[1]) if contact_info[1] else ''
    df.loc[index, 'Contact Form Link'] = contact_info[2] if contact_info[2] else ''
    time.sleep(random.uniform(1, 3))

# Save the updated DataFrame back to an Excel file
df.to_excel('scraped_data.xlsx', index=False)
print("Scraping complete!")
