# spignosapi/llm/prompts/orchestrator.py

from spignosapi.llm.prompts.agents.tech_agent import TechCareerAgent
from spignosapi.llm.prompts.agents.udemy_agent import UdemyAgent


class Orchestrator:
    def __init__(self):
        self.tech_agent = TechCareerAgent()
        self.udemy_agent = UdemyAgent()

    def run(self, user_question):
        advice = self.tech_agent.analyze(user_question)
        courses = self.udemy_agent.recommend(advice)
        return f"{advice}\n\n🎓 Formations suggérées :\n{courses}"
