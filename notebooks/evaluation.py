import numpy as np
from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr

def evaluate_metrics(human_scores, llm_scores):
    """
    Calculates Pearson r correlation between human and LLM scores.
    """
    if len(human_scores) != len(llm_scores) or len(human_scores) < 2:
        return {"pearson_r": None, "error": "Insufficient or mismatched data points."}
        
    try:
        pearson_corr, p_value = pearsonr(human_scores, llm_scores)
    except Exception as e:
        return {"pearson_r": None, "error": str(e)}
        
    return {
        "pearson_r": pearson_corr,
        "p_value": p_value,
        "meets_target": pearson_corr > 0.75
    }

def evaluate_inter_rater(annotator1_scores, annotator2_scores):
    """
    Computes Cohen's Kappa between two human annotators.
    """
    if len(annotator1_scores) != len(annotator2_scores) or not annotator1_scores:
        return {"kappa": None, "error": "Insufficient or mismatched data points."}
        
    kappa = cohen_kappa_score(annotator1_scores, annotator2_scores)
    return {
        "kappa": kappa,
        "meets_target": kappa > 0.60
    }

def generate_ablation_report(nlp_only_scores, llm_only_scores, full_pipeline_scores, human_ground_truth):
    """
    Compares the 3 system variants against ground truth using Pearson r.
    """
    nlp_eval = evaluate_metrics(human_ground_truth, nlp_only_scores)
    llm_eval = evaluate_metrics(human_ground_truth, llm_only_scores)
    full_eval = evaluate_metrics(human_ground_truth, full_pipeline_scores)
    
    return {
        "nlp_only_pearson_r": nlp_eval.get("pearson_r"),
        "llm_only_pearson_r": llm_eval.get("pearson_r"),
        "full_pipeline_pearson_r": full_eval.get("pearson_r"),
        "conclusion": "Full pipeline outperforms standalone variants." if 
            (full_eval.get("pearson_r", 0) > llm_eval.get("pearson_r", 0) and 
             full_eval.get("pearson_r", 0) > nlp_eval.get("pearson_r", 0)) else "Further tuning needed."
    }
