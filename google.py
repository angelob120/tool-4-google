import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

def scrape_business_info(url):
    # Ensure the URL is complete
    if not url.startswith('http'):
        url = 'https://www.google.com' + url

    # Send a request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract information based on the provided HTML structure
    name = soup.find('div', class_='rgnuSb xYjf2e')
    rating = soup.find('div', class_='rGaJuf')
    reviews = soup.find('div', class_='leIgTe')
    business_type = soup.find('span', class_='hGz87c')
    years_in_business = soup.find('span', class_='FjZRNe hGz87c')
    location = soup.find('span', text=re.compile('Detroit, MI'))  # Adjust the regex based on actual content
    phone = soup.find('span', class_='hGz87c', text=re.compile(r'\(\d{3}\) \d{3}-\d{4}'))
    website_anchor = soup.find('a', text='Website')
    website = website_anchor['href'] if website_anchor else None

    return {
        'Name': name.get_text().strip() if name else 'Not Found',
        'Rating': rating.get_text().strip() if rating else 'Not Found',
        'Reviews': reviews.get_text().strip() if reviews else 'Not Found',
        'Business Type': business_type.get_text().strip() if business_type else 'Not Found',
        'Years in Business': years_in_business.get_text().strip() if years_in_business else 'Not Found',
        'Location': location.get_text().strip() if location else 'Not Found',
        'Phone': phone.get_text().strip() if phone else 'Not Found',
        'Website': website.strip() if website else 'Not Found'
    }

def main():
    urls = []
    while True:
        url = input("Enter a URL to scrape (or type 'done' to finish): ")
        if url.lower() == 'done':
            break
        urls.append(url)

    all_data = [scrape_business_info(url) for url in urls]

    # Generate a timestamp for the file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'business_info_{timestamp}.csv'

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_data)
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

if __name__ == '__main__':
    main()
