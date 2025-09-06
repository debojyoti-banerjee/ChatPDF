from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.exceptions import PDFLoadError

class PDFLoaderManager:
    def __init__(self,chunk_size=1000,chunk_overlap=200):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
    def load_pdf(self,file_paths:list):
        all_docs=[]
        for path in file_paths:
            try:
                loader=PyPDFLoader(path)
                data=loader.load()
                splitter=RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)
                split_docs=splitter.split_documents(data)
                all_docs.extend(split_docs)
            except Exception as e:
                raise PDFLoadError(str(e), file_path=path)
        return all_docs