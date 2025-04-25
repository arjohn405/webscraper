from flask import Flask, render_template, redirect, url_for
import json
import os
from main import scrape_websites as run_scraper

app = Flask(__name__)

def load_scraped_data():
    """Load all scraped JSON files and combine them."""
    all_data = []
    json_files = [f for f in os.listdir('.') if f.startswith('scraped_') and f.endswith('.json')]
    
    print(f"Found JSON files: {json_files}")  # Debug print
    
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Successfully read {file}")  # Debug print
                
                # Extract relevant information from the JSON data
                # This will need to be adjusted based on the actual JSON structure
                hackathon_data = {
                    'title': data.get('title', 'Untitled Hackathon'),
                    'description': data.get('description', 'No description available'),
                    'source': file.replace('scraped_', '').replace('.json', ''),
                    'date': data.get('date', 'Not available'),
                    'location': data.get('location', 'Not available'),
                    'link': data.get('link', f"https://{file.replace('scraped_', '').replace('.json', '')}"),
                    'keywords': data.get('keywords', '')
                }
                all_data.append(hackathon_data)
                
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    if all_data:
        print(f"Total number of hackathons loaded: {len(all_data)}")  # Debug print
        return all_data
    else:
        print("No data found in JSON files")  # Debug print
    return []

@app.route('/')
def index():
    hackathons = load_scraped_data()
    print(f"Number of hackathons being passed to template: {len(hackathons)}")  # Debug print
    return render_template('index.html', hackathons=hackathons)

@app.route('/run-scraper')
def run_scraper_route():
    """Route to run the scraper and redirect back to the index."""
    try:
        print("Starting scraper...")
        run_scraper()
        print("Scraper completed successfully")
    except Exception as e:
        print(f"Error running scraper: {str(e)}")
    return redirect(url_for('index'))

@app.route('/scrape')
def scrape():
    """Route to display scraped data."""
    scraped_data = {}
    txt_files = [f for f in os.listdir('.') if f.startswith('scraped_') and f.endswith('.txt')]
    
    for file in txt_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                source = file.replace('scraped_', '').replace('.txt', '')
                scraped_data[source] = content
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    return render_template('scrape.html', scraped_data=scraped_data)

if __name__ == '__main__':
    app.run(debug=True) 