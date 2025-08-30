import json

class ClarificationAgent:
    def __init__(self, llm_client, model):
        self.llm = llm_client
        self.model = model
        self.prompt = None

    def run(self, user_text):
        self.prompt = f"""
        You are a clarification agent in a psychological triage system.
        The user's input may be vague, ambiguous, or lacking detail.

        Your job is to ask a gentle, specific follow-up question to clarify their concern.
        Do not classify or diagnose—just ask a question that helps the user express themselves more clearly.

        User input: "{user_text}"

        Respond in JSON:
        {{
          "thought": "Why clarification is needed",
          "follow_up": "Your clarifying question"
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
            return {
                "thought": "Failed to parse response. Defaulting to generic clarification.",
                "follow_up": "Boleh ceritakan lebih detail tentang apa yang kamu rasakan akhir-akhir ini?"
            }
