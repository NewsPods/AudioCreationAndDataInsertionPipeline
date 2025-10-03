import os
from google.cloud import aiplatform  # for Vertex AI / Gen AI
from google.generativeai import generativeai  # or the Google Gen AI SDK
# (install with `pip install google-generativeai`)

def setup_google_api():
    # Set your Google credentials and project info
    # You can authenticate via GOOGLE_APPLICATION_CREDENTIALS env var (path to JSON key file)
    # Or via default ADC if running inside GCP.
    project_id = "YOUR_PROJECT_ID"
    location = "YOUR_MODEL_LOCATION"  # e.g. "us-central1" or "asia-south1", etc.
    generativeai.init(project=project_id, location=location)
    return project_id, location

def build_prompt(article_text: str,
                 voice1: str = "en-IN-NeerjaNeural",
                 voice2: str = "en-IN-PrabhatNeural",
                 pacing: str = "normal") -> str:
    """
    Build a system + user prompt to ask the LLM to produce ONLY the SSML content for double speakers.
    """
    prompt = f"""
You are a generator that converts news articles into **SSML** for **two speakers** in a podcast style.  
Your output should be only valid SSML (no explanation, no commentary).  

- The SSML should alternate between two voices: `{voice1}` and `{voice2}`.  
- Use expressive tags such as `<emphasis>`, `<prosody>`, `<break>`, and, if supported, `mstts:express-as` to improve naturalness.  
- Insert short pauses (e.g. 200-500 ms) between sentences and longer pauses (500-800 ms) between sections.  
- Use relative pacing (fast / medium / slow) via `<prosody rate="...">` tags, consistent with the `pacing` parameter.  
- Do not include any text outside the `<speak> … </speak>` tags.  
- Do not wrap the SSML in markdown or code fences.

Here is the article:

\"\"\"{article_text}\"\"\"

Generate the SSML with two speakers and stylistic elements.
"""
    return prompt

def call_llm_to_ssml(prompt: str) -> str:
    """
    Call the Google generative model API to produce SSML.  
    Returns the SSML string.
    """
    response = generativeai.chat.create(
        model="models/text-bison-001",  # or your chosen model
        prompt=prompt,
        temperature=0.2,
        top_p=0.9,
        candidate_count=1
    )
    # The response may contain text; we assume the first candidate is SSML
    # The returned response might have `response["candidates"][0]["output"]`
    ssml = response.candidates[0].output.strip()
    return ssml

def article_to_double_ssml(article: str,
                           voice1: str = "en-IN-NeerjaNeural",
                           voice2: str = "en-IN-PrabhatNeural",
                           pacing: str = "normal") -> str:
    prompt = build_prompt(article, voice1, voice2, pacing)
    ssml = call_llm_to_ssml(prompt)
    return ssml

if __name__ == "__main__":
    project, location = setup_google_api()
    # Example article (you can replace with your input)
    sample_article = """
India's democracy is under threat, according to Congress leader Rahul Gandhi, who accused the BJP-led central government ...
[rest of article here]
"""
    ssml_output = article_to_double_ssml(sample_article,
                                         voice1="en-IN-NeerjaNeural",
                                         voice2="en-IN-PrabhatNeural",
                                         pacing="normal")
    print(ssml_output)
