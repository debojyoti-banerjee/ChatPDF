from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from core.exceptions import ChromaDBError
from dotenv import load_dotenv
load_dotenv()


class ChromaDBManager:
    def __init__(self,persist_dir="chromadb",collection_name="sample_1"):
        self.persist_dir=persist_dir
        self.embedding_model=HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
        self.db=None
        self.collection_name=collection_name
        
        
    def build_database(self):
        try:
            self.db=Chroma(embedding_function=self.embedding_model,persist_directory=self.persist_dir,collection_name=self.collection_name)
        except Exception as e:
            raise ChromaDBError(f"Failed to build Chroma Database | message: {e}")
    
    def add_documents(self,documents):
        if not self.db:
            raise ChromaDBError("Database not initialized hence document upload failed")
        try:
            self.db.add_documents(documents)
        except Exception as e:
            raise ChromaDBError(f"Failed to add documents | message: {str(e)}")
    
    def delete_documents(self,filter):
        if not self.db:
            raise ChromaDBError("Database not initialized hence document cant be deleted")
        try:
            self.db.delete(filter=filter)
        except Exception as e:
            raise ChromaDBError(f"Failed to delete documents {str(e)}")
        
    def get_retriever(self,k=6):
        if not self.db:
            raise ChromaDBError("Database not initialized")
        return self.db.as_retriever(search_kwargs={"k":k})