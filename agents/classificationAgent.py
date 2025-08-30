import json
class ClassificationAgent:
    def __init__(self, llm_client, tools, model):
        self.llm = llm_client
        self.tools = tools
        self.model = model
        self.context = None
        self.prompt = None

    def run(self, user_text):
        context_chunks = self.tools["retrieve_context"](user_text, purpose="classification")
        self.context = "\n".join(context_chunks)

        self.prompt = f"""
        You are a psychological classification agent.
        
        Your task is to classify the user's emotional state based on the context provided.
        Choose the closest category available in the context list below. 
        If the input is completely unrelated, return:
        {{ "category": "other", "suicidal_ideation": "No" }}
                
        User input:
        "{user_text}"
        
        Relevant context:
        {self.context}
        
        Respond in JSON format:
        {{
          "category": "...",  // must match one of the categories in context or be "other"
          "suicidal_ideation": "Yes" or "No"
        }}
        """


        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}],
            temperature=0.3,
            max_tokens=150
        )

        try:
            output_text = response.choices[0].message.content
            cleaned = output_text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except:
            return {"category": "other", "suicidal_ideation": "No"}
