"""In which we define the classes and such necessary for the agent solution to work."""
# TODO: Alternatively we can use Mesa which was mentioned in the slides. I used this before
# to make agent simulations work, but it's more focused around getting metrics and spatial
# simulations. The former might be of use here though.
from typing import List, Dict, Union
import owlready2
from OWL_interface import OWLInterface
import os


# Files
from llm_utils import initialize_llm, generate_synonyms, generate_sparql_queries
from nlp import preprocess_text, cosine_similarity
from owl_utils import find_ontology_entities, find_relevant_ontology_items, precompute_or_load_embeddings
from reddit_utils import RedditAPI



class Prompt:
    """Used to wrap a prompt given to the environment, to be processed by an agent."""
    def __init__(self, prompt: str):
        self.text = prompt

class Source:
    """Used to wrap a source given to the environment, to be processed by an agent."""
    def __init__(self, origin: str, information: str):
        self.origin = origin
        self.info = information

    def compare_to(self, another):  # Just uses another Source, I don't know why Python doesn't like that type definition
        return cosine_similarity(self.info, another.info)

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
        self.llm = initialize_llm()
        ontology_path = os.getcwd() + "\\ontology3.owl"
        self.owl_interface = OWLInterface(ontology_path)
        
        self.reddit_api = RedditAPI()
        
        self.env : Env = env
        self.prompt : Prompt = None
        
        # ---------- State 1 ---------- #
        self.ontology_elements = find_ontology_entities('ontology3.owl')
        self.embeddings_path = 'embeddings/ontology_embeddings.pkl'
        self.ontology_embeddings = precompute_or_load_embeddings(self.ontology_elements, self.embeddings_path)
        self.tokenized_prompt : List[str] = []
        self.pos_tags : List[tuple] = []
        self.tokenized_prompt_with_synonyms : List[str] = []
        # self.ontology_elements: Dict[str, Union[Dict[str, List], List]] = {}
        self.ontology_filtered: Dict[str, Dict[str, List]] = {} 
        
        self.sparql_queries = List[str]
        self.prefix = '<http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>'

        # ----------------------------- #
        
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
    
    def ontology_source_utility(self, source: Source) -> float:
        return cosine_similarity(self.answer, source.info)

    def perceive(self):
        if self.state == 1:  # We are looking for a prompt -> Get a prompt from an user in the env.
            if self.env.prompt is not None:
                print("Set prompt")
                self.prompt = self.env.prompt
        elif self.state == 3:  # We are looking for external sources -> Get a external source from the env.
            if len(self.env.sources) > 0:
                self.source = self.env.sources[self.sourceidx]
            else:  # Fallback scenario in case if all sources have been exhausted.
                self.source = None


    def reason(self):
        # ------------------------------------------ State 1------------------------------------------#
        if self.state == 1 and isinstance(self.prompt, Prompt):  # We have perceived a prompt.
            self.tokenized_prompt, self.pos_tags = preprocess_text(self.prompt.text)  # Use .text here
            self.tokenized_prompt_with_synonyms = generate_synonyms(self.llm, self.pos_tags, 2)

            print(f"- Classes: {len(self.ontology_elements['class_subclasses'])}")
            print(f"- Object Properties: {len(self.ontology_elements['object_property_domain_range'])}")
            print(f"- Data Properties: {len(self.ontology_elements['data_property_domain'])}")
            
            self.ontology_filtered = find_relevant_ontology_items(self.tokenized_prompt, self.pos_tags, self.ontology_elements, self.ontology_embeddings)
            
            print(f"- Filtered Classes: {len(self.ontology_filtered['filtered_classes'])} \n {self.ontology_filtered['filtered_classes'].keys()}")
            print(f"- Filtered Object Properties: {len(self.ontology_filtered['filtered_obj_properties'])} \n {self.ontology_filtered['filtered_obj_properties'].keys()}")
            print(f"- Filtered Data Properties: {len(self.ontology_filtered['filtered_data_properties'])} \n {self.ontology_filtered['filtered_data_properties'].keys()}")
            
            self.sparql_queries = generate_sparql_queries(self.llm, self.prompt.text, self.ontology_filtered, self.prefix)
            
            print(f"- DL queries: {self.sparql_queries}")
            
            self.state = 2
        # --------------------------------------------------------------------------------------------#

        elif self.state == 2:  # We are currently processing our ontology internally.
            # TODO: We need to get a DL query here for the ontology!
            # Use self.variedprompt?
            if self.sourceidx <= len(self.env.sources):
                print("Query ontology")
                outcome = self.owl_interface.query_ontology(self.sparql_queries) # TODO: Query the ontology.
                self.truthval = None # TODO: Explicitely obtain truth value from query ? the outcome variable is a list of results including multiple true/false values
                self.answer = None  # TODO: Obtain an answer from the query
                self.explanation = None  # TODO: Store the DL query raw explanation from the ontology.
                self.state = 3
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
            self.removesource = False
        if self.state == 5:
            print(self.answer)
            print(self.explanation)
        # Perhaps querying the ontology is a valid action?

    def __str__(self):
        return "AGENT \n - ID: {}".format(self.id)
    

if __name__=="__main__":
    # Test step 1
    test_env = Env()
    test_prompt = Prompt("Animals that are not venomus")
    test_env.set_prompt(test_prompt)

    # Create an agent
    test_agent = Agent(test_env)

    # The agent perceives the prompt and process it in State 1
    test_agent.perceive() 
    test_agent.reason()  
    test_agent.reason()