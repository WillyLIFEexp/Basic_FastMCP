from langchain_core.tools import StructuredTool
from app.chains.math_chain import MathChain

def solve(question: str) -> str:
    chain = MathChain()
    return chain.run(question)

math_solver_tool = StructuredTool.from_function(
    func=solve,
    name="MathSolverTool",
    description="Solves math problems and returns the answer. Input must include 'question'."
)