from OWL_interface import OWLInterface
import os

def main():
    ontology_path = os.getcwd()+"\\ontology3.owl"
    owl_interface = OWLInterface(ontology_path)

    sparql_query_1 = """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?individual
            WHERE {
                ?individual a ex:FrogAndToad .
                ?individual ex:isPoisonous false .
            }
            """
    # result = owl_interface.query_ontology(sparql_query_1)
    # print("Result for query 1: ",result)

    sparql_query_2 = """
        PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

        SELECT ?symptom
        WHERE {
          ?symptom a ex:Symptom .
          ?symptom ex:resultsFrom ex:Concussion .
        }
    """
    # results_2 = owl_interface.query_ontology(sparql_query_2)
    # print("Results for Query 2:", results_2)

    spark_sql_queries = [
        # Query 1: Dehydration and (hasSymptom some {Headache}) and (shouldVisitDoctor value true)
        """
        SELECT * 
        FROM conditions 
        WHERE condition_name = 'Dehydration' 
        AND hasSymptom LIKE '%Headache%' 
        AND shouldVisitDoctor = true;
        """,

        # Query 2: Injury and (isCausedBy some {Football}) and (hasSymptom some {Headache})
        """
        SELECT * 
        FROM injuries 
        WHERE isCausedBy LIKE '%Football%' 
        AND hasSymptom LIKE '%Headache%';
        """,

        # Query 3: Injury and (hasSymptom some {Headache}) and (shouldVisitDoctor value true)
        """
        SELECT * 
        FROM injuries 
        WHERE hasSymptom LIKE '%Headache%' 
        AND shouldVisitDoctor = true;
        """,

        # Query 4: Symptom and (resultsFrom some {Concussion})
        """
        SELECT * 
        FROM symptoms 
        WHERE resultsFrom LIKE '%Concussion%';
        """
    ]
    for query in spark_sql_queries:
        print(owl_interface.query_ontology(query))

if __name__ == "__main__":
    main()
