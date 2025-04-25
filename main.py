import requests
import json
import os
from bs4 import BeautifulSoup
import html
from datetime import datetime

# ScraperAPI configuration
API_KEY = '53afe5f076bc4ddc0e4443fb61400c6b'
SCRAPER_API_URL = 'https://api.scraperapi.com/'

def convert_txt_to_html():
    """Convert scraped text files to HTML format."""
    txt_files = [f for f in os.listdir('.') if f.startswith('scraped_') and f.endswith('.txt')]
    
    print(f"Found text files: {txt_files}")  # Debug print
    
    for txt_file in txt_files:
        try:
            print(f"Processing {txt_file}...")  # Debug print
            
            # Read the text file
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Escape HTML special characters
            content = html.escape(content)
            
            # Create HTML content with improved styling
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Content - {txt_file}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            overflow-x: auto;
        }}
        .source {{
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
            padding: 10px;
            background: #e9ecef;
            border-radius: 4px;
        }}
        .timestamp {{
            color: #999;
            font-size: 0.9em;
            text-align: right;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Scraped Content</h1>
        <div class="source">Source: {txt_file.replace('scraped_', '').replace('.txt', '')}</div>
        <pre>{content}</pre>
        <div class="timestamp">Generated on: {html.escape(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))}</div>
    </div>
</body>
</html>
"""
            
            # Create HTML filename
            html_file = txt_file.replace('.txt', '.html')
            
            # Save the HTML file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Successfully converted {txt_file} to {html_file}")
            
        except Exception as e:
            print(f"Error converting {txt_file}: {str(e)}")
            import traceback
            print(traceback.format_exc())

def scrape_websites():
    """Scrape data from websites using ScraperAPI."""
    # List of URLs to scrape
    urls = [
        'https://devfolio.co/hackathons/open',
        'https://devpost.com/hackathons'
    ]
    
    for url in urls:
        try:
            # Configure the API request with simplified parameters
            payload = {
                'api_key': API_KEY,
                'url': url,
                'device_type': 'desktop'
            }
            
            # Make the API request
            response = requests.get(SCRAPER_API_URL, params=payload)
            
            if response.status_code == 200:
                print(f"Successfully scraped: {url}")
                # Save the response as text file
                filename = f"scraped_{url.split('//')[1].replace('/', '_')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Data saved to {filename}")
            else:
                print(f"Error scraping {url}: Status code {response.status_code}")
                
        except Exception as e:
            print(f"Error occurred while scraping {url}: {str(e)}")

if __name__ == "__main__":
    print("Starting scraping process...")
    scrape_websites()
    print("Converting text files to HTML...")
    convert_txt_to_html()
    print("Scraping and conversion completed.")