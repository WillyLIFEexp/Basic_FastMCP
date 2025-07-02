# app/chains/base_chain.py
from langchain_openai import ChatOpenAI
from app.core.config import settings
import os

class BaseChain:
    def __init__(self):
        # shared LLM config
        # prompt = ReActPrompt.to_langchain_prompt(tools)
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4.1-mini",
            api_key=settings.OPENAI_API_KEY
        )