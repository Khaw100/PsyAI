import gradio as gr
from orchestrator import Orchestrator
import openai
from load_env import get_gemini_client, get_openai_client

client = get_gemini_client()

orch = Orchestrator(llm_client=client, model="gemini-1.5-flash")

def chat(message, history):
    result = orch.run(message, interactive=True)
    data = result["result"]

    if data["category"] == "other" and data.get("clarified_text"):
        response = (
            f"🤔 I’m still not sure about the exact category.\n\n"
            f"But here's a question to help us understand better:\n\n"
            f"👉 {data['clarified_text']}\n\n"
            f"📘 Educational Insight: {data['education']}"
        )
    else:
        response = f"""
            🧠 **Category:** {data['category']}  
            - Suicidal Ideation: {data['suicidal_ideation']}

            👩‍⚕️ **Recommended Psychologists:**  
            {data['recommendations'] if data['recommendations'] else "General psychologist who can help with various concerns."}

            📘 **Educational Insight:**  
            {data['education']}
        """

    return history + [(message, response)]

with gr.Blocks() as demo:
    gr.Markdown("## 🗨️ PsyAI - Interactive Chatbot")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Tell me how you feel...")
    msg.submit(chat, [msg, chatbot], [chatbot])

if __name__ == "__main__":
    demo.launch()
