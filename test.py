import unittest
from orchestrator import Orchestrator
from load_env import get_openai_client, get_gemini_client
from tools.vectorPipeline import VectorPipeline

class TestPsyAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # init Orchestrator sekali sebelum semua test
        client = get_gemini_client()
        cls.orch = Orchestrator(llm_client=client, model="gemini-1.5-flash")

    def test_classification_depression(self):
        result = self.orch.run("I feel sad and hopeless", interactive=False)["result"]
        self.assertIn(result["category"], ["depression", "other"])
        print("\n[Depression Test] =>", result)

    def test_classification_anxiety(self):
        result = self.orch.run("I’m nervous and can't sleep before exams", interactive=False)["result"]
        self.assertIn(result["category"], ["anxiety", "other"])
        print("\n[Anxiety Test] =>", result)

    def test_fallback_clarification(self):
        result = self.orch.run("blabla random text", interactive=True)["result"]
        # boleh other kalau ga jelas
        self.assertIn(result["category"], ["other", "mental health basics"])
        print("\n[Clarification Test] =>", result)

    def test_psychologist_matcher(self):
        from tools.psychologistMatcher import PsychologistMatcher
        matcher = PsychologistMatcher(filepath="psychologist.json")
        matches = matcher.match("anxiety")
        self.assertIsInstance(matches, list)
        print("\n[Psychologist Match Test] =>", matches)

    def test_vector_db_not_empty(self):
        vp = VectorPipeline(data_folder="../knowledge-base", index_path="mental_health_index")

        # pastikan index sudah ada atau bikin baru
        try:
            vp.load_index()
        except FileNotFoundError:
            vp.create_or_update_index()

        # ambil contoh query
        results = vp.retrieve_context("depression", k=2)

        # test hasil tidak kosong
        self.assertGreater(len(results), 0, "VectorDB should return at least 1 document")
        print("\n[VectorDB Test] =>", results)

if __name__ == "__main__":
    unittest.main()
