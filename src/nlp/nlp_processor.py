import spacy
import textstat

# Load spaCy model (will be downloaded via command line)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spacy en_core_web_sm not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

VC_JARGON = set([
    "synergy", "disrupt", "pivot", "runway", "burn rate", "churn", "saas", 
    "b2b", "b2c", "roi", "kpi", "unicorn", "agile", "bootstrapped", "mvp",
    "freemium", "go-to-market", "gtm", "moat", "network effects", "scale", 
    "scalable", "tam", "sam", "som", "cac", "ltv", "arr", "mrr", "hockey stick"
])

def extract_ner(doc):
    """Extracts entities of interest: ORG, MONEY, DATE, PERCENT."""
    entities = {
        "organizations": [],
        "monetary_values": [],
        "dates": [],
        "percentages": []
    }
    if not doc: return entities
    
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "MONEY":
            entities["monetary_values"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
        elif ent.label_ in ["PERCENT", "CARDINAL"]:  # Often percentages or numbers
            entities["percentages"].append(ent.text)
            
    # Deduplicate
    return {k: list(set(v)) for k, v in entities.items()}

def compute_claim_density(doc):
    """Computes adjective to noun ratio as a proxy for claim density."""
    if not doc: return 0.0
    
    adjectives = sum(1 for token in doc if token.pos_ == "ADJ")
    nouns = sum(1 for token in doc if token.pos_ in ["NOUN", "PROPN"])
    
    if nouns == 0:
        return 0.0
    return round(adjectives / nouns, 2)

def compute_jargon_score(text):
    """Computes jargon density based on predefined VC terms."""
    if not text: return 0.0
    words = [w.strip(".,!?\"'()") for w in text.lower().split()]
    if not words: return 0.0
    
    jargon_count = sum(1 for word in words if word in VC_JARGON)
    return round(jargon_count / len(words), 3)

def enrich_slides_with_nlp(slides_data):
    """
    Adds classical NLP enrichments to each slide in the data.
    """
    for slide in slides_data:
        text = slide.get("raw_text", "")
        
        # Initialize defaults
        try:
            slide["readability_score"] = textstat.flesch_kincaid_grade(text) if text else 0.0
        except Exception:
            slide["readability_score"] = 0.0
            
        slide["jargon_score"] = compute_jargon_score(text)
        slide["ner_entities"] = {"organizations": [], "monetary_values": [], "dates": [], "percentages": []}
        slide["claim_density"] = 0.0
        
        if nlp and text:
            doc = nlp(text)
            slide["ner_entities"] = extract_ner(doc)
            slide["claim_density"] = compute_claim_density(doc)
            
    return slides_data
