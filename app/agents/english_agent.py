from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.tools.vocab_tool import vocab_lookup_tool
from app.core.config import settings

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4.1-mini",
    api_key=settings.OPENAI_API_KEY
)

tools = [vocab_lookup_tool]

vocab_agent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是英文單字助教，根據問題使用合適的工具回答。\n\n"
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

vocab_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=vocab_agent_prompt
)

vocab_executor = AgentExecutor(agent=vocab_agent, tools=tools, verbose=True)

class VocabAgentTool(BaseTool):
    name: str = "vocab_agent"
    description: str = "查英文單字意思的智慧助教"

    def _run(self, query: str) -> str:
        return vocab_executor.invoke({"input": query})["output"]
