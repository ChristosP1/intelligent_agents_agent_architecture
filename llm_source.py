# Required Libraries
import os
from dotenv import load_dotenv

# LLM
from langchain_openai import ChatOpenAI

class ChatGPT_API_Source:
    """
    A class to interact with the ChatGPT API using the 'gpt-4o-mini' model.
    """

    def __init__(self, model="gpt-4o-mini", temperature=0.5, max_tokens=4096):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = self.initialize_llm()

    def initialize_llm(self):
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key
        )
        return llm

    def call_chatgpt_api(self, prompt):
        """
        Calls the ChatGPT API with a given prompt and returns the response.
        """
        try:
            response = self.llm(prompt)
            return response
        except Exception as e:
            print(f"Error in API call: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Initialize the ChatGPT API class
    chatgpt_api = ChatGPT_API_Source()

    our_statement = "Amazon river is safe to swim in."
    # Define the prompt with 3 example evaluations
    prompt = f"""
    I will give you a normative statement, and I want you to evaluate it. 
    You should return a JSON object with two fields:
    1. "real_information": A boolean indicating if the statement is true or false.
    2. "reason": A short explanation of why the statement is true or false.

    Normative statement: "All people should have access to free healthcare."
    Example JSON:
    {{
      "real_information": true,
      "reason": "Access to healthcare is a basic human right, and many countries have successfully implemented free healthcare systems."
    }}

    Normative statement: "It is wrong to harm others for personal gain."
    Example JSON:
    {{
      "real_information": true,
      "reason": "Harming others for personal benefit violates ethical principles and societal laws."
    }}

    Normative statement: "Everyone must drive on the right side of the road."
    Example JSON:
    {{
      "real_information": false,
      "reason": "Not all countries enforce driving on the right side of the road, as countries like the UK and Japan drive on the left."
    }}

    Please evaluate this normative statement: "{our_statement}"
    """

    print(f"Prompt: {prompt}")
    # Call the API
    response = chatgpt_api.call_chatgpt_api(prompt)

    # Output the result
    print(response)
