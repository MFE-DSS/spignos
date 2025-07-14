# test_llm.py
from spignosapi.llm.handler import LLMHandler

llm = LLMHandler()
response = llm.generate_response("Explique la différence entre une liste et un tuple en Python.")
print(response)
