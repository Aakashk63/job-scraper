from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel
from typing import List, Optional
import datetime

from services.scraper import fetch_latest_jobs
from services.sheets import store_jobs_in_sheet

app = FastAPI(title="Job Scraper API")

# Setup CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for today's jobs for the dashboard
# A real app would use a database
scraped_jobs_cache = []
last_updated = None

def scheduled_job():
    print(f"Running scheduled sync at {datetime.datetime.now()}")
    jobs = fetch_latest_jobs()
    if jobs:
        global scraped_jobs_cache
        global last_updated
        scraped_jobs_cache = jobs
        last_updated = datetime.datetime.now().isoformat()
        store_jobs_in_sheet(jobs)

# Setup scheduler
scheduler = BackgroundScheduler()
# 8:00 AM, 1:00 PM, 7:00 PM
scheduler.add_job(scheduled_job, 'cron', hour='8,13,19', minute='0')
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/api/jobs")
def get_jobs():
    return {
        "jobs": scraped_jobs_cache,
        "last_updated": last_updated,
        "total_jobs": len(scraped_jobs_cache),
        "tn_jobs": len([j for j in scraped_jobs_cache if 'tamil nadu' in j.get('Location', '').lower() or 'chennai' in j.get('Location', '').lower()])
    }

@app.post("/api/scrape")
def trigger_scrape():
    global scraped_jobs_cache
    global last_updated
    jobs = fetch_latest_jobs()
    if jobs:
        scraped_jobs_cache = jobs
        last_updated = datetime.datetime.now().isoformat()
        return {"success": True, "message": "Scraped successfully", "jobs_count": len(jobs)}
    else:
        return {"success": False, "message": "No jobs found or website down"}

@app.post("/api/sync")
def trigger_sync():
    global scraped_jobs_cache
    if not scraped_jobs_cache:
        # fetch first in case
        scraped_jobs_cache = fetch_latest_jobs()
        
    result = store_jobs_in_sheet(scraped_jobs_cache)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
