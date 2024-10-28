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
    You are an expert in SPARQL query construction. 
    Your goal is to generate precise and specific SPARQL queries to answer user statements by retrieving 
    exact information from the provided ontology. Avoid generalizations and focus on specificity.
 

    The ontology is structured with three main components:
    1. **Hierarchical Ontology Structure**: This contains classes with nested subclasses and individuals, showing the hierarchy and which individuals belong to each class or subclass.
    2. **Object Properties**: These connect instances or classes by establishing relationships. Each object property includes a *domain* and a *range*, defining the types of entities it connects.
    3. **Data Properties**: These provide literal values for classes or individuals (e.g., integer, string, boolean values). Data properties use `FILTER` statements in SPARQL to filter literal values.

 
    Your goal is to generate SPARQL queries to verify statements by determining relationships, properties, or class memberships. 
    Based on the statement type, you may need to apply one of two methods:

    1. **Direct Assertion Method**: This method is used when verifying relationships or properties between specific individuals.
        - **When to Use**: Apply this when the statement involves a direct relationship or property assertion between individual entities (e.g., “Carbonara has ingredient Bacon” or “Gecko is venomous”).
        - **SPARQL Construction**: 
        - Directly reference both individuals in the `WHERE` clause.
        - Use `FILTER` statements where necessary to verify specific conditions on individual properties.

    2. **Class-Based Method**: This method is applied when verifying relationships or properties at the class level, such as subclass relationships, retrieving instances based on class membership, or checking properties that apply to all instances of a class.
        - **When to Use**: Apply this when the statement involves a generalization about classes or requests information based on class membership (e.g., “Reptiles are venomous” or “All frogs and toads are non-poisonous”).
        - **SPARQL Construction**:
        - Use `rdfs:subClassOf*` to query class hierarchies.
        - Use `?variable a/rdfs:subClassOf*` in the `WHERE` clause for class-based filtering.
        - Retrieve instances or properties that apply to all members of a class or subclass.

    
    ### Examples of Direct Assertion Method

    #### 1. Verifying an Individual’s Relationship to Another Individual
    - **Statement**: “Carbonara has ingredient Bacon.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?ingredient
        WHERE {{
            ex:Carbonara ex:hasIngredient ?ingredient .
            FILTER(?ingredient = ex:Bacon)
        }}
        ```

    #### 2. Checking an Individual’s Specific Boolean Property
    - **Statement**: “Gecko is venomous.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?isVenomous
        WHERE {{ ex:Gecko ex:isVenomous ?isVenomous . }}
        ```

    #### 3. Filtering Data Properties for an Individual’s Attribute
    - **Statement**: “Swimming burns more than 500 calories.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?sport
        WHERE {{
            ex:Swimming ex:caloriesBurnedPerHour ?calories .
            FILTER(?calories > 500)
        }}
        ```

    #### 4. Confirming an Individual’s Property Against a Specific Entity
    - **Statement**: “Salmon has nutrient VitaminB12.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?nutrient
        WHERE {{ 
            ex:Salmon ex:hasNutrient ?nutrient . 
            FILTER(?nutrient = ex:VitaminB12)
        }}
        ```
    
    #### 5. Validating an Object Property Relationship Between Two Individuals
    - **Statement**: “Weightlifting trains bodypart Bicep.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?bodyPart
        WHERE {{
            ex:Weightlifting ex:trainsBodyPart ?bodyPart .
            FILTER(?bodyPart = ex:Bicep)
        }}
        ```
        
    #### 6. Retrieving Recipes with Specific Ingredients Including Subclasses
    - **Statement**: “There are recipes that have ingredient some frogsandtoads.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?recipe
        WHERE {{
            ?recipe a ex:Recipe ;
                    ex:hasIngredient ?ingredient .
            ?ingredient a/rdfs:subClassOf* ex:FrogAndToad .
        }}
        ```
    
    #### 7.
    - **Statement**: “There are recipes that have ingredient some frogsandtoads.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?symptom
        WHERE {{
        ?symptom ex:isCausedBy ex:Concussion .
        }}
        ```
        

    ### Examples of Class-Based Method

    #### 1. Retrieving All Instances of a Class Based on a Shared Property
    - **Statement**: “Reptiles are venomous.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?reptile
        WHERE {{
            ?reptile a/rdfs:subClassOf* ex:Reptile ;
                    ex:isVenomous ?isVenomous .
            FILTER(?isVenomous = true)
        }}
        ```

    #### 2. Validating Subclass Membership
    - **Statement**: “Birds are animals.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?birdSubclass
        WHERE {{
            ?birdSubclass a/rdfs:subClassOf* ex:Bird .
            ?birdSubclass a/rdfs:subClassOf* ex:Animal .
        }}
        ```
        
    #### 3. Confirming an Invalid Subclass Relationship
    - **Statement**: “Birds are mammals.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

        SELECT ?birdInstance
        WHERE {{
            ?birdInstance a/rdfs:subClassOf* ex:Bird .
            ?birdInstance a/rdfs:subClassOf* ex:Mammal .
        }}
        ```

    #### 4. Property Filtering for Class Members with Data Properties
    - **Statement**: "There are frogs and toads that are not poisonous and are eaten by humans."
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        
        SELECT ?frogAndToad
        WHERE {{
            ?frogAndToad a/rdfs:subClassOf* ex:FrogAndToad ;
                        ex:isEatenBy ex:Human ;
                        ex:isPoisonous ?isPoisonous .
            FILTER(?isPoisonous = false)
        }}
        ```
    - **Explanation**:
        - Use the **Direct Assertion Method** with `FILTER` for the data property `isPoisonous`.
        - When querying literal values (e.g., boolean, integer), retrieve the data property as a variable (e.g., `?isPoisonous`) and filter it using `FILTER(?isPoisonous = false)`.
        - This approach ensures that only frogs and toads that are **not** poisonous and are eaten by humans are returned, aligning with the statement’s requirements.


    #### 5. Object Property with Reversed Order
    - **Statement**: "Some nutrients are present in frogs and toads."
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        
        SELECT ?nutrient
        WHERE {{
            ?nutrient ex:isPresentIn ?frogAndToad .
            ?frogAndToad a/rdfs:subClassOf* ex:FrogAndToad .
        }}
        ```
    - **Explanation**:
        - This query aims to find instances of nutrients that are present in any frogs and toads.
        - **Object Property Ordering**: Since the statement asks if "nutrients are present in frogs and toads," the nutrient should be the subject, followed by the `isPresentIn` property with `?frogAndToad` as the object.
        - The class hierarchy for `FrogAndToad` is included using `a/rdfs:subClassOf* ex:FrogAndToad`, allowing the query to return any nutrients related to `FrogAndToad` and its subclasses.


    #### 6. Identifying Class Instances Based on Contained Ingredients
    - **Statement**: “List all desserts that contain Chocolate.”
    - **SPARQL Query**:
        ```sparql
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?dessert
        WHERE {{
            ?dessert a/rdfs:subClassOf* ex:Dessert ;
                    ex:hasIngredient ex:Chocolate .
        }}
        ```    
        
    Now, generate a list of SPARQL queries to prove or disprove the following statement:

    **User's Statement**: "{statement}"

    Here is the ontology:
    - **Hierarchical ontology**: {hierarchical_ontology}
    - **Object Properties**: {obj_properties}
    - **Data Properties**: {data_properties}
    
    **Prefix**: {prefix}

    Ensure to use `rdfs:subClassOf*` only for classes to include subclasses and relevant instances.
    '''
    
    
sparql_queries_prompt_template = PromptTemplate(
    input_variables=["statement", "hierarchical_ontology", "obj_properties", "data_properties", "prefix"],
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
