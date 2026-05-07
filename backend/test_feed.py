import requests
import xml.etree.ElementTree as ET

url = "https://freshershunt.in/feed/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    # the feed is RSS 2.0 so root is rss -> channel -> items
    channel = root.find("channel")
    items = channel.findall("item")
    print(f"Found {len(items)} items in feed")
    for item in items[:5]:
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        category = [c.text for c in item.findall("category")]
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Categories: {category}")
        print("-------------")
else:
    print("Failed to fetch feed")
