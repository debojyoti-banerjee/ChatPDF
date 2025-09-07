from core.pdf_loader import PDFLoaderManager
from core.exceptions import PDFLoadError
from core.chroma_db import ChromaDBManager
from core.exceptions import ChromaDBError
from core.exceptions import ChatChainError
from core.chat_chain import ChatBotManager

loader=PDFLoaderManager()

try:
    docs=loader.load_pdf(["tests\Btech_Project.pdf"])
    chroma_mgr=ChromaDBManager()
    chroma_mgr.build_database()
    chroma_mgr.add_documents(docs)
    retriever=chroma_mgr.get_retriever()
    chatbot=ChatBotManager(retriever)
    print(chatbot.ask_question("what is hurst exponent"))
    
except PDFLoadError as e:
    print(e.message)
except ChromaDBError as e:
    print(e.message)
except ChatChainError as e:
    print(e.message)
except Exception as e:
    print(e)
