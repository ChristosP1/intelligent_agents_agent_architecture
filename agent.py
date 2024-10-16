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
        self.prompt = None
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

    def set_prompt(self, prompt: Prompt):
        self.prompt = prompt

    def add_source(self, source: Source):
        self.sources.append(source)

    def reset(self):
        self.prompt = []
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
        self.sourceidx : int = 0
        self.removesource : bool = False  # Whether we need to remove the source we queried last
        self.vars = []  # In which we will store truth values. Maybe a dictionary with key/val; source/truth value?

        self.id = len(env.agents)
        self.state = 1

        self.env.add_agent(self)

        self.truthval = None
        self.answer = ""
        self.explanation = ""
    
    def perceive(self):
        if self.state == 1:  # We are looking for a prompt -> Get a prompt from an user in the env.
            if self.env.prompt is not None:
                self.prompt = self.env.prompt
        elif self.state == 3:  # We are looking for external sources -> Get a external source from the env.
            if len(self.env.sources) > 0:
                self.source = self.env.sources[self.sourceidx]
            else:  # Fallback scenario in case if all sources have been exhausted.
                self.source = None


    def reason(self):
        if self.state == 1:  # We have perceived a prompt.
            if isinstance(self.prompt, Prompt):
                self.variedprompt = generate_synonyms(self.llm, self.prompt, 2)  # TODO: Is this done properly?
                self.state = 2
        elif self.state == 2:  # We are currently processing our ontology internally.
            # TODO: We need to get a DL query here for the ontology!
            # Use self.variedprompt?
            if self.sourceidx <= len(self.env.sources):
                outcome = None # TODO: Query the ontology.
                self.truthval = None # TODO: Explicitely obtain truth value from query
                self.answer = None  # TODO: Obtain an answer from the query
                self.explanation = None  # TODO: Store the DL query raw explanation from the ontology.
                self.state = 3
            else:  # If there's no more remaining sources to query
                self.state = 5
        elif self.state == 3:  # We are currently querying external sources and have obtained one (hopefully)
            # TODO: Query the text for a truth value?
            # TODO: Turn the text into an ontology query?
            self.state = 4  # We can now start comparing the internal source to the external source.
        elif self.state == 4:  # Comparison of sources
            # TODO: Source comparison
            pass
        elif self.state == 5:  # !: When we reach this state; do nothing. We reached the goal state already.
            self.state = 6  # Special terminal state that is not handled to prevent spamming the console



    def act(self):
        if self.state == 4:  # If we did the comparison;
            if self.removesource:  # If our internal ontology was better than the external source;
                self.env.sources.pop(0)
            else:
                self.sourceidx += 1  # Ignore the current source; leave it in the environment
        if self.state == 5:
            print(self.answer)
            print(self.explanation)
        # Perhaps querying the ontology is a valid action?

    def __str__(self):
        return "AGENT \n - ID: {}".format(self.id)