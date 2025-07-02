import requests
import gradio as gr

API_KEY = "past key"
MODEL = "mistralai/mistral-7b-instruct:free"

def check_symptoms(symptoms):
    prompt = f"""
You are a helpful AI assistant trained in general health and wellness.

The user reports the following symptoms: {symptoms}

Please respond in the following format with clear section headings:
1. **Possible Causes** – List 2 to 3 common causes of the symptoms.
2. **Lifestyle Advice** – Provide 2 helpful general tips for care or prevention.
3. **Suggested Medications** – Recommend common over-the-counter (OTC) medicines if applicable (like paracetamol, cough syrup, ORS, etc.).
4. **Disclaimer** – Add: "This is not medical advice. Please consult a doctor for proper diagnosis and treatment."

⚠️ Do NOT name rare or serious diseases. Keep tone simple, friendly, and educational.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} – {response.text}"

gr.Interface(
    fn=check_symptoms,
    inputs=gr.Textbox(label="Enter your symptoms (e.g., cough, fever, headache)", placeholder="fatigue, sore throat, dizziness"),
    outputs=gr.Textbox(label="AI Health Suggestions", lines=10),
    title="🩺 AI Symptom Checker (with Medication)",
    description="Get basic possible causes, home advice, and common medicine suggestions for your symptoms.\n\n❗This is not a real medical tool. Always consult a licensed doctor."
).launch()
