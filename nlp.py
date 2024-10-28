import nltk
import string
import math
import os

from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from typing import List

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('averaged_perceptron_tagger')
os.system('cls')

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
    tokenizer = TweetTokenizer(preserve_case=False)  # TweetTokenizer to preserve contractions
    word_tokens = tokenizer.tokenize(sentence)
    
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

def remove_stopwords(word_tokens: List[str]):
    stop_words = set(stopwords.words('english'))
    keep_words = {"and", "or", "not", "no", "only", "every", "all", "any", "both", "each", 
                  "nor", "few", "some", "at least", "at most", 
                  "exactly", "sometimes", "if", "then", "all", "does", "doesn't", "do", "was", "were",
                  "because", "until", "while", "of", "at", "by", "for", "with", "between", 
                  "into", "during", "before", "after", "above", "below", "to", "from", "up",
                  "down", "in", "out", "on", "off", "over", "under", "then", "most", "will",
                  "oesn't", "had", "hadn't", "has", "hasn't", "are", "aren't", "can", "can't",
                  "there", "is", "when", "why", "where", "how", "more", "most", "same", "just", 
                  "didn't", "did", "have", "haven't", "might", "must", "need", "won't", "wouldn't"}

    custom_stopwords = stop_words - keep_words

    return [word for word in word_tokens if word not in custom_stopwords]


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
    # Step 2; remove some stopwords.
    tokens_remove_stop = remove_stopwords(tokens_no_punct)
    # Step 3; remove stopwords(?; some of these words we may need to keep for negations)
    tokens_pos = pos_tagging(tokens_remove_stop)
    
    return tokens_remove_stop, tokens_pos



def cosine_similarity(str1: str, str2: str) -> float:
    """Calculate the cosine similarity between two strings. This cosine similarity
    is then scaled to be within the range of [0,1] by only using positive counts."""
    vector1 = []
    vector2 = []
    tokens1 = nltk.word_tokenize(str1)
    tokens2 = nltk.word_tokenize(str2)
    combined = tokens1 + tokens2

    for token in set(combined):
        vector1.append(tokens1.count(token))
        vector2.append(tokens2.count(token))

    nomsum = 0
    denomsuma = 0
    denomsumb = 0
    for i, _ in enumerate(set(combined)):
        nomsum += vector1[i] * vector2[i]
        denomsuma += vector1[i]**2
        denomsumb += vector2[i]**2

    return (nomsum/(math.sqrt(denomsuma) * math.sqrt(denomsumb)))
