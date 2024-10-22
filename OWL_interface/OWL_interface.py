import owlready2
from owlready2 import get_ontology, default_world, sync_reasoner, sync_reasoner_pellet
owlready2.JAVA_EXE = r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"


class OWLInterface:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

        # Run reasoner to obtain inferences
        with self.ontology:
            sync_reasoner_pellet(infer_property_values=True)

        # Additional
        # Reference dictionaries between IRIs and given labels that might be useful
        self.label_to_class = {ent.label[0]: ent for ent in self.ontology.classes() if ent.label}
        self.label_to_prop = {prop.label[0]: prop for prop in self.ontology.properties() if prop.label}

        self.class_to_label = {ent: ent.label[0] for ent in self.ontology.classes() if ent.label}
        self.prop_to_label = {prop: prop.label[0] for prop in self.ontology.properties() if prop.label}

        # Save types to help differentiate between classes and properties later on
        self.class_type = type(list(self.ontology.classes())[0])
        self.property_type = type(list(self.ontology.properties())[0])

    def query_ontology_first_iteration(self):#, query):
        # print("The classes included in the ontology are:")
        # print([cls.name for cls in self.ontology.classes()])

        frog_and_toad = self.ontology.FrogAndToad
        results = [instance for instance in frog_and_toad.instances() if instance.isPoisonous == [False]]

        return results # Returns: [C:\Users\saski\Documents\GitHub\intelligent_agents_agent_architecture\OWL_interface\ontology3.Bullfrog]

    def query_ontology_second_iteration(self):  # , query):
        query = "Symptom and (resultsFrom some {Concussion})"

        try:
            # Parse the query
            query_parts = query.split(" and ")
            class_name = query_parts[0].strip()  # e.g., "Symptom"
            condition = query_parts[1].strip() if len(
                query_parts) > 1 else None  # e.g., "(resultsFrom some {Concussion})"

            # Get the class reference from the label-to-class dictionary
            query_class = self.label_to_class.get(class_name)
            if not query_class:
                raise ValueError(f"Class '{class_name}' not found in the ontology.")

            # If there's no condition, return all instances of the class
            if not condition:
                return list(query_class.instances())

            # Parse the condition
            if "some" in condition:
                # Example: "resultsFrom some {Concussion}"
                prop_name, instance_name = condition.replace("(", "").replace(")", "").split(" some ")
                prop_name = prop_name.strip()
                instance_name = instance_name.strip("{}").strip()

                # Get the property and instance references
                query_property = self.label_to_prop.get(prop_name)
                query_instance = self.ontology.search_one(label=instance_name)

                if not query_property:
                    raise ValueError(f"Property '{prop_name}' not found in the ontology.")
                if not query_instance:
                    raise ValueError(f"Instance '{instance_name}' not found in the ontology.")

                # Search for instances of the class that have the property related to the instance
                results = [
                    inst for inst in query_class.instances()
                    if query_instance in getattr(inst, query_property.python_name, [])
                ]
                return results
            else:
                raise ValueError(f"Unsupported query condition: '{condition}'")

        except Exception as e:
            print(f"Error processing query: {e}")
            return []






        # Spark SQL queries
        # l = list(default_world.sparql("""  """))
        # print(f"Querying the ontology with: {query}")
        # return result
