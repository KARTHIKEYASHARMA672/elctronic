import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not set in .env file.")
else:
    genai.configure(api_key=API_KEY)

# -------------------------------
# Master Prompt Template
# -------------------------------
MASTER_PROMPT = """
You are an expert electronics project assistant for students.
Your job is to analyze a given input (which can be a YouTube link transcript, an image description, or manual project idea)
and generate a detailed, structured output for a student project report.

Follow this exact structure in your response (always return JSON format):

{
  "project_name": "Clear title of the project",
  "overview": "Short explanation of what the project is and why it is useful.",
  "real_life_applications": [
    "List of at least 3 real-world applications where this project is useful."
  ],
  "components": [
    {
      "name": "Component name",
      "specifications": "Important technical details like voltage, current, memory, etc."
    }
  ],
  "procedure": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ...",
    "Provide at least 5 detailed steps to build the project."
  ],
  "pin_diagram": "Describe a clean circuit or pin diagram in detail so it can be drawn later.",
  "future_aspects": [
    "List at least 2-3 possible improvements or future upgrades for this project."
  ]
}

Rules:
1. Always return valid JSON format only.
2. Be concise but informative (like a student project report).
3. Use clear technical terms for components and specs.
4. If the input is unclear, make logical assumptions and still provide a complete output.
"""

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Electronics Project Assistant", layout="wide")
st.title("🤖 Electronics Project Assistant (Gemini AI)")

st.write("Enter a **YouTube link** or **manual description** of a project idea:")

# Input type selection
input_type = st.radio("Choose input type:", ["YouTube Link", "Manual Text"])

user_input = ""
if input_type == "YouTube Link":
    user_input = st.text_input("Paste YouTube video link here:")
elif input_type == "Manual Text":
    user_input = st.text_area("Enter project description here:")

# Process button
if st.button("Generate Project Report") and user_input.strip() != "":
    with st.spinner("Generating project details using Gemini..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")

            prompt = MASTER_PROMPT + f"\n\nStudent Input: {user_input}\n\nRespond in JSON only."

            response = model.generate_content(prompt)
            result_text = response.text.strip()

            # Try parsing JSON
            try:
                result_json = json.loads(result_text)
            except:
                # Try extracting valid JSON substring
                start = result_text.find("{")
                end = result_text.rfind("}")
                if start != -1 and end != -1:
                    result_json = json.loads(result_text[start:end+1])
                else:
                    result_json = {"error": "Invalid JSON from Gemini", "raw_output": result_text}

            # Display neatly
            st.subheader("📌 Project Report")
            st.json(result_json, expanded=True)

            # Download button
            st.download_button(
                label="📥 Download JSON",
                data=json.dumps(result_json, indent=4),
                file_name="project_report.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
