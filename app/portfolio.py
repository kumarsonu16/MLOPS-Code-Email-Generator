import pandas as pd
import chromadb
import uuid
import os


class Portfolio:
    def __init__(self, file_path="./resource/my_portfolio.csv"):
        # Get the absolute path of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Correct file path inside the Docker container
        file_path = os.path.join(base_dir, "resource", "my_portfolio.csv")
        
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
