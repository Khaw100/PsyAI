# 🧠 PsyAI: Mental Health Knowledge Assistant

PsyAI is an **LLM-powered assistant** for mental health support and education.  
It retrieves curated educational information about mental health topics and can also match users with psychologists based on their expertise.  

This project was developed as part of the **OpenAI LLM Challenge**.

---

## ✨ Features
- 📘 **Education Agent** – Retrieves mental health educational material from a curated knowledge base.  
- 👩‍⚕️ **Psychologist Matcher** – Suggests psychologists by category (e.g., anxiety, depression, trauma).  
- 📂 **Vector Pipeline** – Uses **FAISS** and **SentenceTransformers embeddings** to index and retrieve documents.  
- 🔧 **Tool Initializer** – Centralized setup for tools and agents.  

---

## 📂 Project Structure
PsyAI/
│
├── agents/ # LLM agents
│ ├── educationAgent.py
│ ├── classificationAgent.py
│ └── clarificationAgent.py
│
├── knowledge-base/ # Curated text files (mental health topics)
│ ├── depression/depression_information.txt
│ ├── anxiety/anxiety_information.txt
│ └── ...
│
├── tools/ # Core utilities
│ ├── psychologistMatcher.py
│ ├── toolInitializer.py
│ └── vectorPipeline.py
│
├── mental_health_index/ # Auto-generated FAISS index (ignored in git)
├── psychologist_data.json # Psychologist info (ignored in git)
├── temp.py # Entry point for testing
├── requirements.txt
├── README.md
└── .gitignore

---

## 🚀 Getting Started

### 1. Clone Repo
git clone https://github.com/<your-username>/PsyAI.git
cd PsyAI

### 2. Create Virtual Environment
python -m venv psyai
psyai\Scripts\activate    # Windows PowerShell
# or
source psyai/bin/activate # Linux/Mac

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run Example


