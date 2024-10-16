import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')


def remove_stopwords(sentence):
    """
        This function receives a sentence and removes its stopwords and punctuation.  
    Args:
        sentence (string): A natural langiage sentence
        
    Returns:
        filtered_words (list): A list of the words of the original sentence after the cleaning
    """
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    word_tokens = word_tokenize(sentence)
    filtered_words = [word for word in word_tokens if word.lower() not in stop_words and word not in punctuation]
    print(word_tokens)
    print(filtered_words)
    
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
    

# def filter(pre: str, blacklist : list =[":",";",",",".","?","!"]):
#     new = ""
#     for char in pre:
#         if char not in blacklist:
#             new += char
#     return new


# def preprocess_text_pipeline(prompt: str) -> str:
#     """Preprocesses a text for NLP usage."""
#     # Step 1; remove punctuation from entire string.
#     substr1 = filter(prompt)
#     # Step 2; Tokenize string
#     substr2 = nltk.tokenize(substr1)
