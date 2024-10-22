from OWL_interface import OWLInterface
import os

def main():
    ontology_path = os.getcwd()+"\\ontology3.owl"
    owl_interface = OWLInterface(ontology_path)

    # result = owl_interface.query_ontology_first_iteration()
    # print(f"Result of the query: {result}")

    result = owl_interface.query_ontology_second_iteration()
    print(f"Result of the query: {result}")



    # Placeholder for now, should come from one of the other functions
    example_query1 = "FrogAndToad and (isPoisonous value false)" # Result should be instance Bullfrog
    example_query2 = "Symptom and (resultsFrom some {Concussion})" # Result should be instances: Amnesia, Fatigue, Headache, Nausea

    # Function to be used in our final agent class
    # result = owl_interface.query_ontology(example_query1)

    # result = owl_interface.query_ontology(example_query2)
    # print(f"Result of the query: {result}")

if __name__ == "__main__":
    main()
