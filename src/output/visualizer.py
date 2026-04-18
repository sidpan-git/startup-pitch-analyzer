import matplotlib.pyplot as plt
import numpy as np
import os

def generate_radar_chart(scores_dict, output_path="data/processed/radar_chart.png"):
    """
    Generates a radar chart for the 6-dimension rubric scores.
    """
    if not scores_dict:
        print("No scores provided for radar chart.")
        return
        
    labels=np.array(list(scores_dict.keys()))
    stats=np.array(list(scores_dict.values()))
    
    # Needs to be closed loop
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    
    # Close the polygon
    stats=np.concatenate((stats,[stats[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    
    fig=plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, color='teal')
    ax.fill(angles, stats, alpha=0.25, color='teal')
    
    # Add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=10)
    
    ax.set_title("Pitch Deck Evaluation Scorecard", weight='bold', size=14, pad=20)
    
    # Set radial limits
    ax.set_ylim(0,5)
    ax.set_yticks([1, 2, 3, 4, 5])
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def generate_nlp_metrics_chart(evaluated_slides, output_path="data/processed/nlp_metrics.png"):
    """
    Generates a bar chart showing Readability and Jargon score across slides.
    """
    slide_nums = []
    readability = []
    jargon = []
    
    for slide in evaluated_slides:
        slide_nums.append(f"Slide {slide.get('slide_number')}")
        readability.append(slide.get('readability_score', 0))
        # Scale jargon up for visibility since it's usually < 0.1
        jargon.append(slide.get('jargon_score', 0) * 100) 
        
    x = np.arange(len(slide_nums))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width/2, readability, width, label='Readability Grade', color='cornflowerblue')
    rects2 = ax.bar(x + width/2, jargon, width, label='Jargon Density (x100)', color='salmon')
    
    ax.set_ylabel('Scores')
    ax.set_title('NLP Metrics per Slide')
    ax.set_xticks(x)
    ax.set_xticklabels(slide_nums, rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
