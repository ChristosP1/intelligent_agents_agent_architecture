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
        temperature=0.5,
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


def generate_sparql_queries(llm, user_statement, ontology_filtered, prefix, max_retries=3):
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
    
    # Convert dictionaries to string format for prompt
    class_individuals_str = json.dumps(ontology_filtered['filtered_classes'], indent=4)
    obj_properties_str = json.dumps(ontology_filtered['filtered_obj_properties'], indent=4)
    data_properties_str = json.dumps(ontology_filtered['filtered_data_properties'], indent=4)
    
    
    sparql_query_prompt = sparql_queries_prompt_template.format(statement=user_statement,
                                                                class_individuals=class_individuals_str,
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
    