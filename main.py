import os
from src.ingestion.extractor import extract_text
from src.ingestion.labeller import process_slides
from src.nlp.nlp_processor import enrich_slides_with_nlp
from src.llm.gemini_client import process_deck_with_llm
from src.output.visualizer import generate_radar_chart, generate_nlp_metrics_chart
from src.output.report_generator import generate_full_report

def evaluate_pitch_deck(file_path):
    print(f"Starting evaluation for {file_path}...")
    
    # Stage 1: Ingestion & Preprocessing
    print("Stage 1: Extracting text and labeling slides...")
    raw_slides = extract_text(file_path)
    labeled_slides = process_slides(raw_slides)
    
    # Stage 2: Classical NLP Layer
    print("Stage 2: Enriching with NLP metadata (NER, Readability, Jargon)...")
    enriched_slides = enrich_slides_with_nlp(labeled_slides)
    
    # Stage 3: LLM Engineering with Gemini
    print("Stage 3: Evaluating with Gemini API...")
    evaluated_slides = process_deck_with_llm(enriched_slides)
    
    # Stage 4: Output Generation
    print("\nStage 4: Generating reports and visualizations...")
    # First generate the charts
    generate_nlp_metrics_chart(evaluated_slides)
    
    # Create the report and radar chart
    report = generate_full_report(evaluated_slides)
    if "scores" in report and report["scores"]:
        generate_radar_chart(report["scores"])
        # Regenerate report PDF to include the radar chart now that it exists
        generate_full_report(evaluated_slides)
        
    print(f"\nEvaluation complete! Check data/processed/ for results (JSON, PNG, PDF).")
    print(f"Verdict: {report.get('verdict')}")
    return report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate a Pitch Deck")
    parser.add_argument("filepath", help="Path to the PDF or PPTX pitch deck")
    args = parser.parse_args()
    
    if os.path.exists(args.filepath):
        evaluate_pitch_deck(args.filepath)
    else:
        print(f"File not found: {args.filepath}")

