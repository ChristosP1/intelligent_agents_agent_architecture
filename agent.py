"""In which we define the classes and such necessary for the agent solution to work."""
# TODO: Alternatively we can use Mesa which was mentioned in the slides. I used this before
# to make agent simulations work, but it's more focused around getting metrics and spatial
# simulations. The former might be of use here though.
from typing import List

class Env:
    """Contains all information in the environment."""
    def __init__(self, prompt: str, sources: List[str]):
        self.agents = []
        self.prompt = prompt
        self.sources = sources

    def step(self):
        for a in self.agents:
            a.perceive()
            a.reason()
            a.act()

class Agent:
    """Contains all information related to individual agents."""
    def __init__(self, env: Env):
        self.env = env
        self.id = len(env.agents)
    
    def perceive(self):
        pass

    def reason(self):
        pass

    def act(self):
        pass