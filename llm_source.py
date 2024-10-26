import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from json import JSONDecodeError
from tolerantjson import tolerate

class ChatGPT_API_Source:
    """
    A class to interact with the ChatGPT API using the 'gpt-4o-mini' model.
    """

    def __init__(self, model="gpt-4o-mini", temperature=0.4, max_tokens=4096):
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
        Calls the ChatGPT API with a given prompt and returns only the response content.
        """
        try:
            response = self.llm.invoke(prompt)  # Using invoke as per deprecation warning
            return response.content  # Only returning the actual content part of the response
        except Exception as e:
            print(f"Error in API call: {e}")
            return None

    def evaluate_normative_statement(self, statement):
        """
        Creates the prompt to evaluate a normative statement and calls the API.
        
        Args:
            statement (str): The normative statement to be evaluated.
        
        Returns:
            dict: The JSON response from the API with the evaluation.
        """
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

        Please evaluate this normative statement: "{statement}"
        """
        # Call the API with the generated prompt
        response = self.call_chatgpt_api(prompt)
        
        if response is None:
            return {"real_information": False, "reason": None }

        # Attempt to parse response as JSON using tolerantjson
        try:
            # Removing non-JSON artifacts (if any) and attempting to parse
            cleaned_response = response.strip().replace("```json", "").replace("```", "")
            parsed_response = tolerate(cleaned_response)
        except Exception as e:
            print(f"Error in tolerant JSON parsing: {e}")
            return {"real_information": False, "reason": None }

        # Check if the required keys exist in parsed response
        if not isinstance(parsed_response, dict) or "real_information" not in parsed_response or "reason" not in parsed_response:
            return {"real_information": False, "reason": None }

        return parsed_response

# Example usage
if __name__ == "__main__":
    # Initialize the ChatGPT API class
    chatgpt_api = ChatGPT_API_Source()

    # Normative statement to evaluate
    our_statement = "Amazon river is safe to swim in."

    # Evaluate the statement
    response = chatgpt_api.evaluate_normative_statement(our_statement)

    # Output the result
    print(response)
