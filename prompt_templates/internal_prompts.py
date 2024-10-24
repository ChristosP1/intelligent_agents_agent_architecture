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

sparql_queries_template = ''' 
    You are an expert in SPARQL queries. You will take a user statement, and based on the given ontology 
    (classes, individuals, object properties, and data properties), generate simple SPARQL queries to either 
    prove or disprove the statement. 

    The ontology is provided in three parts:
    - **Classes and Individuals**: A dictionary where the keys are class names, and the values are lists of individuals that belong to the class.
    - **Object Properties**: A dictionary where the keys are object properties, and the values are lists with the domain (class) and range (class).
    - **Data Properties**: A dictionary where the keys are data properties, and the values are lists with the domain (class) and range (data type like integer, float, or string).

    Your goal is to generate as few SPARQL queries as possible to check whether the statement can be proven using this ontology.
    Ensure the queries use `rdfs:subClassOf*` where appropriate to retrieve both direct instances and instances from subclasses.

    ### Examples:
    1. **Statement**: "Concussion can cause headaches."
    - **Ontology**:
        - Classes: {{"Concussion": ["Concussion"], "Symptom": ["Headache", "Nausea"]}}
        - Object Properties: {{"causesSymptom": ["Concussion", "Symptom"]}}
        - Data Properties: {{}}
    - **SPARQL Query**:
    ```sparql
    PREFIX ex: {prefix}
    
    SELECT ?symptom
    WHERE {{
        ?symptom a/rdfs:subClassOf* ex:Symptom;
                ex:resultsFrom ex:Concussion .
    }}
    ```
    
    2. **Statement**: "Lizards can live up to 200 years old."
    - **Ontology**:
        - Classes: {{"Lizard": ["Lizard"]}}
        - Object Properties: {{}}
        - Data Properties: {{"lifeExpectancy": ["Lizard", "integer"]}}
    - **SPARQL Query**:
    ```sparql
    PREFIX ex: {prefix}
    
    SELECT ?lizard
    WHERE {{
    ?lizard a/rdfs:subClassOf* ex:Lizard;
            ex:lifeExpectancy ?years .
    FILTER (?years >= 200)
    }}
    ```

    3. **Statement**: "Dogs are carnivores."
    - **Ontology**:
        - Classes: {{"Dog": ["GoldenRetriever", "Bulldog"], "Diet": ["Carnivore"]}}
        - Object Properties: {{"hasDiet": ["Dog", "Diet"]}}
        - Data Properties: {{}}
    - **SPARQL Query**:
    ```sparql
    PREFIX ex: {prefix}
    
    SELECT ?dog
    WHERE {{
    ?dog a/rdfs:subClassOf* ex:Dog;
         ex:hasDiet ex:Carnivore .
    }}
    ```

    Now, generate a list of SPARQL queries to prove or disprove the following statement:

    **User's Statement**: "{statement}"

    Here is the ontology:
    - **Classes and Individuals**: {class_individuals}
    - **Object Properties**: {obj_properties}
    - **Data Properties**: {data_properties}
    
    **Prefix**: {prefix}

    Ensure to use `rdfs:subClassOf*` where applicable to include subclasses and relevant instances.
    '''
    
    
sparql_queries_prompt_template = PromptTemplate(
    input_variables=["statement", "class_individuals", "obj_properties", "data_properties", "prefix"],
    template=sparql_queries_template
)

sparql_queries_schema = Object(
    id="sparql_query_list",
    description="A list of generated SPARQL queries to prove or disprove the statement using the ontology.",
    attributes=[
        Text(id="sparql_query", description="A single SPARQL query.", many=True)
    ],
    many=True,
)
