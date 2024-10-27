from pprint import pprint
from owlready2 import *
owlready2.JAVA_EXE = r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"


class OWLInterface:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

        with self.ontology:
            sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


    def query_ontology(self, queries):
        """
        Function that takes SPARQL queries and uses them to query the ontology.

        Args:
            A list of SPARQL queries in string format.

        Returns:
            A list of the results for each query. For each query all the instances are returned. If the list
            has elements it starts with "true", if it doesn't it starts with "false".
        """
        try:
            results = []
            for query in queries:
                instances = list(default_world.sparql(query))
                
                # Check if the result is a boolean query result (ASK query result)
                if all(isinstance(item[0], bool) for item in instances):
                    # If any `True` is found in the results, return True, else return False
                    boolean_result = any(item[0] for item in instances)
                    results.append(['True'] if boolean_result else ['False'])
                else:
                    # For non-boolean results, extract individual names as before
                    result = list(set(instance[0].name for instance in instances if instance))
                    if result:
                        results.append(['True', result])  # Nest result in a list with 'True'
                    else:
                        results.append(['False'])
            
            return results
        except:
            return False
