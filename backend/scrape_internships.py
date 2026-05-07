import requests
from bs4 import BeautifulSoup
import re

def scrape_internships_and_placements(pages=2):
    """
    Scrapes freshershunt.in (or can be adapted for any site) using BeautifulSoup
    to extract Internship and Placement details specifically.
    """
    base_url = "https://freshershunt.in/page/{}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    scraped_data = []
    
    print(f"Starting web scraper for Internships & Placements...")
    
    for page in range(1, pages + 1):
        url = base_url.format(page) if page > 1 else "https://freshershunt.in/"
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to load page {page}. Status Code: {response.status_code}")
                continue
                
            # Initialize the web scraper (BeautifulSoup)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all job post containers
            articles = soup.find_all('article')
            
            for article in articles:
                # Extract title and link
                title_element = article.find('h2') or article.find('h3')
                if not title_element:
                    continue
                    
                title_text = title_element.get_text(strip=True)
                link_element = title_element.find('a')
                post_link = link_element['href'] if link_element and 'href' in link_element.attrs else None
                
                # Filter logic: Check if it's an internship or placement drive
                is_internship = re.search(r'\bintern(ship)?\b', title_text, re.IGNORECASE)
                is_placement = re.search(r'\b(placement|campus drive|off campus)\b', title_text, re.IGNORECASE)
                
                if is_internship or is_placement:
                    # Extract brief description text
                    summary = article.get_text(separator=' ', strip=True)
                    
                    data = {
                        "title": title_text,
                        "type": "Internship" if is_internship else "Placement/Drive",
                        "link": post_link,
                        "preview": summary[:150] + "..." # Quick preview
                    }
                    scraped_data.append(data)
                    print(f"[FOUND] {data['type']}: {title_text}")
                    
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            
    return scraped_data

if __name__ == "__main__":
    results = scrape_internships_and_placements(pages=3)
    print(f"\n--- Scraping Complete ---")
    print(f"Total Internship & Placement opportunities found: {len(results)}")
    
    for idx, item in enumerate(results, 1):
        print(f"\n{idx}. {item['title']} ({item['type']})")
        print(f"   Link: {item['link']}")
