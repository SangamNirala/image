#!/usr/bin/env python3

import os
import sys
sys.path.append('/app/backend')

from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

def test_image_generation():
    """Test business card generation and inspect response structure"""
    
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    
    # Simple business card prompt
    prompt = """Generate a professional business card design for:
Company: EcoFlow Solutions
Contact: John Smith, CEO
Email: john@ecoflow.com
Phone: (555) 123-4567

Create a clean, modern business card with the company logo integrated."""
    
    try:
        print("Making API call to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=prompt
        )
        
        print("Response received!")
        print(f"Response type: {type(response)}")
        print(f"Response dir: {dir(response)}")
        
        if hasattr(response, 'candidates'):
            print(f"Candidates: {len(response.candidates)}")
            for i, candidate in enumerate(response.candidates):
                print(f"  Candidate {i}: {type(candidate)}")
                print(f"  Candidate {i} dir: {dir(candidate)}")
                
                if hasattr(candidate, 'content'):
                    print(f"    Content: {type(candidate.content)}")
                    print(f"    Content dir: {dir(candidate.content)}")
                    
                    if hasattr(candidate.content, 'parts'):
                        print(f"      Parts: {len(candidate.content.parts)}")
                        for j, part in enumerate(candidate.content.parts):
                            print(f"        Part {j}: {type(part)}")
                            print(f"        Part {j} dir: {dir(part)}")
                            
                            if hasattr(part, 'inline_data'):
                                print(f"          Inline data: {type(part.inline_data)}")
                                print(f"          Inline data dir: {dir(part.inline_data)}")
                                
                                if hasattr(part.inline_data, 'data'):
                                    data = part.inline_data.data
                                    print(f"            Data type: {type(data)}")
                                    print(f"            Data length: {len(data) if data else 'None'}")
                                    if data:
                                        print(f"            Data preview: {str(data)[:100]}...")
                                        
                                        # Try to determine if it's valid base64
                                        if isinstance(data, str):
                                            try:
                                                import base64
                                                decoded = base64.b64decode(data)
                                                print(f"            Successfully decoded base64 ({len(decoded)} bytes)")
                                            except Exception as e:
                                                print(f"            Base64 decode failed: {e}")
                                        
                            if hasattr(part, 'text'):
                                print(f"          Text part: {part.text[:100]}...")
                                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_generation()