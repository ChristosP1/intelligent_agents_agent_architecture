from langchain.prompts import PromptTemplate
from kor.nodes import Object, Text


statement_answer_template = ''' 
    You are given a statement and a truth value. Your task is to produce a short response sentence that is clear, contextually relevant, and reflects the truth value of the statement. 

    **Instructions:**
    1. **For "True"**: Confirm the statement in a concise manner, retaining the essence and meaning.
    2. **For "False"**: Rephrase the statement to reflect that it is not true.
    3. **For "Not Found"**: Indicate that there is no available information to confirm or deny the statement.

    ### Examples

    **Example 1**
    - Statement: "If you have dehydration you should see a doctor"
    - Truth value: "False"
    - Extracted text: "If you have dehydration, you don't have to see a doctor."

    **Example 2**
    - Statement: "There are dishes that have ingredient frogsandtoads"
    - Truth value: "True"
    - Extracted text: "There are dishes that have frogs and toads as an ingredient."

    **Example 3**
    - Statement: "All reptiles are venomous"
    - Truth value: "False"
    - Extracted text: "Not all reptiles are venomous."

    **Example 4**
    - Statement: "There are no foods with Vitamin C"
    - Truth value: "Not Found"
    - Extracted text: "No information found about foods with Vitamin C."

    Now, please generate a short response for the following:

    - **Statement**: "{statement}"
    - **Truth Value**: "{truth_value}"

    '''
    
    
statement_answer_prompt_template = PromptTemplate(
    input_variables=["statement", "truth_value"],
    template=statement_answer_template
)


statement_response_schema = Object(
    id="statement_response",
    description="A short response sentence based on the truth value of a given statement.",
    attributes=[
        Text(id="response_text", description="The concise response sentence reflecting the truth value of the statement.")
    ],
    many=False
)


##############################################################################################################
##############################################################################################################

truth_statement_template = ''' 
    You are given a statement. Your task is to assess it and generate a concise response with the following:
    - A **truth value** (either "True" or "False") indicating whether the statement is correct.
    - A **response** sentence that briefly confirms or refutes the statement based on the truth value.

    **Instructions**:
    - Don't pay attention to grammatical or syntactical mistakes.
    - If the content of the statement is correct, return "True" as the truth value and a supportive sentence.
    - If the content of the statement is incorrect, return "False" as the truth value and a sentence that refutes the statement.

    ### Example Format

    **Example 1**
    - Statement: "Dogs can fly."
    - Truth Value: "False"
    - Response: "Dogs cannot fly."

    **Example 2**
    - Statement: "Cats are mammals."
    - Truth Value: "True"
    - Response: "Cats are indeed mammals."

    Now, evaluate the following:

    - **Statement**: "{statement}"
'''


truth_statement_prompt_template = PromptTemplate(
    input_variables=["statement"],
    template=truth_statement_template
)


truth_statement_schema = Object(
    id="truth_statement",
    description="An object containing a truth value and a response for the given statement.",
    attributes=[
        Text(id="truth_value", description="A truth value indicating whether the statement is correct, either 'True' or 'False'."),
        Text(id="response_text", description="A short response sentence confirming or refuting the statement.")
    ]
)


##############################################################################################################
##############################################################################################################


scenario_explanation_template = ''' 
Given the following scenario evaluation, produce a concise and natural explanation. The explanation should support the scenario's truth value without mentioning sources, separate statements, or technical details.

Statements:
{statements}

Final Assessment: The scenario is {truth_value}.

Generate a cohesive explanation based on the final assessment, using the statement evaluations to support the overall truth value in a single paragraph. The explanation should avoid listing individual statements or referencing the ontology.

Example output:
"The scenario is {truth_value}. There are indeed animals in the Amazon with humans in their diet, such as piranhas. However, swimming is not considered a non-contact sport, and the calories burned per hour are not consistently above 500."

'''

scenario_explanation_prompt_template = PromptTemplate(
    input_variables=["statements", "truth_value"], 
    template=scenario_explanation_template
)


scenario_explanation_schema = Object(
    id="scenario_explanation",
    description="A structured explanation for the truth value of the scenario based on statements provided.",
    attributes=[
        Text(id="truth_value", description="Boolean result of scenario truth."),
        Text(id="explanation", description="Explanation based on statements.")
    ],
)





