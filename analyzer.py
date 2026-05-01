import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()

# Initialize the Gemini client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def summarize_changes(old_text: str, new_text: str) -> str:
    """
    Compares two website scrapes and returns a 3-bullet HTML summary 
    of the most important business or pricing changes.
    """
    if not api_key:
        return "<ul class='list-disc pl-5'><li>⚠️ Error: GEMINI_API_KEY not found in .env file.</li></ul>"

    # Strict system prompt to constrain the LLM's output
    prompt = f"""
    You are a Senior Product Manager analyzing competitor website changes.
    Compare the following old website text and new website text.
    Identify the most important business, feature, or pricing changes.
    
    Rules:
    1. Return EXACTLY 3 bullet points summarizing the changes.
    2. Format the output STRICTLY as basic HTML (<ul><li>...</li></ul>).
    3. Do not include any markdown formatting or backticks (like ```html).
    4. Ignore minor grammatical fixes, typos, or boilerplate text changes.
    5. Be concise and focus on business value.
    
    Old Text:
    {old_text}
    
    New Text:
    {new_text}
    """

    try:
        # Call the Gemini 1.5 Flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1, # Low temperature for factual, deterministic analysis
            )
        )
        
        # Clean up the response to ensure no rogue markdown breaks our frontend
        html_output = response.text.replace("```html", "").replace("```", "").strip()
        
        # Inject Tailwind classes into the <ul> for cleaner UI rendering later
        if "<ul>" in html_output:
            html_output = html_output.replace("<ul>", "<ul class='list-disc pl-5 space-y-2 text-slate-700'>")
            
        return html_output
        
    except Exception as e:
        print(f"AI Analyzer Error: {str(e)}")
        # Graceful fallback so the app doesn't crash if the API fails
        return "<ul class='list-disc pl-5 text-red-600'><li>⚠️ AI summary currently unavailable. Please view raw changes.</li></ul>"

# Simple test block (will only run if you execute analyzer.py directly)
if __name__ == "__main__":
    old = "Pro plan is $49/month. Includes 5 team members and basic support."
    new = "Pro plan is $59/month. Includes 5 team members, 24/7 priority support, and custom reporting."
    print("Testing AI Analyzer...")
    print(summarize_changes(old, new))