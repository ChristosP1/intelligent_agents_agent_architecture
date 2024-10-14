from owlready2 import get_ontology, default_world, sync_reasoner


class OWLInterface:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

    def query_ontology(self):#, query):
        print("The classes included in the ontology are:")
        print([cls.name for cls in self.ontology.classes()])

        # Surely we will use the reasoner
        with self.ontology:
            sync_reasoner()
        print("reasoning...")

        # Spark SQL queries
        # l = list(default_world.sparql("""  """))
        # print(f"Querying the ontology with: {query}")
        # return result
