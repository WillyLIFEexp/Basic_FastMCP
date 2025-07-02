from langchain.agents import create_react_agent, AgentExecutor
# from langchain.agents.react.base import ReActPompt
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from app.tools.math_solving import math_solver_tool
from app.core.config import settings

# prompt = ReActPrompt.to_langchain_prompt(tools)
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4.1-mini",
    api_key=settings.OPENAI_API_KEY
)

math_agent_executor = initialize_agent(
    tools=[math_solver_tool],
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 4. Expose agent runner
async def run_math_agent(user_question: str) -> str:
    return await math_agent_executor.arun(user_question)