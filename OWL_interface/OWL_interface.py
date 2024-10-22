from pprint import pprint
from owlready2 import *
owlready2.JAVA_EXE = r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"


class OWLInterface:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

        # Run reasoner to obtain inferences
        with self.ontology:
            sync_reasoner_pellet(infer_property_values=True)

        # Additional
        # Reference dictionaries between IRIs and given labels that might be useful
        self.label_to_class = {ent.label[0]: ent for ent in self.ontology.classes()}
        self.label_to_prop = {prop.label[0]: prop for prop in self.ontology.properties()}

        self.class_to_label = {ent: ent.label[0] for ent in self.ontology.classes()}
        self.prop_to_label = {prop: prop.label[0] for prop in self.ontology.properties()}

        # Save types to help differentiate between classes and properties later on
        self.class_type = type(list(self.ontology.classes())[0])
        self.property_type = type(list(self.ontology.properties())[0])


    # def query_ontology_first_iteration(self):#, query):
    #     # print("The classes included in the ontology are:")
    #     # print([cls.name for cls in self.ontology.classes()])
    #
    #     frog_and_toad = self.ontology.FrogAndToad
    #     results = [instance for instance in frog_and_toad.instances() if instance.isPoisonous == [False]]
    #
    #     return results # Returns: [C:\Users\saski\Documents\GitHub\intelligent_agents_agent_architecture\OWL_interface\ontology3.Bullfrog]


    def query_ontology_second_iteration(self, query):  # , query):

        query_class, query_condition = self.parse_query(query)
        # If there's no condition, return all instances of the class
        if not query_condition:
            return list(query_class.instances())

        property_type, query_property, query_instance, value = self.parse_condition(query_condition)

        if property_type == "object_property":
            # Search for instances of the class that have the property related to the instance
            results = [
                instance.name for instance in query_class.instances()
                if query_instance in getattr(instance, query_property.python_name, [])
            ]

        elif property_type == "data_property":
            results = [
                instance.name for instance in query_class.instances()
                if getattr(instance, query_property.python_name) == [value]
            ]

        return results


    def parse_query(self, query):
        query_parts = query.split(" and ")

        # Get class
        class_name = query_parts[0].strip()
        query_class = self.label_to_class.get(class_name)
        if not query_class:
            raise ValueError(f"Class '{class_name}' not found in the ontology.")

        # Get condition
        condition = query_parts[1].strip("()").strip() if len(
            query_parts) > 1 else None

        return query_class, condition


    def parse_condition(self, condition):
        property_type = None
        property_name = None
        query_instance = None
        value = None

        if "some" in condition:
            property_type = "object_property"
            prop_name, instance_name = condition.split(" some ")
            property_name = prop_name.strip()
            instance_name = instance_name.strip("{}").strip()
            query_instance = self.ontology.search_one(label=instance_name)

        elif "value" in condition:
            property_type = "data_property"
            prop_name, value_str = condition.split(" value ")
            property_name = prop_name.strip()
            value = self.parse_value(value_str)

        query_property = self.label_to_prop.get(property_name)

        # if not query_property:
        #     raise ValueError(f"Property '{property_name}' not found in the ontology.")
        # if not query_instance:
        #     raise ValueError(f"Instance '{instance_name}' not found in the ontology.")

        return property_type, query_property, query_instance, value

    def parse_value(self, string):
        if string == "true":
            return True
        if string == "false":
            return False