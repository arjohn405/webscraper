import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict
import re

def normalize_text(text: str) -> str:
    """Normalize text by removing extra spaces and newlines."""
    return re.sub(r'\s+', ' ', text).strip()

def scrape_devfolio() -> List[Dict]:
    """Scrape hackathon data from Devfolio."""
    url = "https://devfolio.co/hackathons/open"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    hackathons = []
    
    for card in soup.find_all('div', class_="sc-ZyCDH dccYnH CompactHackathonCard__StyledCard-sc-9ff45231-0 fudhHJ"):
        title = normalize_text(card.find('h1', class_='sc-dkzDqf ikqvcK').text) if card.find('h1', class_='sc-dkzDqf ikqvcK') else ""
        description = normalize_text(card.find('div', class_='sc-fmGnzW giVfFV Overview__StyledDescriptionCard-sc-1aead9cd-3 evNsmn').text) if card.find('div', class_='sc-fmGnzW giVfFV Overview__StyledDescriptionCard-sc-1aead9cd-3 evNsmn') else ""
        date = normalize_text(card.find('p', class_='sc-hZgfyJ fsVoAT').text) if card.find('p', class_='sc-hZgfyJ fsVoAT') else ""
        location = normalize_text(card.find('p', class_='sc-hZgfyJ fsVoAT').text) if card.find('p', class_='sc-hZgfyJ fsVoAT') else ""
        link = "https://devfolio.co" + card.find('a')['href'] if card.find('a') else ""
        
        hackathon = {
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "link": link,
            "keywords": ""  # Devfolio doesn't provide keywords directly
        }
        hackathons.append(hackathon)
    
    return hackathons

def scrape_devpost() -> List[Dict]:
    """Scrape hackathon data from Devpost."""
    url = "https://devpost.com/hackathons"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    hackathons = []
    
    for card in soup.find_all('article', class_='flex-row tile-anchor'):
        title = normalize_text(card.find('h1').text) if card.find('h1') else ""
        description = normalize_text(card.find('article', class_='challenge-description').text) if card.find('article', class_='challenge-description') else ""
        date = normalize_text(card.find('div', class_='submission-period').text) if card.find('div', class_='submission-period') else ""
        location = normalize_text(card.find('div', class_='info').text) if card.find('div', class_='info') else ""
        link = card.find('a')['href'] if card.find('a') else ""
        
        # Extract keywords from tags
        keywords = []
        for tag in card.find_all('span', class_='cp-tag'):
            keywords.append(normalize_text(tag.text))
        
        hackathon = {
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "link": link,
            "keywords": ", ".join(keywords)  # Join keywords into a single string
        }
        hackathons.append(hackathon)
    
    return hackathons

def save_to_csv(data: List[Dict], filename: str):
    """Save scraped data to a CSV file."""
    # Define the CSV column headers
    fieldnames = ["title", "description", "date", "location", "link", "keywords"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the data rows
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Scrape data from both websites
    devfolio_data = scrape_devfolio()
    devpost_data = scrape_devpost()
    
    # Combine data
    combined_data = devfolio_data + devpost_data
    
    # Save to CSV file
    save_to_csv(combined_data, "hackathons.csv")
    
    print("Scraping completed. Data saved to hackathons.csv.")