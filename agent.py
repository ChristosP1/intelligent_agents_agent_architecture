"""In which we define the classes and such necessary for the agent solution to work."""
# TODO: Alternatively we can use Mesa which was mentioned in the slides. I used this before
# to make agent simulations work, but it's more focused around getting metrics and spatial
# simulations. The former might be of use here though.
from typing import List

class Prompt:
    """Used to wrap a prompt given to the environment, to be processed by an agent."""
    def __init__(self, prompt: str):
        pass

class Source:
    """Used to wrap a source given to the environment, to be processed by an agent."""
    def __init__(self, information: str):
        pass

class Env:
    """Contains all information in the environment."""
    def __init__(self):
        self.agents = []
        self.prompts = []
        self.sources = []

    def step(self):
        for a in self.agents:
            a.perceive()
            a.reason()
            a.act()
    
    def get_agents(self):
        return self.agents
    
    def add_agent(self, a):
        self.agents.append(a)

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

    def __str__(self):
        return "AGENT \n - ID: {}".format(self.id)