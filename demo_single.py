import gradio as gr
from orchestrator import Orchestrator
from load_env import get_gemini_client, get_openai_client

client = get_gemini_client()

orch = Orchestrator(llm_client=client, model="gemini-1.5-flash")

def analyze_user_input(user_text):
    result = orch.run(user_text, interactive=False)["result"]

    response = f"""
        # 🧠 PsyAI - Analysis Report

        **Category:** {result['category']}  
        **Suicidal Ideation:** {result['suicidal_ideation']}  

        ---

        👩‍⚕️ **Recommended Psychologists:**  
        {result['recommendations'] if result['recommendations'] else "General psychologist who can help with various concerns."}

        ---

        📘 **Educational Insight:**  
        {result['education']}
    """
    return response

demo = gr.Interface(
    fn=analyze_user_input,
    inputs=gr.Textbox(placeholder="Tell me how you feel...", lines=3),
    outputs=gr.Markdown(),
    title="PsyAI - Quick Mental Health Analysis",
    description="Enter your feelings in a sentence or two. PsyAI will analyze, classify, recommend psychologists, and provide helpful education."
    )

if __name__ == "__main__":
    demo.launch()
