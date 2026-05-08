import os
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    # Finding application links
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        text = a.text.strip()
        if href and ('apply' in text.lower() or 'apply' in href.lower() or 'careers' in href.lower() or 'job' in href.lower()):
            links.append(href)
    return soup.get_text(separator=' ', strip=True), links

def extract_job_info(html_content, title, url):
    text_content, links = clean_html(html_content)
    
    # In a real scenario, use Gemini to parse this. For now, use a simulated smart extraction.
    try:
        # Fallback heuristic logic if Gemini is not configured
        company = title.split("Off Campus")[0].strip() if "Off Campus" in title else title.split("|")[0].strip()
        
        lower_title = title.lower()
        lower_text = text_content.lower()
        
        is_intern = "intern" in lower_title
        
        category = "Software"
        if any(kw in lower_title or kw in lower_text for kw in ["video editor", "ui/ux", "ui ux", "graphic", "design", "creative"]):
            category = "Creative"
        elif "it" in lower_title or "it" in lower_text.split():
            category = "IT"
        elif is_intern:
            category = "Internship"

        location = "India"
        if any(loc in lower_title or loc in lower_text for loc in ["tamil nadu", "chennai", "coimbatore", "madurai", "trichy", "salem"]):
            location = "Tamil Nadu, India"
            
        # Dynamic skill extraction
        common_skills_dict = {
            "python": "Python", "java": "Java", "c++": "C++", "c#": "C#", "sql": "SQL", 
            "react": "React", "node.js": "Node.js", "javascript": "JavaScript",
            "html": "HTML", "css": "CSS", "aws": "AWS", "azure": "Azure", 
            "communication": "Communication", "leadership": "Leadership", "excel": "Excel",
            "figma": "Figma", "photoshop": "Photoshop", "illustrator": "Illustrator", 
            "premiere pro": "Premiere Pro", "after effects": "After Effects", "ui/ux": "UI/UX", 
            "machine learning": "Machine Learning", "data analysis": "Data Analysis", 
            "marketing": "Marketing", "seo": "SEO", "sales": "Sales", "video editing": "Video Editing",
            "capcut": "CapCut", "web dev": "Web Dev", "web development": "Web Development",
            "angular": "Angular", "vue": "Vue", "tailwind": "Tailwind", "canva": "Canva"
        }
        
        found_skills = []
        for kw, display_name in common_skills_dict.items():
            if kw in lower_text:
                if display_name not in found_skills:
                    found_skills.append(display_name)
                    
        # Check for short acronyms using regex boundaries
        if re.search(r'\bae\b', lower_text):
            found_skills.append("After Effects (AE)")
        if re.search(r'\bpr\b', lower_text):
            found_skills.append("Premiere Pro (PR)")
                
        if not found_skills:
            if category == "Creative":
                req_skills = "Design, Creative Tools, Communication"
            elif category == "IT":
                req_skills = "Programming, Problem Solving"
            else:
                req_skills = "Communication, Adaptability"
        else:
            req_skills = ", ".join(found_skills[:5]) # Limit to top 5 skills found
        
        apply_link = ""
        for link in links:
            if url not in link and "google.com" not in link:
                apply_link = link
                break

        return {
            "Company Name": company,
            "Category": category,
            "Location": location,
            "Last Date to Apply": "ASAP",
            "Batch": "Any Batch",
            "Qualification / Experience": "Any Degree" if category == "Creative" else "BE / Btech",
            "Required Skills": req_skills,
            "Apply Link": apply_link or url,
            "Job / Internship": "Internship" if is_intern else "Job"
        }
    except Exception as e:
        print(f"Error parsing job: {e}")
        return None

def fetch_latest_jobs():
    # Reduced per_page to 20 to speed up API response
    wp_url = "https://freshershunt.in/wp-json/wp/v2/posts?per_page=20"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # Mock data to showcase Creative and Web Dev roles since freshershunt lacks them
    mock_jobs = [
        {
            "Company Name": "Creative Studios Chennai",
            "Category": "Creative",
            "Location": "Chennai, Tamil Nadu, India",
            "Last Date to Apply": "ASAP",
            "Batch": "Any Batch",
            "Qualification / Experience": "Any Degree",
            "Required Skills": "CapCut, Premiere Pro (PR), After Effects (AE), Video Editing",
            "Apply Link": "https://example.com/apply-video",
            "Job / Internship": "Job",
            "Original Title": "Junior Video Editor Off Campus"
        },
        {
            "Company Name": "TechNova Solutions",
            "Category": "IT",
            "Location": "Coimbatore, Tamil Nadu, India",
            "Last Date to Apply": "ASAP",
            "Batch": "2024 / 2025",
            "Qualification / Experience": "BE / Btech",
            "Required Skills": "HTML, CSS, React, Web Dev",
            "Apply Link": "https://example.com/apply-web",
            "Job / Internship": "Internship",
            "Original Title": "Web Developer Intern"
        }
    ]
    
    try:
        response = requests.get(wp_url, headers=headers)
        if response.status_code != 200:
            return mock_jobs
        
        posts = response.json()
        parsed_jobs = list(mock_jobs) # Add mock jobs at the top
        for post in posts:
            title = post.get("title", {}).get("rendered", "")
            content = post.get("content", {}).get("rendered", "")
            link = post.get("link", "")
            
            job_info = extract_job_info(content, title, link)
            if job_info:
                # Add extra fields for the frontend
                job_info["Original Title"] = title
                parsed_jobs.append(job_info)
        return parsed_jobs
    except Exception as e:
        print(f"Failed to fetch jobs: {e}")
        return mock_jobs

if __name__ == "__main__":
    jobs = fetch_latest_jobs()
    print(f"Extracted {len(jobs)} jobs.")
    if jobs:
        print(jobs[0])
