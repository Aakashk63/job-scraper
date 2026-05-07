import requests
import json

url = "https://freshershunt.in/wp-json/wp/v2/posts?per_page=15"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)

if response.status_code == 200:
    posts = response.json()
    print(f"Found {len(posts)} posts via WP API")
    for post in posts[:3]:
        print(f"Title: {post.get('title', {}).get('rendered')}")
        print(f"Link: {post.get('link')}")
else:
    print("Failed to fetch.")
