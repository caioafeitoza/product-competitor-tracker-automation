from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import difflib

# Import our custom modules
import scraper
import database
import analyzer

app = FastAPI(title="Competitor Tracker API")

class URLRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # Reads the index.html file and serves it to the browser
    html_content = Path("index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/api/check_url")
async def check_url(request: URLRequest):
    url = request.url
    
    try:
        # Step A: Scrape the live website
        live_content = scraper.scrape_website_text(url)
        
        if live_content.startswith("Error:"):
            return {
                "status": "error",
                "changed": False,
                "message": live_content,
                "summary": None,
                "raw_diff": None
            }
        
        # Step B: Get the saved content from the database
        saved_content = database.get_last_content(url)
        
        # Step C: Compare, Analyze, and Update
        if saved_content is None:
            # First time checking
            database.update_site_content(url, live_content)
            return {
                "status": "success", 
                "changed": True, 
                "message": "First time tracking this URL. Content saved!",
                "summary": "<p class='text-slate-600 italic'>Initial scrape complete. AI will summarize changes on the next check.</p>",
                "raw_diff": "No previous data to compare against."
            }
            
        elif live_content != saved_content:
            # Changes detected! Let's generate the diff and summary.
            
            # 1. Generate Raw Diff (splitlines is required for difflib)
            diff_lines = difflib.unified_diff(
                saved_content.splitlines(),
                live_content.splitlines(),
                fromfile='Previous Scrape',
                tofile='Live Website',
                lineterm=''
            )
            raw_diff_text = '\n'.join(list(diff_lines))
            
            # 2. Generate AI Summary
            ai_summary_html = analyzer.summarize_changes(saved_content, live_content)
            
            # 3. Save new content to DB *after* analysis is done
            database.update_site_content(url, live_content)
            
            return {
                "status": "success", 
                "changed": True, 
                "message": "Changes detected! We updated the database with the new content.",
                "summary": ai_summary_html,
                "raw_diff": raw_diff_text
            }
            
        else:
            # No changes
            return {
                "status": "success", 
                "changed": False, 
                "message": "No changes since the last check.",
                "summary": None,
                "raw_diff": None
            }
            
    except Exception as e:
        return {
            "status": "error",
            "changed": False,
            "message": f"An unexpected server error occurred: {str(e)}",
            "summary": None,
            "raw_diff": None
        }