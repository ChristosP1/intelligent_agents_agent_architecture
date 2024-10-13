"""NLP Module used to turn prompts into queries."""
import nltk
import string
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')

# query_db = ["Are frogs dangerous?", "Can sharks be found on land?", "Are frogs not dangerous?"]

"""Remember; queries usually involve selecting a domain first (MedicalConditions, Food, etc.) and
then querying via a relationship. Quite limited but it will have to do for starters."""

def remove_stopwords(tokens: List[str]):
    """
        This function receives a sentence and removes its stopwords and punctuation.  
    Args:
        tokens (List[str]): a list of tokens preprocessed by nltk.tokenize(str)
        
    Returns:
        filtered_words (List[str]): A list of the words of the original sentence after the cleaning
    """
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    # word_tokens = word_tokenize(sentence)
    filtered_words = [word for word in tokens if word.lower() not in stop_words and word not in punctuation]
    # TODO: Can later remove word.lower() as this should already be done in the process by this point.
    # print(tokens)
    # print(filtered_words)
    
    return filtered_words


def pos_tagging(words):
    """_summary_

    Args:
        words (list or string): A list of words or a sentence

    Returns:
        pos_tags (list): A list of tuples (Word, TAG)
    """
    
    if type(words) is not list:
        word_tokens = word_tokenize(words)
    else:
        word_tokens = words
        
    pos_tags = nltk.pos_tag(word_tokens)
    print(pos_tags)
    
    return pos_tags

def prompt_parser(tokens: List[str]) -> str:
    """Turns a tokenized prompt into a DL Query for use in the OWL API for determining whether a statement is truthful."""
    end_query = ""
    # Step 1: Determine relevant sets (similarity)
    # Step 2: Determine relevant relationship
    return end_query

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
    # Step 0; lowercase the entire string
    substr0 = prompt.lower()
    # Step 1; remove punctuation from entire string.
    substr1 = filter(substr0)
    # Step 2; tokenize
    tokens1 = nltk.tokenize(substr1)
    # Step 3; remove stopwords(?; some of these words we may need to keep for negations)
    tokens2 = remove_stopwords(tokens1)
