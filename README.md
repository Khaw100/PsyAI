
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

```
PsyAI/
│
├── agents/                  # LLM agents
│   ├── educationAgent.py     # Retrieves educational content
│   ├── classificationAgent.py # Classifies user emotional state
│   └── clarificationAgent.py  # Asks follow-up questions for clarification
│
├── knowledge-base/           # Curated text files (mental health topics)
│   ├── depression/depression_information.txt  # Mental health data for depression
│   ├── anxiety/anxiety_information.txt      # Mental health data for anxiety
│   └── ...
│
├── tools/                    # Core utilities
│   ├── psychologistMatcher.py  # Matches psychologists based on user needs
│   ├── toolInitializer.py      # Centralized setup for tools and agents
│   └── vectorPipeline.py       # Handles the vector-based document search
│
├── mental_health_index/       # Auto-generated FAISS index (ignored in git)
├── psychologist_data.json     # Psychologist info (ignored in git)
├── temp.py                    # Entry point for testing
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore file
```

---

## 🚀 Getting Started

### 1. Clone Repo
```bash
git clone https://github.com/<your-username>/PsyAI.git
cd PsyAI
```

### 2. Create Virtual Environment
For **Windows**:
```bash
python -m venv psyai
.\psyai\Scripts\activate      # Activate the environment in PowerShell
```

For **Linux/Mac**:
```bash
python -m venv psyai
source psyai/bin/activate # Activate the environment in terminal
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Example
You can run the example chatbot or single input demo by executing the following commands:

- For the **Interactive Chatbot** (real-time conversation):
  ```bash
  python demo_chatbot.py
  ```

- For **Single Input Analysis** (quick mental health analysis):
  ```bash
  python demo_single.py
  ```

---

## ⚙️ Configuration

### LLM Client Configuration
PsyAI supports integration with various LLM clients. By default, it uses the **Gemini LLM**. To configure your client:

1. Create a `.env` file in the root directory of your project.
2. Set the `GEMINI_API_KEY` (or other LLM keys) in the `.env` file.

Example `.env` file:
```env
GEMINI_API_KEY=your-api-key-here 
```

---

## 🤝 Contributing

We welcome contributions to improve PsyAI!  
To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## 📝 Acknowledgments
- **OpenAI** – For the LLM models.
- **Gradio** – For the interface and quick demo setups.
- **Hugging Face** – For the SentenceTransformers embeddings.
