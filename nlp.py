"""NLP Module used to turn prompts into queries."""
import nltk
from nltk.util import ngrams

query_db = ["Are frogs dangerous?", "Can sharks be found on land?", "Are frogs not dangerous?"]

"""Remember; queries usually involve selecting a domain first (MedicalConditions, Food, etc.) and
then querying via a relationship. Quite limited but it will have to do for starters."""

def prompt_parser(prompt: str) -> str:
    """Turns a prompt into a DL Query for use in the OWL API for determining whether a statement is truthful."""

def filter(pre: str, blacklist : list =[":",";",",",".","?","!"]):
    new = ""
    for char in pre:
        if char not in blacklist:
            new += char
    return new

def extract_negations(tokens: list) -> list:
    """Extracts negations from a tokenized prompt."""
    

def preprocess_text(prompt: str) -> str:
    """Preprocesses a text for NLP usage."""
    # Step 1; remove punctuation from entire string.
    substr1 = filter(prompt)
    # Step 2; tokenize
    substr2 = nltk.tokenize(substr1)
