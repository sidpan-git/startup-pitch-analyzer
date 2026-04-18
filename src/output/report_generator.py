import json
import os
from fpdf import FPDF
from datetime import datetime

def sanitize_text(text):
    """
    Replaces unicode characters with ascii equivalents so fpdf helvetica doesn't crash.
    """
    if not isinstance(text, str):
        return str(text)
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u00a0': ' ',
        '\u2022': '-', '\u00b7': '-'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_priority_fix_list(evaluated_slides):
    fixes = []
    for slide in evaluated_slides:
        eval_data = slide.get("llm_evaluation")
        if eval_data and eval_data.get("score", 5) <= 3:
            fixes.append({
                "dimension": eval_data.get("dimension", "Unknown"),
                "slide_number": slide.get("slide_number"),
                "score": eval_data.get("score"),
                "issue": eval_data.get("missing_concern"),
                "suggestion": eval_data.get("fix_suggestion")
            })
    fixes.sort(key=lambda x: x["score"])
    return fixes

def generate_one_paragraph_verdict(scores_dict):
    if not scores_dict: return "No data available."
    avg_score = sum(scores_dict.values()) / len(scores_dict)
    weak_points = [k for k, v in scores_dict.items() if v <= 3]
    strong_points = [k for k, v in scores_dict.items() if v >= 4]
    
    verdict = f"This pitch deck scored an average of {avg_score:.1f}/5. "
    if strong_points:
        verdict += f"It demonstrates strengths in {', '.join(strong_points)}. "
    if weak_points:
        verdict += f"However, it requires significant improvements in {', '.join(weak_points)} before presenting to investors. "
        
    if avg_score >= 4:
        verdict += "Overall, it is a highly competitive deck."
    elif avg_score >= 3:
        verdict += "Overall, it shows promise but needs refinement."
    else:
        verdict += "Overall, it needs a major overhaul to clearly communicate the business case."
    return verdict

class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Startup Pitch Deck Evaluator - Automated AI Report", border=False, ln=True, align="R")
        
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", border=False, ln=True, align="C")

def create_pdf_report(report_data, output_path="data/processed/report.pdf"):
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # === COVER PAGE ===
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("helvetica", "B", 28)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 20, "PITCH DECK EVALUATION", ln=True, align="C")
    
    pdf.set_font("helvetica", "", 16)
    pdf.set_text_color(108, 117, 125)
    pdf.cell(0, 10, "Comprehensive AI & NLP Analysis Report", ln=True, align="C")
    
    pdf.ln(20)
    pdf.set_font("helvetica", "I", 12)
    date_str = datetime.now().strftime("%B %d, %Y")
    pdf.cell(0, 10, f"Generated on: {date_str}", ln=True, align="C")
    
    # === EXECUTIVE SUMMARY ===
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 15, "1. Executive Summary", ln=True)
    #pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Verdict Box
    # pdf.set_fill_color(248, 249, 250) (Doesn't work without RGB list sometimes)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(33, 37, 41)
    pdf.multi_cell(0, 10, sanitize_text(report_data.get("verdict", "N/A")), border=1)
    pdf.ln(10)
    
    # Visualizations
    radar_path = "data/processed/radar_chart.png"
    nlp_path = "data/processed/nlp_metrics.png"
    
    start_y = pdf.get_y()
    if os.path.exists(radar_path):
        pdf.image(radar_path, x=10, y=start_y, w=95)
    if os.path.exists(nlp_path):
        pdf.image(nlp_path, x=105, y=start_y+10, w=100)
    
    # === PRIORITY FIXES ===
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 15, "2. Priority Fixes (Critical Issues)", ln=True)
    pdf.ln(5)
    
    fixes = report_data.get("priority_fixes", [])
    if not fixes:
        pdf.set_font("helvetica", "I", 12)
        pdf.cell(0, 10, "No major issues found! All slides scored > 3.", ln=True)
    else:
        for fix in fixes:
            pdf.set_font("helvetica", "B", 14)
            pdf.set_text_color(220, 53, 69) # Red
            pdf.cell(0, 10, sanitize_text(f"Slide {fix['slide_number']} | {fix['dimension']} | Score: {fix['score']}/5"), ln=True)
            
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(33, 37, 41)
            pdf.cell(0, 8, "Issue: ", ln=True)
            pdf.set_font("helvetica", "", 11)
            pdf.multi_cell(0, 8, sanitize_text(fix['issue']))
            
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(25, 135, 84) # Green
            pdf.cell(0, 8, "Suggestion: ", ln=True)
            pdf.set_font("helvetica", "", 11)
            pdf.set_text_color(33, 37, 41)
            pdf.multi_cell(0, 8, sanitize_text(fix['suggestion']))
            pdf.ln(5)

    # === DETAILED SLIDE ANALYSIS ===
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    pdf.cell(0, 15, "3. Slide-by-Slide Analysis & NLP Metrics", ln=True)
    pdf.ln(5)
    
    for slide in report_data.get("slide_details", []):
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, f"Slide {slide.get('slide_number')} - {slide.get('slide_type', 'Unknown')}", ln=True)
        
        # NLP Metrics
        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(108, 117, 125)
        metrics_str = f"Readability Grade: {slide.get('readability_score', 0):.1f} | Jargon Density: {slide.get('jargon_score', 0):.2f}"
        pdf.cell(0, 8, metrics_str, ln=True)
        pdf.set_text_color(33, 37, 41)
        
        eval_data = slide.get("llm_evaluation")
        if eval_data:
            pdf.set_font("helvetica", "B", 11)
            pdf.cell(0, 6, f"Score: {eval_data.get('score', 'N/A')}/5", ln=True)
            
            pdf.set_font("helvetica", "B", 11)
            pdf.cell(0, 6, "Rationale:", ln=True)
            pdf.set_font("helvetica", "", 11)
            pdf.multi_cell(0, 6, sanitize_text(eval_data.get('rationale', '')))
        else:
            pdf.set_font("helvetica", "I", 11)
            pdf.cell(0, 6, "No LLM evaluation for this slide.", ln=True)
        
        pdf.ln(5)
            
    pdf.output(output_path)

def generate_full_report(evaluated_slides, output_path="data/processed/report.json"):
    # Aggregate scores: average across slides with the same dimension
    from collections import defaultdict
    dim_scores = defaultdict(list)
    for slide in evaluated_slides:
        eval_data = slide.get("llm_evaluation")
        if eval_data and eval_data.get("dimension") and eval_data.get("score") is not None:
            dim_scores[eval_data["dimension"]].append(eval_data["score"])
    
    scores_dict = {dim: round(sum(scores) / len(scores), 1) for dim, scores in dim_scores.items()}
            
    report = {
        "scores": scores_dict,
        "radar_chart_path": "data/processed/radar_chart.png",
        "verdict": generate_one_paragraph_verdict(scores_dict),
        "priority_fixes": generate_priority_fix_list(evaluated_slides),
        "slide_details": evaluated_slides
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
        
    try:
        create_pdf_report(report, output_path.replace(".json", ".pdf"))
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
        
    return report