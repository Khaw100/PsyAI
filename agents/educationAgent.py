class EducationAgent:
    def __init__(self, tools):
        self.retrieve_context = tools["retrieve_context"]

    def run(self, category):
        # 🚫 Don't query vector DB if it's "other"
        print(category)
        if category.lower() == "other":
            return {
                "education": (
                    "I could not find a specific category for what you're feeling. "
                    "That's completely okay — your experience is still valid. "
                    "Talking directly to a psychologist may help you explore it further."
                )
            }

        # Normal retrieval for known categories
        context_chunks = self.retrieve_context(category, purpose="education")

        # Fallback: broader retrieval if empty
        if not context_chunks:
            all_docs = self.retrieve_context(category, k=3)
            filtered = [doc for doc in all_docs if category.lower() in doc.lower()]
            if filtered:
                context_chunks = filtered

        if not context_chunks:
            return {
                "education": (
                    f"Sorry, there is no educational information available for the category '{category}'."
                )
            }

        education_text = "\n".join(context_chunks)
        return {"education": education_text}
