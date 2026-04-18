import json

SYSTEM_PROMPT = """You are a seasoned Series A venture capitalist with 12 years of investing experience across SaaS, fintech, and consumer tech. You evaluate pitch decks using a rigorous rubric. You are critical but constructive. Your task is to analyze slide data (which has been enriched with classical NLP) and provide a score from 1-5 for the given rubric dimension.

Dimensions:
1. Problem Clarity
2. Solution Differentiation
3. Market Sizing
4. Traction
5. Team Credibility
6. Ask Clarity
7. General (used when the slide doesn't fit a specific category - evaluate overall quality, clarity, and investor impact)

Follow this Chain-of-Thought structure for your evaluation:
Step 1: Identify what claim the founder is making.
Step 2: Check if evidence or data backs the claim.
Step 3: Flag any missing investor concern this slide doesn't address.
Step 4: Assign a score 1-5 with a one-sentence rationale.

Return the result ONLY as a valid JSON object matching this schema:
{
  "dimension": "<dimension_name>",
  "claim_identified": "<step 1 output>",
  "evidence_found": <true/false>,
  "missing_concern": "<step 3 output>",
  "score": <1-5>,
  "rationale": "<step 4 output>",
  "fix_suggestion": "<actionable advice to improve the slide>"
}"""

FEW_SHOT_EXAMPLES = {
    "Problem": """
Example 1 (Strong - Score 5):
Slide Text: "The cost of cloud storage is rising 15% YoY. Mid-market companies spend $120k annually on unused capacity due to fragmented provisioning tools."
Evaluation:
{
  "dimension": "Problem",
  "claim_identified": "Cloud storage costs are rising and mid-market companies overspend due to poor provisioning.",
  "evidence_found": true,
  "missing_concern": "None, highly specific and quantified.",
  "score": 5,
  "rationale": "Quantifies a painful, specific problem with clear evidence of financial waste.",
  "fix_suggestion": "None."
}

Example 2 (Weak - Score 2):
Slide Text: "Managing files is hard and companies waste time. We fix this."
Evaluation:
{
  "dimension": "Problem",
  "claim_identified": "Managing files is hard and wastes time.",
  "evidence_found": false,
  "missing_concern": "Lacks specific data, target audience, and scale of the problem.",
  "score": 2,
  "rationale": "The problem is generic and lacks quantifiable data to prove it is a severe pain point.",
  "fix_suggestion": "Quantify the time/money wasted and specify which type of companies suffer from this."
}
""",
    "General": """
Example 1 (Strong - Score 4):
Slide Text: "Our vision: By 2025, every SMB will have access to enterprise-grade analytics at 1/10th the cost. We're building the Shopify of data."
Evaluation:
{
  "dimension": "General",
  "claim_identified": "The company aims to democratize data analytics for SMBs at low cost.",
  "evidence_found": false,
  "missing_concern": "No timeline milestones or current metrics to back the vision statement.",
  "score": 4,
  "rationale": "Strong, memorable positioning with a clear analogy, but lacks supporting evidence.",
  "fix_suggestion": "Add a brief stat or milestone to ground the vision in current progress."
}
"""
    # Other dimensions can be added similarly
}

def build_prompt(slide_context, dimension):
    """
    Constructs the final prompt combining system role, few-shot examples, and the specific slide context.
    """
    examples = FEW_SHOT_EXAMPLES.get(dimension, "")
    
    prompt = f"{SYSTEM_PROMPT}\n\n"
    if examples:
        prompt += f"--- FEW SHOT EXAMPLES ---\n{examples}\n\n"
        
    prompt += f"--- TARGET SLIDE CONTEXT ---\n"
    prompt += json.dumps(slide_context, indent=2)
    prompt += f"\n\nNow, evaluate this target slide for the '{dimension}' dimension and return the JSON output."
    
    return prompt
