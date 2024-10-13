# STANDARD LIBRARIES #
import streamlit
import pandas as pd
import numpy as np

# LOGGING #
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger()

# LLM & NLP #
from llm_utils import *
from nlp_utils import *




    

def Agent():
    # Initialize llm and output parser
    llm, output_parser = initialize_llm()
    logger.info(">> LLM and Parser created")

    words = remove_stopwords("This. is a lovely day to go for a walk!")
    pos_tags = pos_tagging(words)

    synonyms = generate_synonyms(llm, words)





if __name__=="__main__":
    Agent()