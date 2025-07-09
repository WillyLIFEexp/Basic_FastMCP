from langchain_core.tools import StructuredTool
from app.chains.vocab_chain import VocabChain

def explain_vocab(word: str) -> str:
    chain = VocabChain()
    return chain.run(word)

vocab_lookup_tool = StructuredTool.from_function(
    func=explain_vocab,
    name="ExplainVocab",
    description="輸入英文單字，回傳單字意思。"
)
