from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path

# Import our custom modules
import scraper
import database

app = FastAPI(title="Competitor Tracker API")

# 1. Define the expected data structure from the frontend
class URLRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # Reads the index.html file and serves it to the browser
    html_content = Path("index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_content, status_code=200)

# 2. Create the POST endpoint
@app.post("/api/check_url")
async def check_url(request: URLRequest):
    url = request.url
    
    try:
        # Step A: Scrape the live website
        live_content = scraper.scrape_website_text(url)
        
        # Catch our scraper's custom error messages
        if live_content.startswith("Error:"):
            return {
                "status": "error",
                "changed": False,
                "message": live_content
            }
        
        # Step B: Get the saved content from the database
        saved_content = database.get_last_content(url)
        
        # Step C & D: Compare and update logic
        if saved_content is None:
            # Scenario 1: First time checking this URL
            database.update_site_content(url, live_content)
            return {
                "status": "success", 
                "changed": True, 
                "message": "First time tracking this URL. Content saved!"
            }
            
        elif live_content != saved_content:
            # Scenario 2: Content has changed
            database.update_site_content(url, live_content)
            return {
                "status": "success", 
                "changed": True, 
                "message": "Changes detected! Database updated with new content."
            }
            
        else:
            # Scenario 3: No changes
            return {
                "status": "success", 
                "changed": False, 
                "message": "No changes since the last check."
            }
            
    except Exception as e:
        # Catch-all for unexpected server errors
        return {
            "status": "error",
            "changed": False,
            "message": f"An unexpected server error occurred: {str(e)}"
        }