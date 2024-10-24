from pprint import pprint
from owlready2 import *
owlready2.JAVA_EXE = r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"


class OWLInterface:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

        with self.ontology:
            sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


    def query_ontology(self, queries):
        # Print all instances of Symptom and their resultsFrom property
        # print(self.ontology.search(is_a=self.ontology.Symptom, resultsFrom=self.ontology.search(is_a=self.ontology.Concussion)))

        results = []
        for query in queries:
            instances = list(default_world.sparql(query))
            result = [instance[0].name for instance in instances]
            if result: result.insert(0,"True")
            if not result: result.insert(0, "False")
            results.append(result)

        return results
