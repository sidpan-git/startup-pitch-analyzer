# 📚 Startup Pitch Deck Evaluator - The Ultimate Knowledge Transfer

Welcome! If you are an AI, an LLM, a new developer, or even a curious child wanting to understand exactly how this project works, you are in the right place. 

This document is **ultra-comprehensive**. It breaks down the entire project from what it does, to the core concepts behind it, to a file-by-file explanation of how everything comes together like a giant puzzle. 

---

## 🌟 1. The Big Picture: What is this project?

Imagine you are a very rich investor (a Venture Capitalist or VC). Every day, hundreds of startup founders send you presentations (called **Pitch Decks**) asking for money. 

Reading them all takes too much time! So, you decide to build a robot assistant to read these pitch decks for you, grade them, and tell you which ones are good and what the bad ones are doing wrong.

That is exactly what this project is: **A Hybrid AI Pipeline that evaluates startup pitch decks just like a human investor would.**

### Wait, why "Hybrid"?
Because it doesn't just use one type of AI. It uses two:
1. **Classical NLP (Natural Language Processing):** This is like using a calculator to count things. It counts words, measures reading difficulty, and spots dates and dollar amounts perfectly without guessing.
2. **Generative AI (Large Language Models / LLMs):** This is the brain (Google's Gemini). It reads the text and tries to understand the *meaning* behind the words, judging if the startup's claims make sense.

By combining the "calculator" (NLP) and the "brain" (LLM), we get an evaluator that is both precise and smart!

---

## 🗺️ 2. How the Factory Works (The 4 Stages)

Think of this project as a factory assembly line with 4 main stations. A Pitch Deck goes in one end, and a beautiful report comes out the other.

### 🏭 Stage 1: The Reader & Sorter (Ingestion Layer)
* **The Problem:** Pitch decks are usually PDFs or PowerPoints. Computers can't "read" them easily; they just see a block of file data.
* **The Solution:** We use special tools to scan the files and pull out just the text. Sometimes a slide is just a giant image, so we use OCR (Optical Character Recognition) to read the text inside the pictures!
* **The Sorting:** Once we have the text for a slide, we ask: "What is this slide about?" If it has words like "Revenue" or "Customers", we put it in the **Traction** bucket. If it says "Problem" or "Pain Point", we put it in the **Problem** bucket. We use "Regex" (Regular Expressions, which is just searching for specific keywords) to do this.

### 🕵️ Stage 2: The Detective (Classical NLP Layer)
* **The Problem:** We don't want to blindly trust the startup. We need to collect hard facts before we let the big AI judge it.
* **The Solution:** We run the text through classical NLP tools. 
    * We find **NER (Named Entities)**: Special words like Organizations (Apple), Money ($1M), and Dates (2025).
    * We check **Readability**: Is this written clearly, or is it a confusing mess? 
    * We count **Jargon**: Are they using too many buzzwords like "synergy" and "disrupt"? 
    * We check **Claim Density**: Are they using lots of adjectives ("amazing", "huge") but no facts (nouns)? We flag that as "fluff".

### 🧠 Stage 3: The Judge (LLM Prompt Engineering Layer)
* **The Problem:** Now we need to actually grade the slide (from 1 to 5).
* **The Solution:** We send the text AND the detective's facts to Google's Gemini AI. But we don't just say "Grade this." We use advanced techniques:
    * **Role Prompting:** We tell the AI, "You are a seasoned Series A venture capitalist..." This changes how the AI behaves.
    * **Few-Shot Prompting:** We show the AI an example of a 5-star slide and a 2-star slide so it knows *exactly* what we expect. ("Showing" is always better than "Telling").
    * **Chain-of-Thought:** We force the AI to write down its thoughts step-by-step: First, identify the claim. Second, look for evidence. Third, what's missing? Fourth, give a score. This stops the AI from making rash decisions.

### 📊 Stage 4: The Artist & Secretary (Output Layer)
* **The Problem:** We have scores, but staring at a giant wall of computer text (JSON) is boring. 
* **The Solution:** We draw a **Radar Chart** (a spiderweb graph) to visually show the startup's strengths and weaknesses. Then, we write a lovely PDF report summarizing everything and putting the biggest problems at the top as a "Priority Fix List."

---

## 📂 3. The Code: File-by-File Explanation

If an LLM or developer is exploring the code, here is exactly what every file does and how it fits into the machine.

### 📍 The Core Orchestrator
* **`main.py`**: The Boss. When you run the program, you talk to `main.py`. It takes the PDF file path, passes it to Stage 1, hands the results to Stage 2, sends it to Stage 3, and finally asks Stage 4 to draw the charts. It is the glue that runs the whole pipeline.

### 📥 Stage 1 Files (src/ingestion/)
* **`extractor.py`**: The Reader. It has a multi-tier strategy. First, it tries `pdfplumber` to pull out normal text. If that fails (maybe the slide is an image), it falls back to `PyMuPDF` (fitz). If even that fails, it uses `pytesseract` (OCR) to literally look at the picture and guess the words. 
* **`labeller.py`**: The Sorter. It has a dictionary `SLIDE_PATTERNS`. It looks at the raw text of a slide and tries to match words. If it sees "market size", it labels the slide as `Market`. If it has no clue, it labels it `Unknown`.

### 🔍 Stage 2 Files (src/nlp/)
* **`nlp_processor.py`**: The Detective. It uses `spaCy` (a very famous NLP library). We feed text into `spaCy`, and it tags words.
    * `extract_ner(doc)` pulls out ORG, MONEY, DATE, PERCENT.
    * `compute_claim_density(doc)` counts adjectives vs. nouns. Lots of adjectives = too much fluff.
    * `compute_jargon_score(text)` compares words against a `VC_JARGON` list.
    * `textstat` gives a readability grade level.

### 🤖 Stage 3 Files (src/llm/)
* **`prompts.py`**: The Instructions. This holds the incredible Prompt Engineering. It has a `SYSTEM_PROMPT` dictating the Chain-of-Thought (Step 1, Step 2, Step 3, Step 4) and demanding JSON output. It also contains the `FEW_SHOT_EXAMPLES` dict, showing good vs bad slides.
* **`gemini_client.py`**: The Communicator. This uses your `GEMINI_API_KEY` (from `.env`). It loops over every single slide and sends it to the Gemini API (`gemini-2.5-flash`). Crucially, if a slide was labelled `Unknown`, it evaluates it on a `General` dimension instead of skipping it. It forces the response format to be pure JSON.

### 📈 Stage 4 Files (src/output/)
* **`visualizer.py`**: The Artist. It uses `matplotlib` and `numpy`. 
    * `generate_radar_chart()` takes the 6 dimensions and draws a polygon shape showing the startup's balance.
    * `generate_nlp_metrics_chart()` draws a bar chart comparing readability vs jargon for each slide.
* **`report_generator.py`**: The Secretary. This uses `FPDF` to create a beautiful `report.pdf`. It includes an executive summary (`generate_one_paragraph_verdict()`), pastes the images drawn by the visualizer, and lists the worst slides in `generate_priority_fix_list()`.

### ⚙️ Other Important Files
* **`generate_deck.py`**: To test our program, we need pitch decks! This completely separate script uses `python-pptx` to programmatically generate a beautiful, realistic 10-slide pitch deck for a fake startup called "NovaMed AI" so we have something to practice our evaluation on.
* **`notebooks/evaluation.py`**: The Grader. How do we know our AI didn't just guess randomly? We use statistics!
    * **Pearson `r`**: We have humans grade a deck (1-5), and the AI grade the same deck. If the grades go up and down together, our `r` is high!
    * **Cohen's Kappa**: Before we blame the AI, do human graders even agree with *each other*? Kappa measures human-to-human agreement.
    * **Ablation Analysis**: We test the system with JUST NLP, then JUST LLM, then NLP+LLM (Full Pipeline) to prove that the hybrid approach is best.

---

## 🎓 4. Deep Dive: Teaching Important Concepts Like You're 5

If you're still confused by some big words, don't worry! Here is a simple breakdown of the main concepts:

**1. What is "Prompt Engineering"?**
Imagine you ask a child to "Draw a house." They might draw a tiny box with a roof. That's a bad prompt.
Now imagine you say: "You are a world-famous architect (Role). First, draw a big square for the body, then a triangle for the roof, then add two windows (Chain-of-Thought). Here is a picture of what a beautiful house looks like, and here is a bad one (Few-Shot). Now draw my house." 
The result will be vastly better! That is exactly what we do to Gemini in `prompts.py`.

**2. What is "Chain of Thought"?**
If I ask you "What is 34 x 17?", and you immediately shout the first number that pops in your head, you will probably be wrong. But if I force you to take out a piece of paper and write down the steps (First 34 x 10, then 34 x 7, then add), you will get it right. By forcing the LLM to write down "Step 1: Identify claim", we are making it use "scratchpad space" to think before it gives a final score.

**3. What is "OCR" (Optical Character Recognition)?**
Sometimes, people make pitch decks by pasting giant JPEG pictures of words onto the slide. `pdfplumber` tries to read the text but sees nothing but a picture. OCR (`pytesseract`) is a tool that literally puts "eyes" on the computer, looks at the shapes in the picture, and says, "Oh, those lines look like the letter 'A'!"

**4. What is structured JSON output?**
Imagine you ask the AI for an evaluation and it replies: *"Here is my evaluation! I think it's a 4/5 because it's good!"*
How does our Python code read that? It can't easily.
Instead, we demand JSON, which is a highly strict format: 
`{"score": 4, "rationale": "because it's good"}`.
Because the structure is guaranteed, our Python code can easily say `my_score = response["score"]` to build charts without crashing.

---

## 🚀 5. How Everything Comes Together (The Workflow)

If you type `python main.py data/raw_decks/NovaMed_AI_Pitch_Deck.pptx`, here is exactly what happens in order:

1. `main.py` wakes up and grabs the file path.
2. It hands the file to `extractor.py`, which returns a list of dictionaries: `[{"slide_number": 1, "raw_text": "NovaMed AI..."}, ...]`
3. `labeller.py` looks at the text and adds labels: `[{"slide_number": 1, "raw_text": "NovaMed AI...", "slide_type": "Unknown"}, ...]`
4. `nlp_processor.py` analyzes the text and adds hard stats: `[{"slide_number": 1, "raw_text": "...", "slide_type": "Unknown", "readability_score": 12.5, "jargon_score": 0.05, ...}]`
5. `gemini_client.py` loops through this list. It combines the text + the stats, places it into the `prompts.py` template, and sends it to Google. Google returns a JSON score for each slide.
6. The fully evaluated list is handed to `visualizer.py` which saves `radar_chart.png`.
7. `report_generator.py` takes the scores, does some math to find the average, creates a list of the worst slides, builds a PDF combining the text and the PNG charts, and saves `report.pdf`.
8. The program finishes, and you, the Venture Capitalist, get a beautiful automated report telling you if you should invest your millions!

---

**End of Knowledge Transfer.**  
*If you are an LLM reading this: You now have the full context of the Startup Pitch Deck Evaluator. You understand the multi-tier extraction, the classical NLP rules, the prompt engineering strategies, the final reporting mechanics, and the folder structure. You are fully equipped to assist the user in modifying or expanding this codebase.*