import os
import glob
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class VectorPipeline:
    def __init__(self, data_folder="knowledge-base", index_path="mental_health_index"):
        self.data_folder = data_folder
        self.index_path = index_path
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = None
        self.documents = None

    def load_data(self):
        folders = glob.glob(f"{self.data_folder}/*")
        text_loader_kwargs = {'encoding': 'utf-8'}
        documents = []
    
        for folder in folders:
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(folder, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
            folder_docs = loader.load()
    
            for doc in folder_docs:
                filename = os.path.basename(doc.metadata["source"])
                if "sample" in filename or "example" in filename:
                    doc.metadata["purpose"] = "classification"
                elif "info" in filename or "explanation" in filename or "information" in filename:
                    doc.metadata["purpose"] = "education"
                else:
                    doc.metadata["purpose"] = "general"
    
                doc.metadata["doc_type"] = doc_type
                documents.append(doc)
    
        print(f"Loaded {len(documents)} documents")
        return documents


    def create_or_update_index(self):
        self.documents = self.load_data()
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        split_docs = splitter.split_documents(self.documents)
        print(f"Number of split docs: {len(split_docs)}")

        if os.path.exists(self.index_path):
            print("🔄 Updating existing index...")
            self.vectorstore = FAISS.load_local(self.index_path, self.embedding_model, allow_dangerous_deserialization = True)
            self.vectorstore.add_documents(split_docs)
        else:
            print("🆕 Creating new index...")
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding_model)

        self.vectorstore.save_local(self.index_path)

    def load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index not found at {self.index_path}")
        self.vectorstore = FAISS.load_local(self.index_path, self.embedding_model, allow_dangerous_deserialization = True)

    def retrieve_context(self, query: str, k: int = 3, purpose: str = None):
        if not self.vectorstore:
            self.load_index()
        results = self.vectorstore.similarity_search(query, k=k)
        if purpose:
            results = [doc for doc in results if doc.metadata.get("purpose") == purpose]
        return [doc.page_content for doc in results]

