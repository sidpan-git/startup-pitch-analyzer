import re

# Define regex patterns for slide types based on common keywords
SLIDE_PATTERNS = {
    "Problem": r"(?i)\b(problem|pain point|challenge|opportunity|why now|the issue)\b",
    "Solution": r"(?i)\b(solution|how it works|our product|platform|demo|technology|value proposition)\b",
    "Market": r"(?i)\b(market|tam|sam|som|market size|competitors|competition|landscape|target audience)\b",
    "Traction": r"(?i)\b(traction|milestones|metrics|growth|revenue|users|customers|case study)\b",
    "Team": r"(?i)\b(team|founders|leadership|advisors|board|who we are)\b",
    "Ask": r"(?i)\b(ask|financials|fundraising|use of funds|investment|financial projections)\b"
}

def label_slide(text):
    """
    Labels a slide based on regex matching of its raw text.
    Returns the matched label or 'Unknown'.
    """
    if not text:
        return "Unknown"
        
    for label, pattern in SLIDE_PATTERNS.items():
        if re.search(pattern, text):
            return label
            
    return "Unknown"

def process_slides(slides_data):
    """
    Takes a list of dictionaries containing 'slide_number' and 'raw_text'
    and adds a 'slide_type' key to each dictionary.
    """
    for slide in slides_data:
        slide["slide_type"] = label_slide(slide.get("raw_text", ""))
    return slides_data
