
class Reasoner:
    def __init__(self, llm = None):
        self.llm = llm
    def reason(self, statement, evaluation):
        reason = evaluation["reason"]
        if reason is None:
            return "I could not find any information to confirm or falsify this statement."
        
        truthhood = str(evaluation["real_information"]).lower();

        if not "reddit_title" in evaluation:
            return f"This is {truthhood}, because {reason}"

        reddit_title = evaluation["reddit_title"]

        prefix = f"According to the reddit post \"{reddit_title}\" this is {truthhood}"
        if self.llm is None:
            return f"{prefix}, because {reason}"
        
        prompt = f'''
        I will give you a JSON object with 3 fields:
        1. "statement": A statement that is evaluated to be either true or false.
        2. "real_information": A boolean indicating whether the specified statement in the "statement" field is true or false.
        3. "reason": A text that explains why the statement specified in the "statement" field is true or false according to the "real_information" field.
        You will return a summary of the "reason" field that explains why the statement specified in the "statement" field is true or false according to the "real_information" field.

        JSON:
        {{
            "statement": "A lactose intolerant person can drink milk.",
            "real_information": false,
            "reason": "Milk is a white liquid food produced by the mammary glands of mammals. It is the primary source of nutrition for young mammals (including breastfed human infants) before they are able to digest solid food. Milk contains many nutrients, including calcium and protein, as well as lactose and saturated fat. Immune factors and immune-modulating components in milk contribute to milk immunity. Early-lactation milk, which is called colostrum, contains antibodies and immune-modulating components that strengthen the immune system against many diseases. The US CDC agency recommends that children over the age of 12 months (the minimum age to stop giving breast milk or formula) should have two servings of dairy (milk) products a day, and more than six billion people worldwide consume milk and milk products."
        }}
        Example summary: "Milk contains lactose."

        JSON:
        {{
            "statement": "I can reach London from New York just by car."
            "real_information": true,
            "reason": "Hi, I am planning a road trip through America by car. Starting in Vegas I will be visiting various cities such as New York. I will end the roadtrip in Canada, more specifically London, Ontario. I do not have the specifics of the roadtrip planned out yet, does anyone have any recommendations for the roadtrip that are not that popular under tourists?"
        }}
        Example summary: "London is a city in Ontario, Canada."

        JSON:
        {{
            "statement": "The Python programming language is named after its creator's favorite animal."
            "real_information": false,
            "reason": "Python's developers usually strive to avoid premature optimization and reject patches to non-critical parts of the CPython reference implementation that would offer marginal increases in speed at the cost of clarity. Execution speed can be improved by moving speed-critical functions to extension modules written in languages such as C, or by using a just-in-time compiler like PyPy. It is also possible to cross-compile to other languages, but it either doesn't provide the full speed-up that might be expected, since Python is a very dynamic language, or a restricted subset of Python is compiled, and possibly semantics are slightly changed. Python's developers aim for it to be fun to use. This is reflected in its name — a tribute to the British comedy group Monty Python — and in occasionally playful approaches to tutorials and reference materials, such as the use of the terms "spam" and "eggs" (a reference to a Monty Python sketch) in examples, instead of the often-used "foo" and "bar". A common neologism in the Python community is pythonic, which has a wide range of meanings related to program style. "Pythonic" code may use Python idioms well, be natural or show fluency in the language, or conform with Python's minimalist philosophy and emphasis on readability. Code that is difficult to understand or reads like a rough transcription from another programming language is called unpythonic."
        }}
        Example summary: "The Python programming language was named after the British comedy group Monty Python."

        Summarize the "reason" field of the following JSON:
        {{
            "statement": {statement},
            "real_information": {truthhood},
            "reason": "{reason}"
        }}
        '''
        # https://en.wikipedia.org/wiki/Milk
        # https://en.wikipedia.org/wiki/Python_(programming_language)

        return f"{prefix}, because {self.llm.invoke(prompt).content}"
    
    def reason_ontology(self, query, truth_value, examples):
        prompt = f'''
            You are an expert at SPARQL query deconstruction.
            Your goal is to generate a natural explanation from a SPARQL query and its result.
            
            Your input is a JSON object consisting of 3 fields.
            The first field "query" is a string representing a SPARQL query.
            The second field "truth_value" is a boolean that indicates whether the query specified in the "query" field was evaluated to be true.
            The third field "examples" is a possibly empty list of examples that make the query true or false as specified by the "truth_value" field.
            
            ### Examples
            #### 1.
            - Input:
            ```
            {{
                "query": "PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#> SELECT ?isVenomous WHERE {{ ex:Gecko ex:isVenomous ?isVenomous . }}",
                "truth_value": false,
                "examples": []
            }}
            ```
            - Output:
            "Geckos are not venomous."

            #### 2.
            - Input:
            ```
            {{
                "query": "PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#> SELECT ?recipe WHERE {{ ?recipe a ex:Recipe ; ex:hasIngredient ?ingredient . ?ingredient a/rdfs:subClassOf* ex:FrogAndToad . }}",
                "truth_value": true,
                "examples": ["FrogRisotto", "FriedFrogLegs"]
            }}
            ```
            - Output:
            "The recipes for frog risotto and fried frog legs contain frogs or toads."

            #### 3.
            ```
            {{
                "query": "PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#> SELECT ?nutrient WHERE {{ ?nutrient ex:isPresentIn ?frogAndToad . ?frogAndToad a/rdfs:subClassOf* ex:FrogAndToad . }}",
                "truth_value": true,
                "examples": ["SaturatedFat"]
            }}
            ```
            - Output:
            "Nutrients such as saturated fat are present in frogs and toads."

            #### 4.
            ```
            {{
                "query": "PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#> SELECT ?dessert WHERE {{ ?dessert a/rdfs:subClassOf* ex:Dessert ; ex:hasIngredient ex:Shark . }}",
                "truth_value": false,
                "examples": []
            }}
            ```
            - Output:
            "There are no desserts that contain shark."

            Now, generate an exmplanation for the following JSON:
            ```
            {{
                "query": "{query}",
                "truth_value": {truth_value},
                "examples": {examples}
            }}
            ```
        '''

        return self.llm.invoke(prompt).content