# Freshershunt Jobs Automation Dashboard

A modern full-stack web application that autonomously fetches fresher IT jobs from Freshershunt, manages duplicates, provides a dynamic dashboard, and synchronizes the results flawlessly with Google Sheets.

## Project Structure

- `frontend/` - React + Vite application featuring a premium "glassmorphism" based UI.
- `backend/` - FastAPI backend handles scraping logic, API routes, scheduled auto-syncing, and Google Sheets integration.

## Installation & Running

### 1. Backend Setup

1. Open a new terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

Note: Background auto-sync is automatically scheduled in the backend to trigger at 8:00 AM, 1:00 PM, and 7:00 PM daily.

### 2. Frontend Setup

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Run the frontend local server:
   ```bash
   npm run dev
   ```
3. Open the provided `localhost` link to view the dashboard!

## Configuration (Google Sheets)

To enable the "Auto Sync to Sheets" feature:

1. Create a `credentials.json` file inside the `backend` folder containing your Google Service Account keys. See `backend/credentials.json.example` for the format.
2. Ensure you have granted "Editor" access to the Google Sheet link you provided in your account by sharing the sheet with your `client_email` located inside `credentials.json`.
3. In `backend/services/sheets.py`, the Sheet ID `1qMPebxWPFy89RFz0FDgq6p4wPLi6n7NcsdOIP3_hD3s` is already linked.

## Features Included

- ✅ Scraping from `freshershunt.in` using high-speed WP API
- ✅ Extraction of required fields (Company name, category, required skills matching logic)
- ✅ Intelligent duplicate prevention using `Apply Links`
- ✅ Dynamic, premium glassmorphism styling in the UI
- ✅ Instant preview and CSV export function
- ✅ Auto scheduling ready to run background tasks daily
