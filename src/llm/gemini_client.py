import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from .prompts import build_prompt
from tqdm import tqdm

load_dotenv()

# Configure API client
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

# Define generation config for JSON response
generation_config = types.GenerateContentConfig(
    temperature=0.2,
    top_p=1,
    top_k=1,
    max_output_tokens=2048,
    response_mime_type="application/json",
)

def evaluate_slide_with_llm(slide_context, dimension="Problem", retries=3):
    """
    Sends the enriched slide context to Gemini for evaluation, with basic retry logic.
    """
    if not client:
        print("Error: GEMINI_API_KEY not found in environment.")
        return None
        
    prompt = build_prompt(slide_context, dimension)
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=generation_config
            )
            # Parse the JSON string response
            return json.loads(response.text)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))  # Exponential backoff
                continue
            print(f"\nLLM Error on slide {slide_context.get('slide_number')}: {e}")
            return None

def process_deck_with_llm(enriched_slides):
    """
    Processes all slides in a deck, including those with 'Unknown' slide types.
    Unknown slides are evaluated with a 'General' dimension to ensure no slide is skipped.
    """
    results = []
    
    # Use tqdm for progress tracking
    print("\nStarting LLM Evaluation Pipeline...")
    try:
        for slide in tqdm(enriched_slides, desc="Scoring slides via Gemini API", unit="slide"):
            dimension = slide.get("slide_type", "Unknown")
            
            # Use "General" for Unknown slides instead of skipping them
            eval_dimension = dimension if dimension != "Unknown" else "General"
            
            # Only skip slides with truly empty text (no content at all)
            raw_text = slide.get("raw_text", "").strip()
            if not raw_text:
                # Mark as unevaluated but don't send to LLM
                slide["llm_evaluation"] = {
                    "dimension": eval_dimension,
                    "claim_identified": "No text content detected on this slide (likely an image-only slide).",
                    "evidence_found": False,
                    "missing_concern": "Slide contains no extractable text. Consider adding key text points alongside visuals.",
                    "score": 1,
                    "rationale": "Image-only slides without supporting text are difficult to evaluate and may lack clarity for investors.",
                    "fix_suggestion": "Add concise text overlay or speaker notes to communicate the key message of this visual."
                }
            else:
                eval_result = evaluate_slide_with_llm(slide, eval_dimension)
                if eval_result:
                    slide["llm_evaluation"] = eval_result
                    
            results.append(slide)
            time.sleep(2) # Small delay to avoid aggressive rate-limiting
    except KeyboardInterrupt:
        print("\nProcess interrupted by user! Saving progress so far...")
        
    return results
