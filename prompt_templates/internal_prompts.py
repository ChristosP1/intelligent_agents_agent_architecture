from langchain.prompts import PromptTemplate
from kor.nodes import Object, Text


# ==============================================================================================================#
synonyms_template = ''' 
    Given a list of words, provide a list with exactly {synonyms_num} synonyms for each word in a dictionary format. 
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

# ==============================================================================================================#
