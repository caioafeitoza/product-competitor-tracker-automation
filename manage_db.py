import sqlite3

DB_NAME = "competitors.db"

def delete_url(target_url: str):
    """Deletes a specific URL from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if it exists first to give good feedback
    cursor.execute('SELECT id FROM tracked_sites WHERE url = ?', (target_url,))
    if cursor.fetchone():
        cursor.execute('DELETE FROM tracked_sites WHERE url = ?', (target_url,))
        conn.commit()
        print(f"✅ Success: Deleted '{target_url}' from the database.")
    else:
        print(f"⚠️ Error: Could not find '{target_url}' in the database.")
        
    conn.close()

def show_all_sites():
    """Prints all currently tracked sites so you know what is in there."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, url, last_checked FROM tracked_sites')
    rows = cursor.fetchall()
    
    print("\n--- Currently Tracked Sites ---")
    if not rows:
        print("Database is empty.")
    else:
        for row in rows:
            print(f"ID: {row[0]} | URL: {row[1]} | Last Checked: {row[2]}")
    print("-------------------------------\n")
    conn.close()

if __name__ == "__main__":
    # 1. First, see what is in your database:
    show_all_sites()
    
    # 2. To delete a specific site, uncomment the line below and add the exact URL:
    # delete_url("https://example.com")
    
    # Run show_all_sites() again to verify it is gone
    # show_all_sites()