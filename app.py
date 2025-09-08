import streamlit as st
from core.pdf_loader import PDFLoaderManager
from core.chroma_db import ChromaDBManager
from core.chat_chain import ChatBotManager
import os
st.title("ChatPDF")

upload_files=st.file_uploader("Upload PDFs",accept_multiple_files=True,type="pdf")

if upload_files:
    loader=PDFLoaderManager()
    pdf_paths=[]
    os.makedirs("temp", exist_ok=True)
    for file in upload_files:
        path=f"temp/{file.name}"
        with open(path,"wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(path)
        
    docs=loader.load_pdf(pdf_paths)
    chroma_mgr=ChromaDBManager()
    chroma_mgr.build_database()
    chroma_mgr.add_documents(docs)
    retriever=chroma_mgr.get_retriever()
    chatbot=ChatBotManager(retriever)
    query=st.text_input("Ask a question about your PDF")
    if query:
        answer=chatbot.ask_question(query)
        st.text_area("Answer",answer,height=200)
    