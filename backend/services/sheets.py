import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def get_sheet():
    # Define scope
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    # In a real app we'd load this from a valid service account json file
    creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
    
    if not os.path.exists(creds_path):
        return None, "Error: credentials.json not found in backend/. Please add a Google Service Account JSON."
        
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        # 1qMPebxWPFy89RFz0FDgq6p4wPLi6n7NcsdOIP3_hD3s
        sheet = client.open_by_key("1qMPebxWPFy89RFz0FDgq6p4wPLi6n7NcsdOIP3_hD3s").sheet1
        return sheet, "Success"
    except Exception as e:
        return None, f"Error authenticating with Google Sheets: {e}"

def store_jobs_in_sheet(jobs):
    sheet, msg = get_sheet()
    if not sheet:
        print(msg)
        return {"success": False, "message": msg}
        
    try:
        existing_records = sheet.get_all_records()
        existing_links = {row.get('Apply Link', '') for row in existing_records}
        
        # Calculate next S.No
        next_sno = len(existing_records) + 1
        
        rows_to_insert = []
        for job in jobs:
            if job['Apply Link'] not in existing_links:
                row = [
                    next_sno,
                    job.get('Company Name', ''),
                    job.get('Category', ''),
                    job.get('Location', ''),
                    job.get('Last Date to Apply', ''),
                    job.get('Batch', ''),
                    job.get('Qualification / Experience', ''),
                    job.get('Required Skills', ''),
                    job.get('Apply Link', ''),
                    job.get('Job / Internship', '')
                ]
                rows_to_insert.append(row)
                existing_links.add(job['Apply Link'])
                next_sno += 1
                
        if rows_to_insert:
            sheet.append_rows(rows_to_insert)
            
            # Format rows green (pseudo-code, using gspread formatting APIs is complex but we can do a basic append)
            # Actually, Google Sheets API can color rows but `gspread` needs `batch_update`
            # For simplicity, appending is good enough for now.
            
        return {"success": True, "inserted": len(rows_to_insert), "message": "Successfully updated sheet."}
    except Exception as e:
        return {"success": False, "message": f"Error updating sheet: {e}"}

