import json
import os

class PsychologistMatcher:
    def __init__(self, filepath="psychologist_data.json"):
        self.filepath = filepath
        self.psychologists = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ File {self.filepath} not found. Using empty psychologist list.")
            return []

    def match_by_category(self, category):
        category = category.lower()
        matches = [
            p for p in self.psychologists
            if category in [e.lower() for e in p.get("expertise", [])]
        ]
        if matches:
            return matches

        fallback = [
            p for p in self.psychologists
            if "general mental health" in [e.lower() for e in p.get("expertise", [])]
        ]

        if fallback:
            return fallback

        return [{
            "name": "No psychologist available",
            "expertise": [],
            "contact": "Currently no psychologist is available for this category."
        }]
