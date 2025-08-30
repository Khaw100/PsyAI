class EducationAgent:
    def __init__(self, tools):
        self.retrieve_context = tools["retrieve_context"]

    def run(self, category):
        context_chunks = self.retrieve_context(category, purpose="education")
        if not context_chunks:
            # 🔹 Fallback cari berdasarkan nama folder
            all_docs = self.retrieve_context(category, k=20)  # ambil lebih banyak dulu
            filtered = [doc for doc in all_docs if category.lower() in doc.lower()]
            if filtered:
                context_chunks = filtered

        if not context_chunks:
            if category.lower() == "other":
                return {"education": "I could not find a specific category ..."}
            else:
                return {"education": f"Sorry, there is no educational information available for the category '{category}'."}

        education_text = "\n".join(context_chunks)
        return {"education": education_text}
