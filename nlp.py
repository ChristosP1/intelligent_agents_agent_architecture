"""NLP Module used to turn prompts into queries."""
import nltk
import string
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from typing import List

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

# query_db = ["Are frogs dangerous?", "Can sharks be found on land?", "Are frogs not dangerous?"]

"""Remember; queries usually involve selecting a domain first (MedicalConditions, Food, etc.) and
then querying via a relationship. Quite limited but it will have to do for starters."""

def tokenize_prompt(sentence: str):
    """
        This function receives a sentence and removes its stopwords and punctuation.  
    Args:
        tokens (List[str]): a list of tokens preprocessed by nltk.tokenize(str)
        
    Returns:
        filtered_words (List[str]): A list of the words of the original
    """
    word_tokens = word_tokenize(sentence)
    
    return word_tokens


def remove_punctuation(word_tokens: List[str]):
    """
    Receives a list of word tokens (str) and removes the ones that are punctuation

    Args:
        word_tokens (List[str]): A list with a splitted (tokenized) sentence

    Returns:
        filtered_words (List[str]): The input list but without the punctuation
    """
    punctuation = set(string.punctuation)
    filtered_words = [word for word in word_tokens if word not in punctuation]
    
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



def extract_negations(tokens: list) -> list:
    """Extracts negations from a tokenized prompt."""
    

def preprocess_text(prompt: str) -> str:
    """Preprocesses a text for NLP usage."""
    # Step 0; lowercase the entire string
    substr_lower = prompt.lower()
    # Step 1; Tokenize the sentence
    tokens = tokenize_prompt(substr_lower)
    # Step 2; remove punctuation from entire string.
    tokens_no_punct = remove_punctuation(tokens)
    # Step 3; remove stopwords(?; some of these words we may need to keep for negations)
    tokens_pos = pos_tagging(tokens_no_punct)
    
    return tokens_no_punct, tokens_pos
