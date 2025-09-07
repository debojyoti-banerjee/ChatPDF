class ChatPDFError(Exception):   
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class PDFLoadError(ChatPDFError):
    def __init__(self, message: str, file_path: str = None):
        if file_path:
            message = f"[PDFLoadError] File: {file_path} | message: {message}"
        super().__init__(message)
        self.file_path = file_path


class ChromaDBError(ChatPDFError):
    def ___init__(self,message:str):
        super().__init__(f"[ChromaDBError] : {message}")


class ChatChainError(ChatPDFError):
    def __init__(self,message:str):
        super().__init__(f"[ChatChainError] message: {message}")