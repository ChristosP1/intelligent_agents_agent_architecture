from langchain.prompts import PromptTemplate
from kor.nodes import Object, Text


# ================================================== SYNONYMS ================================================== #
synonyms_template = ''' 
    Given a list of words, provide a list with exactly {synonyms_num} simple synonyms for each word in a dictionary format.
    The synonyms should be simple, everyday words and not very sophisticated. 
    The dictionary should have the word as the key and a list of {synonyms_num} synonyms as the value. 
    Here is the list of words: {words}.
    
    Example output:
    dict(
        "happy": ["joyful", "content", "pleased", "cheerful"],
        "fast": ["quick", "speedy", "rapid", "swift"]
    )
    '''


synonyms_prompt_template = PromptTemplate(
    input_variables=["words", "synonyms_num"], 
    template=synonyms_template
    )


synonyms_schema = Object(
    id="synonyms",
    description="A dictionary where each word is a key, and the value is a list of n synonyms.",
    attributes=[
        Text(id="{word}", description="Word as key", many=True),  # Define it as many to handle multiple words
        Text(id="synonyms", description="List of synonyms for each word", many=True)
    ],
    many=True,  # Allow for multiple words
)


# ================================================= DL QUERIES ================================================= #

dl_queries_template = ''' 
    You are an expert in Description Logic (DL) queries. You will take a user statement, and based on the given ontology 
    (classes, individuals, object properties, and data properties), generate simple DL queries to either prove or disprove the statement. 

    The ontology is provided in three parts:
    - **Classes and Individuals**: A dictionary where the keys are class names, and the values are lists of individuals that belong to the class.
    - **Object Properties**: A dictionary where the keys are object properties, and the values are lists with the domain (class) and range (class).
    - **Data Properties**: A dictionary where the keys are data properties, and the values are lists with the domain (class) and range (data type like integer, float, or string).

    Your goal is to generate as few DL queries as possible to check whether the statement can be proven using this ontology. 
    The queries should use the relevant individuals, object properties, or data properties where applicable. 
    Ensure the queries are as simple as possible, using minimal logical operations.
    
    ### Examples:
    1. **Statement**: "Concussion can cause headaches."
   - **Ontology**:
    - Classes: {{"Concussion": ["Concussion"], "Symptom": ["Headache", "Nausea"]}}
    - Object Properties: {{"causesSymptom": ["Concussion", "Symptom"]}}
    - Data Properties: {{}}
   - **DL Query**: `Concussion and (causesSymptom some Headache)`
   
   2. **Statement**: "Lizards can live up to 200 years old."
   - **Ontology**:
     - Classes: {{"Lizard": ["Lizard"]}}
     - Object Properties: {{}}
     - Data Properties: {{"lifeExpectancy": ["Lizard", "integer"]}}
   - **DL Query**: `Lizard and (lifeExpectancy value 200)`

    3. **Statement**: "Dogs are carnivores."
    - **Ontology**:
        - Classes: {{"Dog": ["GoldenRetriever", "Bulldog"], "Diet": ["Carnivore"]}}
        - Object Properties: {{"hasDiet": ["Dog", "Diet"]}}
        - Data Properties: {{}}
    - **DL Query**: `Dog and (hasDiet some Carnivore)`

    Now, generate a list of DL queries to prove or disprove the following statement:

    **User's Statement**: "{statement}"

    Here is the ontology:
    - **Classes and Individuals**: {class_individuals}
    - **Object Properties**: {obj_properties}
    - **Data Properties**: {data_properties}

    Generate a list of DL queries in string format, focusing only on the relevant individuals, object properties, or data properties.
    You can generate multiple DL queries if one query does not cover the whole statement.
    '''
    
    
dl_queries_prompt_template = PromptTemplate(
    input_variables=["statement", "class_individuals", "obj_properties", "data_properties"],
    template=dl_queries_template
    )


dl_queries_schema = Object(
    id="dl_query_list",
    description="A list of generated DL queries to prove or disprove the statement using the ontology.",
    attributes=[
        Text(id="dl_query", description="A single DL query.", many=True)
    ],
    many=True,  
)