# temp.py
from tools.toolInitializer import ToolInitializer
from agents.educationAgent import EducationAgent

if __name__ == "__main__":
    initializer = ToolInitializer(
        data_folder="knowledge-base",
        index_path="mental_health_index",
        psychologist_file="psychologist_data.json"
    )
    tools = initializer.setup()

    # 🔹 Debug: cek semua dokumen yg ke-load
    vp = initializer.vector_pipeline
    docs = vp.load_data()  # ini reload dokumen mentah sebelum split
    print("=== Documents Loaded ===")
    for d in docs:
        filename = d.metadata["source"]
        if "_infor" in filename.lower():   # filter khusus yg ada "infor"
            print(f"File: {filename}")
            print(f"Purpose: {d.metadata.get('purpose')}")
            print("--- Preview ---")
            print(d.page_content[:300], "...\n")

    # 🔹 Cek EducationAgent
    edu_agent = EducationAgent(tools)
    category = "depression"
    result = edu_agent.run(category)
    print("\n📘 Education Result:")
    print(result["education"])
