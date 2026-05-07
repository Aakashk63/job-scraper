import requests
from bs4 import BeautifulSoup

url = "https://freshershunt.in/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # Looking for article or div elements that usually contain jobs
    articles = soup.find_all('article')
    for idx, article in enumerate(articles[:5]):
        print(f"--- Article {idx+1} ---")
        title_tag = article.find('h2') or article.find('h3')
        if title_tag:
            print("Title:", title_tag.text.strip())
            a_tag = title_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                print("Link:", a_tag['href'])
        
        # Print all text in the article
        print("Text preview:", article.text.strip()[:200].replace('\n', ' '))
else:
    print("Failed to fetch.")
