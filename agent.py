"""In which we define the classes and such necessary for the agent solution to work."""
# TODO: Alternatively we can use Mesa which was mentioned in the slides. I used this before
# to make agent simulations work, but it's more focused around getting metrics and spatial
# simulations. The former might be of use here though.
from typing import List, Dict

from llm_utils import initialize_llm, generate_synonyms
from nlp import remo

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

    def add_prompt(self, prompt: Prompt):
        self.prompts.append(prompt)

    def add_source(self, source: Source):
        self.sources.append(source)

    def reset(self):
        self.prompts = []
        self.sources = []

class Agent:
    """Contains all information related to individual agents."""
    # TODO: Massive work in progress, needs more logic.
    def __init__(self, env: Env):
        llm, output_parser = initialize_llm()
        self.llm = llm
        self.output_parser = output_parser
        
        self.env : Env = env
        self.prompt : Prompt = None
        self.variedprompt : List[str] = []
        self.source : Source = None
        self.vars = []  # In which we will store truth values. Maybe a dictionary with key/val; source/truth value?

        self.id = len(env.agents)
        self.state = 1

        self.answer = ""
        self.explanation = ""
    
    def perceive(self):
        if self.state == 1:  # Get a prompt from an user in the env.
            if len(self.env.prompts) > 0:
                self.prompt = self.env.prompts.pop(0)
        elif self.state == 3:  # Get a external source from the env.
            self.source = self.env.sources.pop(0)


    def reason(self):
        if self.state == 1:
            if isinstance(self.prompt, Prompt):
                self.variedprompt = generate_synonyms(self.llm, self.prompt, 2)
                self.state = 2

    def act(self):
        if self.state == 5:
            print(self.answer)
            print(self.explanation)
        # Perhaps querying the ontology is a valid action?

    def __str__(self):
        return "AGENT \n - ID: {}".format(self.id)