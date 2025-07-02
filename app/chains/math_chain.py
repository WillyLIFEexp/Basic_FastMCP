from langchain_core.prompts.chat import ChatPromptTemplate
from app.chains.base_chain import BaseChain

class MathChain(BaseChain):
    def __init__(self):
        super().__init__()  # initialize shared llm

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a world-class math assistant. You solve math equations and return only the final answer."),
            ("human", "Question: {math_question}")
        ])

        self.chain = self.prompt | self.llm

    def run(self, question: str) -> str:
        return self.chain.invoke({"math_question": question}).content

    async def arun(self, question: str) -> str:
        result = await self.chain.ainvoke({"math_question": question})
        return result.content 