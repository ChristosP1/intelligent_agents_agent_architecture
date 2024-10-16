from OWL_interface import OWLInterface
import os

def main():
    ontology_path = os.getcwd()+"\\ontology3.owl"
    owl_interface = OWLInterface(ontology_path)

    # Placeholder for now, should come from one of the other functions
    example_query = "Does soccer cause concussions?" # -> Soccer and canCause Concussion

    # Function to be used in our final agent class
    # result = owl_interface.query_ontology(example_query)
    # print(f"Result of the query: {result}")

    owl_interface.query_ontology()

if __name__ == "__main__":
    main()
