import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# API endpoint
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Master prompt (from your idea)
MASTER_PROMPT = """
You are an expert electronics project assistant for students.
Your job is to analyze a given input (YouTube link, image description, or project idea)
and generate a detailed, structured output in JSON.

Follow this structure:

{
  "project_name": "...",
  "overview": "...",
  "real_life_applications": ["...", "...", "..."],
  "components": [
    {"name": "...", "specifications": "..."}
  ],
  "procedure": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "pin_diagram": "Describe the pin/circuit clearly",
  "future_aspects": ["...", "..."]
}
"""

def get_openrouter_response(user_input, model="meta-llama/llama-3-8b-instruct"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": MASTER_PROMPT},
            {"role": "user", "content": user_input},
        ],
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {e}"

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Electronics Project Assistant", layout="wide")

st.title("⚡ Electronics Project Assistant")
st.write("Enter a YouTube link, image description, or project idea and get a structured project report.")

user_input = st.text_area("🔗 Enter Project Idea / Link / Description:", height=150)

model_choice = st.selectbox(
    "Select Model:",
    ["meta-llama/llama-3-8b-instruct", "mistralai/mixtral-8x7b-instruct", "google/gemma-7b-it"]
)

if st.button("Generate Project Report"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some input first.")
    else:
        with st.spinner("Generating project details..."):
            output = get_openrouter_response(user_input, model_choice)
            st.success("✅ Project Report Generated!")
            st.code(output, language="json")
