from langchain_core.prompts.chat import ChatPromptTemplate
from app.chains.base_chain import BaseChain

class MathChain(BaseChain):
    def __init__(self):
        super().__init__() 

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一個數學專家，請根據問題解答數學問題且只回傳最後答案與解法."),
            ("human", "請計算這個數學問題：{math_question}")
        ])

        self.chain = self.prompt | self.llm

    def run(self, question: str) -> str:
        return self.chain.invoke({"math_question": question}).content
