from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from core.exceptions import ChatChainError

load_dotenv()

class ChatBotManager:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = HuggingFaceEndpoint(
            repo_id="MiniMaxAI/MiniMax-M1-80k",
            task="text-generation",
            timeout=300
        )
        self.model = ChatHuggingFace(llm=self.llm)
        self.chat_history = ""  
        self.prompt = self._init_prompt()

    def _init_prompt(self):
        template = """
        You are a helpful assistant having a conversation with a human.

        Chat history:
        {chat_history}

        Relevant context from knowledge base:
        {context}

        User question:
        {question}

        Answer in a clear and concise way:
        """
        return PromptTemplate(template=template, input_variables=["chat_history", "context", "question"])

    def ask_question(self, query):
        if not query or not query.strip():
            return "Please enter a valid question"

        try:
            docs = self.retriever.invoke(query)
            context = "\n".join([d.page_content for d in docs])
            prompt_text = self.prompt.invoke({
                "chat_history": self.chat_history,
                "context": context,
                "question": query
            })
            
            response_obj = self.model.invoke(prompt_text)

            if hasattr(response_obj, "content"):
                response = response_obj.content
            else:
                response = str(response_obj)
            
            response=response.split("</think>")[-1].strip()
            self.chat_history += f"Human: {query}\nAI: {response}\n"

            return response

        except Exception as e:
            raise ChatChainError(f"Error during query execution: {str(e)}")
