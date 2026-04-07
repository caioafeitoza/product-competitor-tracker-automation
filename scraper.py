import requests
from bs4 import BeautifulSoup

def scrape_website_text(url: str) -> str:
    """
    Fetches a URL and returns the cleaned text content, 
    stripping out scripts, styles, navigation, and footers.
    """
    # 1. Standard headers to prevent basic blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 2. Fetch the page with a timeout (don't wait forever)
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes (404, 500, etc.)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Return a clean error string if the fetch fails
        return f"Error: Unable to fetch {url}. Details: {str(e)}"

    # 3. Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Strip out unnecessary tags
    # We remove scripts and styles (never useful for text) and 
    # structural elements like nav, header, and footer that often 
    # change randomly or contain boilerplate text.
    tags_to_remove = ["script", "style", "nav", "footer", "header", "aside"]
    
    for element in soup(tags_to_remove):
        element.decompose() # This completely removes the tag and its contents

    # 5. Extract and clean the remaining text
    # get_text(separator=" ", strip=True) handles spacing between elements
    cleaned_text = soup.get_text(separator=" ", strip=True)

    # Optional: You could do further cleaning here (like removing multiple spaces),
    # but BeautifulSoup's strip=True does a decent job for our MVP.
    return cleaned_text

# Simple test block (will only run if you execute scraper.py directly)
if __name__ == "__main__":
    test_url = "https://example.com"
    print(f"Testing scraper on {test_url}...")
    result = scrape_website_text(test_url)
    print(f"\nResult:\n{result}")