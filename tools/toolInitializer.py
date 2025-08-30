import os
from tools.psychologistMatcher import PsychologistMatcher
from tools.vectorPipeline import VectorPipeline


class ToolInitializer:
    def __init__(
        self,
        data_folder="knowledge-base",
        index_path="mental_health_index",
        psychologist_file="psychologist_data.json"
        ):
        self.vector_pipeline = VectorPipeline(
            data_folder=data_folder,
            index_path=index_path
        )
        self.matcher = PsychologistMatcher(filepath=psychologist_file)

    def setup(self, create_index_if_missing=True):
        if os.path.exists(self.vector_pipeline.index_path):
            self.vector_pipeline.load_index()
        elif create_index_if_missing:
            self.vector_pipeline.create_or_update_index()
        else:
            raise FileNotFoundError("Index not found and create_index_if_missing=False")

        return {
            "retrieve_context": self.vector_pipeline.retrieve_context,
            "match_psychologist": self.matcher.match_by_category
        }
