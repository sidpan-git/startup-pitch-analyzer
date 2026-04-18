# 🚀 Startup Pitch Deck Evaluator

A hybrid AI pipeline that evaluates startup pitch decks like a human Venture Capitalist. It combines classical Natural Language Processing (NLP) to extract hard facts, readablity, and jargon density, with Generative AI (LLMs) to understand context, business models, and evaluate the overall startup viability. 

For a complete breakdown of the architecture, please refer to [Knowledge_Transfer.md](Knowledge_Transfer.md).

## 🛠️ Prerequisites
- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## 💻 Setup Instructions

Follow these steps to set up the project locally:

### 1. Create a Virtual Environment

It is highly recommended to isolate the project dependencies using a virtual environment.

**Windows:**
```shell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```shell
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Project Dependencies

Install the required Python packages from the `requirements.txt` file.

```shell
pip install -r requirements.txt
```

### 3. Download the NLP Model

This project relies on `spaCy` for classical NLP processing. You need to download its English language model:

```shell
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables

The application needs access to the Google Gemini API. 

1. Create a file named `.env` in the root directory. You can copy the provided example:
   **Windows:**
   ```shell
   copy .env.example .env
   ```
   **macOS/Linux:**
   ```shell
   cp .env.example .env
   ```
2. Open the `.env` file and replace `YOUR_API_KEY` with your actual Google Gemini API Key.
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```

## 🚀 Running the Project

### 1. Generate a Sample Pitch Deck (Optional)
If you don't have a pitch deck to evaluate, you can programmatically generate a realistic 10-slide PowerPoint deck for a fake startup (`NovaMed AI`):

```shell
python generate_deck.py
```
*This will create a dummy presentation (e.g., `data/raw_decks/NovaMed_AI_Pitch_Deck.pptx`).*

### 2. Run the Evaluation Pipeline
Execute the main script and pass the path to the pitch deck you want to evaluate:

```shell
python main.py data/raw_decks/NovaMed_AI_Pitch_Deck.pptx
```

The pipeline will process the deck step-by-step through the extraction, classification, NLP analysis, and Gemini LLM evaluation phases. Once complete, it will generate a comprehensive PDF output report (`report.pdf`) and visualizations (e.g., `radar_chart.png`).
