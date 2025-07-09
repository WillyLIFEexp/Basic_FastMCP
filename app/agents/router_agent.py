from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from app.agents.english_agent import VocabAgentTool
from app.core.config import settings

router_llm = ChatOpenAI(
    temperature=0,
    model="gpt-4.1-mini",
    api_key=settings.OPENAI_API_KEY
)

tools = [VocabAgentTool()]

router_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是智慧的語言學習助教，請根據問題選擇合適的工具。\n\n"
     "你有以下工具可以使用：\n"
     "{tools}\n\n"
     "工具名稱為：{tool_names}\n\n"
     "請按照以下步驟進行：\n"
     "Thought: 你應該如何選擇工具？\n"
     "Action: 工具名稱\n"
     "Action Input: 工具輸入\n"
     "Observation: 工具回傳結果\n"
     "Final Answer: 最終回覆給使用者的答案"),
    ("human", "問題：{input}"),
    ("ai", "{agent_scratchpad}")
])

router_agent = create_react_agent(
    llm=router_llm,
    tools=tools,
    prompt=router_prompt
)

router_executor = AgentExecutor(agent=router_agent, tools=tools, verbose=True)

def run_router(query: str) -> str:
    return router_executor.invoke({"input": query})["output"]
