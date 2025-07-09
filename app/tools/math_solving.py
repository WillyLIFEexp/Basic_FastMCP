from langchain_core.tools import StructuredTool
from app.chains.math_chain import MathChain

def explain_math(question: str) -> str:
    chain = MathChain()
    return chain.run(question)

math_solver_tool = StructuredTool.from_function(
    func=explain_math,
    name="MathSolverTool",
    description="解答數學題目並且回傳答案與解釋, 輸入必須有'question'"
)