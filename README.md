#Competitor Tracker
A lightweight, local tool for Product Managers to automatically track changes on competitor websites (like pricing pages or feature lists).

Instead of manually checking websites or staring at messy code diffs, this tool scrapes the page, compares it to the last version, and uses Google Gemini to give you a quick, 3-bullet summary of what actually changed from a business perspective.

##How it works
Paste a URL (e.g., a competitor's pricing page).

The app scrapes the text and saves it to a local SQLite database.

The next time you check that URL, it compares the live site to the saved version.

If there's a change, the Gemini API summarizes the business impact, and gives you the option to toggle open the raw, line-by-line text diff.

##Tech Stack
Backend: Python, FastAPI

Database: SQLite (built-in, no setup required)

Frontend: Vanilla HTML/JS styled with Tailwind CSS

AI/LLM: Google Gemini API

##Local Setup
1. Set up your environment
Navigate to your project folder and create a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
2. Install dependencies

Bash
pip install fastapi uvicorn requests beautifulsoup4 google-genai python-dotenv
3. Add your API Key
Create a file named .env in the root folder and add your Gemini API key securely:

Plaintext
GEMINI_API_KEY="your_api_key_here"
4. Run the app

Bash
uvicorn main:app --reload
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to use the tool.

##Helpful Scripts Included
manage_db.py: Run this in your terminal to quickly view all tracked URLs or delete a specific one from the database.

trigger_test.py: A testing script that injects a fake pricing change into your local database so you can test the AI UI without having to wait for a real website to update.

##Roadmap
[ ] Migrate local SQLite database to Supabase.

[ ] Deploy backend to Render.com for a free production environment.

[ ] Add background scheduling (APScheduler) to run sweeps automatically daily.

[ ] Integrate Slack webhooks for zero-click notifications.