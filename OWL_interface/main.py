from OWL_interface import OWLInterface
import os

def main():
    ontology_path = os.getcwd()+"\\ontology3.owl"
    owl_interface = OWLInterface(ontology_path)

    # One example query unrelated to any of our scenarios
    example_query = ["""
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
        
            SELECT ?recipe
            WHERE {
              ?recipe a ex:Recipe;
                    ex:hasIngredient ex:Cheese .
            }
        """]
    # results = owl_interface.query_ontology(example_query)
    # print(results)

    scenario1 = [
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
            
            SELECT ?condition
            WHERE {
              ?condition a/rdfs:subClassOf* ex:Dehydration;
                    ex:hasSymptom ex:Headache;
                    ex:shouldVisitDoctor false .
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
            
            SELECT ?injury
            WHERE {
              ?injury a/rdfs:subClassOf* ex:Injury;
                    ex:isCausedBy ex:Football;
                    ex:hasSymptom ex:Headache .
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?injury
            WHERE {
              ?injury a/rdfs:subClassOf* ex:Injury;
                    ex:hasSymptom ex:Headache;
                    ex:shouldVisitDoctor true .
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?symptom
            WHERE {
              ?symptom a/rdfs:subClassOf* ex:Symptom;
                    ex:resultsFrom ex:Concussion .
            }
            """
    ]
    results = owl_interface.query_ontology(scenario1)
    print(results)
    print("Expected results: -, Concussion, Concussion, Amnesia Fatigue Headache Nausea\n")

    scenario2 = [
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
    
            SELECT ?frogAndToad
            WHERE {
              ?frogAndToad a/rdfs:subClassOf* ex:FrogAndToad;
                           ex:isPoisonous false;
                           ex:isEatenBy ex:Human .
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?nutrient
            WHERE {
              ?nutrient a/rdfs:subClassOf* ex:Nutrient;
                        ex:isPresentIn ?frog.
              ?frog a/rdfs:subClassOf* ex:FrogAndToad.
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?recipe
            WHERE {
              ?recipe a/rdfs:subClassOf* ex:Recipe;
                      ex:hasIngredient ?frog .
              ?frog a/rdfs:subClassOf* ex:FrogAndToad.
            }
            """
    ]
    results = owl_interface.query_ontology(scenario2)
    print(results)
    print("Expected results: Bullfrog, magnesium omega3 phosphorus selenium vitaminB, friedfroglegs frogsoup\n")

    scenario3 = [
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
            
            SELECT ?location
            WHERE {
              ?location a/rdfs:subClassOf* ex:Location;
                         ex:hasAnimal ex:Shark;
                         ex:hasSport ex:Volleyball .
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>

            SELECT ?vegetarian
            WHERE {
              ?vegetarian a/rdfs:subClassOf* ex:Vegetarian;
                           ex:hasIngredient ?ingredient;
                           ex:isEatenBy ex:Shark .
              FILTER (?ingredient = ex:Animal || ?ingredient = ex:Seafood || ?ingredient = ex:Meat)
            }
            """
        ,
            """
            PREFIX ex: <http://www.semanticweb.org/chris/ontologies/2024/8/intelligent_agents_ontology#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            SELECT ?sport
            WHERE {
              ?sport a/rdfs:subClassOf* ex:RepetitiveNonContact ;
                     ex:caloriesBurnedPerHour ?calories .
              FILTER(?calories > 500 && ?sport = ex:Swimming)
            }
            """
    ]
    results = owl_interface.query_ontology(scenario3)
    print(results)
    print("Expected results: -, -, swimming\n")


if __name__ == "__main__":
    main()
