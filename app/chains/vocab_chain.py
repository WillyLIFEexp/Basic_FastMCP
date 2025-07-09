from langchain_core.prompts.chat import ChatPromptTemplate
from app.chains.base_chain import BaseChain

class VocabChain(BaseChain):
    def __init__(self):
        super().__init__()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一個英文單字助教。請根據問題給出該單字的意思。"),
            ("human", "請解釋這個單字：{word}")
        ])

        self.chain = self.prompt | self.llm

    def run(self, word: str) -> str:
        return self.chain.invoke({"word": word}).content
