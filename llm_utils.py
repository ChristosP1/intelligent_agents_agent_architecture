# STANDARD LIBRARIES #
import os
from dotenv import load_dotenv

# LLM #
import langchain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from kor.extraction import create_extraction_chain

# PROMPTS #
from prompt_templates.internal_util_prompts import(
                                                    synonyms_prompt_template,
                                                    synonyms_schema
                                                    )

def initialize_llm():
    """
    This function loads the API key from the .env file and initializes the llm and the optput parser.

    Returns:
        llm: The OpenAI llm with its settings
        output_parser: The output parser that makes the outputs more presentable
    """
    # LOAD API KEY #
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # INITIALIZE LLM & OUTPUT PARSER #
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0.5,
        max_tokens=4096,
        api_key=openai_api_key)

    output_parser = StrOutputParser()
    
    return llm, output_parser


def generate_synonyms(llm, words, synonyms_num=7):
    """
        A function that takes an llm and a list of words and generates 2 synonyms for each word
    Args:
        llm (llm): The OpenAI llm
        words (list): A list of string words
        synonyms_num (int): The number of synonyms that we want for each word
    Returns:
        cleaned_output (dict): A dictionary where each key is a word from the initial list and each value is a list with N synonyms
    """
    
    extraction_chain = create_extraction_chain(
            llm,  # Replace with the LLM instance you're using
            synonyms_schema,
            encoder_or_encoder_class="json"
        )
    
    final_prompt = synonyms_prompt_template.format(words=", ".join(words), synonyms_num=synonyms_num)

    # Proceed with extraction only if the response isn't empty
    structured_output = extraction_chain.invoke(final_prompt)['data']
    print("Structured output:", structured_output)
    
    cleaned_output = {}
    for entry in structured_output['synonyms']:
        cleaned_output.update(entry)  # Combine all dictionaries into one
    
    print("Cleaned structured output:", cleaned_output)
    return cleaned_output
