import os
import json
from pathlib import Path

# Load environment first
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded .env from: {env_path}")
except ImportError:
    print("Warning: python-dotenv not available")

# Test direct Gemini call
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"API Key available: {bool(api_key)}")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=(
                "You are LawGic AI, a legal assistant. Provide concise, structured legal analysis "
                "as JSON with keys: category (string), summary (string), key_points (array of strings), "
                "recommendations (array of strings), risk_level (string), disclaimer (string)."
            ),
        )
        
        test_text = "This is a contract agreement with automatic renewal and binding arbitration."
        
        print("Testing direct Gemini API call...")
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1024,
            response_mime_type="application/json",
        )
        
        response = model.generate_content(
            test_text,
            generation_config=generation_config,
        )
        
        print(f"Response type: {type(response)}")
        print(f"Response text: {response.text}")
        
        try:
            parsed = json.loads(response.text)
            print(f"Parsed JSON keys: {list(parsed.keys())}")
            print(f"Category: {parsed.get('category', 'N/A')}")
            print(f"Risk level: {parsed.get('risk_level', 'N/A')}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            
    else:
        print("No API key found in environment")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()