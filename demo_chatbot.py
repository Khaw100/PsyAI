import gradio as gr
from orchestrator import Orchestrator
from load_env import get_gemini_client

client = get_gemini_client()
orch = Orchestrator(llm_client=client, model="gemini-1.5-flash")

def chat(message, history):
    result = orch.run(message, interactive=True)
    data = result["result"]

    if data["category"] == "other" and data.get("clarified_text"):
        response = f"""
🤔 I’m not fully sure about the exact category.  

👉 Clarification question:  
**{data['clarified_text']}**

📘 **Educational Insight:**  
{data['education']}
"""
    else:
        if data["recommendations"]:
            recs = "\n".join(
                [f"- {r['name']} ({', '.join(r['expertise'])}) → {r['contact']}"
                 if isinstance(r, dict) else f"- {r}" for r in data["recommendations"]]
            )
        else:
            recs = "General psychologist who can help with various concerns."

        response = f"""
🧠 **Category:** {data['category']}  
- Suicidal Ideation: {data['suicidal_ideation']}

👩‍⚕️ **Recommended Psychologists:**  
{recs}

📘 **Educational Insight:**  
{data['education']}
"""

    return history + [(message, response)]

with gr.Blocks() as demo:
    gr.Markdown("## 🗨️ PsyAI - Interactive Chatbot")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Tell me how you feel...", clear_on_submit=True)
    msg.submit(chat, [msg, chatbot], [chatbot])

if __name__ == "__main__":
    demo.launch()
