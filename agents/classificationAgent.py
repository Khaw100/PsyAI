import json

class ClassificationAgent:
    def __init__(self, llm_client, tools, model):
        self.llm = llm_client
        self.tools = tools
        self.model = model
        self.context = None
        self.prompt = None

        self.valid_categories = [
            "depression",
            "anxiety",
            "stress",
            "trauma",
            "child_psychology",
            "relationship_issues",
            "work_burnout",
            "other"
        ]

    def run(self, user_text):
        context_chunks = self.tools["retrieve_context"](user_text, purpose="classification")

        examples = [c for c in context_chunks if "example" in c.lower()]
        info = [c for c in context_chunks if "example" not in c.lower()]

        examples_text = "\n".join(examples[:3]) if examples else "No examples available."
        info_text = "\n".join(info[:2]) if info else "No extra info available."

        self.prompt = f"""
You are a psychological classification agent.

Your task is to classify the user's emotional state into one of these categories:
{", ".join(self.valid_categories)}

If the input is unrelated, return exactly:
{{ "category": "other", "suicidal_ideation": "No" }}

Here are some examples from the knowledge base:
{examples_text}

User input:
"{user_text}"

Relevant info (if any):
{info_text}

Respond ONLY in valid JSON:
{{
  "category": "...",  
  "suicidal_ideation": "Yes" or "No"
}}
"""

        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": self.prompt}],
                temperature=0.2,
                max_tokens=150
            )

            output_text = response.choices[0].message.content
            cleaned = output_text.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)

            category = parsed.get("category", "other").lower()
            suicidal = parsed.get("suicidal_ideation", "No")

            if category not in self.valid_categories:
                category = "other"

            return {
                "category": category,
                "suicidal_ideation": suicidal,
                "context": context_chunks
            }

        except Exception as e:
            print(f"[ClassificationAgent ERROR] {e}")
            return {"category": "other", "suicidal_ideation": "No", "context": []}
