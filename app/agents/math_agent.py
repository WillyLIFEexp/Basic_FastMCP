from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,ChatMessagePromptTemplate
from app.tools.math_solving import math_solver_tool
from app.core.config import settings

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4.1-mini",
    api_key=settings.OPENAI_API_KEY
)

tools = [math_solver_tool]

math_agent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是數學專家，根據問題使用合適的工具回答。\n\n"
     "你有以下工具可用：\n"
     "{tools}\n\n"
     "工具名稱為：{tool_names}\n"
     "請按以下格式進行：\n\n"
     "Thought: 思考如何行動\n"
     "Action: 選擇工具名稱\n"
     "Action Input: 工具輸入\n"
     "Observation: 工具回傳結果\n"
     "Final Answer: 最終回答"),

    ("human", "問題：{input}"),

    ("ai", "{agent_scratchpad}")
])

math_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=math_agent_prompt
)

math_executor = AgentExecutor(agent=math_agent, tools=tools, verbose=True)

class MathAgentTool(BaseTool):
    name: str = "math_agent"
    description: str = "用來處理數學相關的問題，例如：**代數(algebra)**、**方程式(equation)**、**微積分(calculus)**、**幾何(geometry)**或**加減乘除(arithmetic)**計算。"

    def _run(self, query: str) -> str:
        return math_executor.invoke({"input": query})["output"]