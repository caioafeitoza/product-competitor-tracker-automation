import sqlite3
from datetime import datetime

DB_NAME = "competitors.db"

def init_db():
    """Creates the database and the tracked_sites table if they don't exist."""
    # Connects to the file (or creates it if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracked_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            last_content TEXT NOT NULL,
            last_checked TIMESTAMP NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_last_content(url: str):
    """Returns the last scraped content for a given URL, or None if not found."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT last_content FROM tracked_sites WHERE url = ?', (url,))
    result = cursor.fetchone()
    
    conn.close()
    
    # result is a tuple like ("scraped text...",), so we return the first item
    if result:
        return result[0]
    return None

def update_site_content(url: str, content: str):
    """Inserts a new site or updates the existing one with new content."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Store the exact time we checked it
    now = datetime.now().isoformat()
    
    # This is an "UPSERT" - a very clean way to Insert, or Update if the URL already exists
    cursor.execute('''
        INSERT INTO tracked_sites (url, last_content, last_checked)
        VALUES (?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET 
            last_content = excluded.last_content,
            last_checked = excluded.last_checked
    ''', (url, content, now))
    
    conn.commit()
    conn.close()

# Automatically initialize the database the first time this file is imported
init_db()

# Simple test block (will only run if you execute database.py directly)
if __name__ == "__main__":
    test_url = "https://example.com"
    print("Testing DB insert...")
    update_site_content(test_url, "This is the initial text.")
    
    print("Fetching from DB...")
    saved_text = get_last_content(test_url)
    print(f"Saved text: {saved_text}")
    
    print("Testing DB update...")
    update_site_content(test_url, "This is the NEW updated text.")
    updated_text = get_last_content(test_url)
    print(f"Updated text: {updated_text}")