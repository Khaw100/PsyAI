import json
from agents.clarificationAgent import ClarificationAgent
from agents.classificationAgent import ClassificationAgent
from agents.educationAgent import EducationAgent
from tools.toolInitializer import ToolInitializer

class Orchestrator:
    def __init__(self, llm_client=None, model="gemini-1.5-flash"):
        tools = ToolInitializer().setup()
        self.agents = {
            "classify": ClassificationAgent(llm_client, tools, model),
            "educate": EducationAgent(tools),
            "clarify": ClarificationAgent(llm_client, model),
        }
        self.tools = tools

    def run(self, user_text, interactive: bool = False):
        """Main orchestration function.
        - interactive=False → simple 1x input (skip clarification)
        - interactive=True → chatbot mode (clarify + reclassify if needed)
        """
        classification = self.agents["classify"].run(user_text)
        category = classification.get("category", "other")
        suicidal = classification.get("suicidal_ideation", "No")
        context_chunks = classification.get("context", [])

        if category != "other":
            thought = "Category identified. Proceeding with recommendation and education."
            recommended = self.tools["match_psychologist"](category)
            education = self.agents["educate"].run(category)

            result = {
                "category": category,
                "context": context_chunks,
                "recommendations": recommended,
                "education": education["education"],
                "clarified": False,
                "suicidal_ideation": suicidal
            }

        else:
            if interactive:
                # Chatbot mode (ask clarification)
                clarification = self.agents["clarify"].run(user_text)
                clarified_text = clarification["follow_up"]

                # Re-run classification on clarified text
                reclassification = self.agents["classify"].run(clarified_text)
                new_category = reclassification.get("category", "other")
                suicidal = reclassification.get("suicidal_ideation", "No")
                context_chunks = reclassification.get("context", [])

                if new_category != "other":
                    thought = "Clarified input classified. Proceeding with recommendation and education."
                    recommended = self.tools["match_psychologist"](new_category)
                    education = self.agents["educate"].run(new_category)

                    result = {
                        "category": new_category,
                        "context": context_chunks,
                        "recommendations": recommended,
                        "education": education["education"],
                        "clarified": True,
                        "suicidal_ideation": suicidal,
                        "clarified_text": clarified_text
                    }
                else:
                    thought = "Still unclear after clarification. Providing general support." 
                    result = { 
                        "category": "other",
                        "context": [],
                        "recommendations": [],
                        "education": (
                            "I could not find a specific category for what you're feeling. "
                            "That's completely okay — your experience is still valid. "
                            "Talking directly to a psychologist may help you explore it further."
                        ), 
                        "clarified": True,
                        "suicidal_ideation": suicidal,
                        "clarified_text": clarified_text
                    }
            else:
                # Simple mode (fallback directly)
                thought = "Input unclear. Providing general support." 
                result = {
                    "category": "other",
                    "context": [],
                    "recommendations": [],
                    "education": (
                        "I could not find a specific category for what you're feeling. "
                        "That's completely okay — your experience is still valid. "
                        "Talking directly to a psychologist may help you explore it further."
                    ), 
                    "clarified": False,
                    "suicidal_ideation": suicidal
                }

        return {
            "thought": thought,
            "result": result
        }
