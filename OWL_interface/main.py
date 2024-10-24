from OWL_interface import OWLInterface
import os

def main():
    ontology_path = os.getcwd()+"\\ontology3.owl"
    owl_interface = OWLInterface(ontology_path)

    sparql_query_1 = """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?frog
            WHERE {
                ?frog rdf:type ex:FrogAndToad .
                ?frog ex:isPoisonous false .
            }
            """
    result = owl_interface.query_ontology(sparql_query_1)
    print("Result for query 1: ",result)

    sparql_query_2 = """
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        SELECT ?symptom
        WHERE {
            ?symptom a ex:Symptom .
            ?symptom ex:resultsFrom ?concussion.
            FILTER(?concussion = ex:Concussion)
        }
    """
    results_2 = owl_interface.query_ontology(sparql_query_2)
    print("Results for Query 2:", results_2)


if __name__ == "__main__":
    main()
