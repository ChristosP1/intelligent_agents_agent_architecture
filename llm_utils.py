# STANDARD LIBRARIES #
import os
from dotenv import load_dotenv
import json

# LLM #
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from kor.extraction import create_extraction_chain

# PROMPTS #
from prompt_templates.internal_prompts import(synonyms_prompt_template, 
                                              synonyms_schema,
                                              sparql_queries_prompt_template,
                                              sparql_queries_schema)

from prompt_templates.external_prompts import (statement_answer_prompt_template,
                                               statement_response_schema,
                                               truth_statement_prompt_template,
                                               truth_statement_schema)


def initialize_llm():
    """
    This function loads the API key from the .env file and initializes the llm and the optput parser.

    Returns:
        llm: The OpenAI llm with its settings
    """
    # LOAD API KEY #
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # INITIALIZE LLM & OUTPUT PARSER #
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0.2,
        max_tokens=4096,
        api_key=openai_api_key)

    
    return llm


def generate_synonyms(llm, pos_tagged_words, synonyms_num=3):
    """
        A function that takes an llm and a list of words and generates N synonyms for each word
    Args:
        llm (llm): The OpenAI llm
        words (list): A list of string words
        synonyms_num (int): The number of synonyms that we want for each word
    Returns:
        cleaned_output (dict): A dictionary where each key is a word from the initial list and each value is a list with N synonyms
    """
    
    # Filter words that are nouns, adjectives, or verbs
    filtered_words = [word for word, pos in pos_tagged_words if pos.startswith(('NN', 'JJ', 'VB'))]

    final_prompt = synonyms_prompt_template.format(words=", ".join(filtered_words), synonyms_num=synonyms_num)
    
    extraction_chain = create_extraction_chain(
            llm, 
            synonyms_schema,
            encoder_or_encoder_class="json"
        )

    # Proceed with extraction
    structured_output = extraction_chain.invoke(final_prompt)['data']
    
    cleaned_output = {}
    for entry in structured_output['synonyms']:
        cleaned_output.update(entry)  # Combine all dictionaries into one
    
    
    output_list = []

    for word, _ in pos_tagged_words:
        output_list.append(word)  # Add original word to the output list
        if word in cleaned_output and isinstance(cleaned_output[word], list):
            for synonym in cleaned_output[word]:
                if isinstance(synonym, str):
                    if " " in synonym:  # Handle synonyms with spaces
                        synonym = synonym.replace(" ", "")
                    output_list.append(synonym)  # Add synonym to the output list
                    

  
    print(f"List with synonyms: {output_list}")
    return output_list


def convert_to_json_serializable(obj):
    """
    Helper function to recursively convert objects to JSON-serializable types.
    - Attempts to convert unknown types by using `str()`.
    - Handles lists, dictionaries, and nested structures recursively.
    """
    if isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    try:
        json.dumps(obj)  # Try serializing; if it fails, convert to string
        return obj
    except (TypeError, ValueError):
        return str(obj)  # Convert non-serializable objects to strings


def generate_sparql_queries(llm, user_statement, ontology_filtered, prefix, max_retries=6):
    """
    A function that takes the llm, the user statement, and the ontology elements, and generates SPARQL queries
    to prove or disprove the statement. It retries in case of structural errors.

    Args:
        llm (llm): The OpenAI llm
        user_statement (str): The user’s input statement
        ontology_filtered (dict): The filtered ontology data

    Returns:
        sparql_queries_output (list): A list of SPARQL queries
    """

    # Apply the conversion to make the entire dictionary JSON-serializable
    ontology_filtered_serializable = {
        "hierarchical_ontology": convert_to_json_serializable(ontology_filtered['hierarchical_ontology']),
        "filtered_obj_properties": convert_to_json_serializable(ontology_filtered['filtered_obj_properties']),
        "filtered_data_properties": convert_to_json_serializable(ontology_filtered['filtered_data_properties'])
    }

    # Convert dictionaries to JSON string format for the prompt
    hierarchical_ontology_str = json.dumps(ontology_filtered_serializable['hierarchical_ontology'], indent=4)
    obj_properties_str = json.dumps(ontology_filtered_serializable['filtered_obj_properties'], indent=4)
    data_properties_str = json.dumps(ontology_filtered_serializable['filtered_data_properties'], indent=4)
    
    sparql_query_prompt = sparql_queries_prompt_template.format(statement=user_statement,
                                                                hierarchical_ontology=hierarchical_ontology_str,
                                                                obj_properties=obj_properties_str,
                                                                data_properties=data_properties_str,
                                                                prefix=prefix)
    
    extraction_chain = create_extraction_chain(llm, 
                                               sparql_queries_schema,
                                               encoder_or_encoder_class="json")
    
    
    # Retry mechanism
    retries = 0
    while retries < max_retries:
        try:
            # Proceed with extraction
            sparql_queries_output = extraction_chain.invoke(sparql_query_prompt)['data']
            # Convert it to list
            sparql_queries_output_list = [query['sparql_query'][0] for query in sparql_queries_output['sparql_query_list']]        
            return sparql_queries_output_list
        
        except KeyError as e:
            print(f"KeyError: {e}. Retrying {retries + 1}/{max_retries}...")
            retries += 1
    
    # If it fails after all retries
    raise ValueError("Failed to generate valid SPARQL queries after multiple retries.")
    
    
def generate_statement_answer(llm, statement, truth_value, max_retries=3):
    """
    Generates a concise response based on the given statement and truth value.

    Args:
        statement (str): The input statement to evaluate.
        truth_value (str): The truth value of the statement, which can be 'True', 'False', or 'Not Found'.

    Returns:
        str: The generated response.
    """
    # Create the prompt
    prompt = statement_answer_prompt_template.format(statement=statement, truth_value=truth_value)
    
    # Initialize the extraction chain with a predefined schema
    extraction_chain = create_extraction_chain(
        llm, 
        statement_response_schema,  # Define this schema similar to `synonyms_schema`
        encoder_or_encoder_class="json"
    )
    
    # Attempt extraction with retry mechanism
    retries = 0
    while retries < max_retries:
        try:
            structured_output = extraction_chain.invoke(prompt)['data']
            # Extract and return the generated response
            response_text = structured_output['statement_response']['response_text']
            return response_text.strip()
        except Exception as e:
            print(f"Attempt {retries + 1} failed: {e}")
            retries += 1

    # If all retries fail, return a default error message
    return "Unable to generate a response after multiple attempts."



def query_llm_for_answer(llm, statement, max_retries=3):
    """
    Generates a dictionary containing a truth value and a concise response to either confirm or refute the given statement.
    
    Args:
        llm: The language model instance.
        statement (str): The input statement to evaluate.
        max_retries (int): Number of retry attempts in case of errors (default is 3).
    
    Returns:
        dict: A dictionary with 'truth_value' ('True' or 'False') and 'response' keys.
    """
    # Create the prompt
    prompt = truth_statement_prompt_template.format(statement=statement)
    
    # Initialize the extraction chain with a predefined schema
    extraction_chain = create_extraction_chain(
        llm, 
        truth_statement_schema,  
        encoder_or_encoder_class="json"
    )
    
    # Attempt extraction with retry mechanism
    retries = 0
    while retries < max_retries:
        try:
            structured_output = extraction_chain.invoke(prompt)['data']
            # Extract the generated response
            truth_value = structured_output['truth_statement']['truth_value']
            response_text = structured_output['truth_statement']['response_text']
            return {"truth_value": truth_value, "response": response_text.strip()}
        except Exception as e:
            print(f"Attempt {retries + 1} failed: {e}")
            retries += 1
    
    # If all retries fail, return a default error message
    return {"truth_value": "Not determined", "response": "Unable to determine the truth value after multiple attempts."}

    
    