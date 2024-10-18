from owlready2 import *


def find_ontology_entities(owl_path: str):
    try:
        # Load the ontology
        onto = get_ontology(owl_path).load()

        # 1. Dictionary of classes and their recursive subclasses
        class_subclasses_dict = {}
        
        def get_all_subclasses(cls):
            """Recursively get all subclasses of a class."""
            subclasses = list(cls.subclasses())
            for subclass in subclasses:
                subclasses += get_all_subclasses(subclass)
            return subclasses

        for cls in onto.classes():
            class_subclasses_dict[cls.name] = [subclass.name for subclass in get_all_subclasses(cls)]

        # 2. Dictionary of classes and individuals (including all subclasses' individuals)
        class_individuals_dict = {}

        def get_all_individuals(cls):
            """Recursively get all individuals of a class and its subclasses."""
            individuals = list(cls.instances())
            for subclass in cls.subclasses():
                individuals += get_all_individuals(subclass)
            return individuals

        for cls in onto.classes():
            class_individuals_dict[cls.name] = [individual.name for individual in get_all_individuals(cls)]

        # 3. Dictionary of object properties with their domain and range
        obj_property_domain_range_dict = {}
        for obj_property in onto.object_properties():
            domain = [dom.name for dom in obj_property.domain]  # Domain can be a list
            range_ = [ran.name for ran in obj_property.range]    # Range can also be a list
            obj_property_domain_range_dict[obj_property.name] = [domain, range_]

        # 4. Dictionary of data properties and their domain
        data_property_domain_dict = {}
        for data_property in onto.data_properties():
            domain = [dom.name for dom in data_property.domain]
            data_property_domain_dict[data_property.name] = domain

        # 5. List of all individuals' names in the ontology
        all_individuals_list = [individual.name for individual in onto.individuals()]

        # Return all the structures as a tuple for later use
        return {
            "class_subclasses": class_subclasses_dict,
            "class_individuals": class_individuals_dict,
            "object_property_domain_range": obj_property_domain_range_dict,
            "object_property_domain": data_property_domain_dict,
            "all_individuals": all_individuals_list
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    ontology_data = find_ontology_entities('ontology3.owl')
    
    # Accessing different parts of the returned data
    # print(f"Classes and subclasses: {ontology_data['class_subclasses']}")
    # print("\n\n\n\n\n")
    # print(f"Classes and individuals: {ontology_data['class_individuals']}")
    # print("\n\n\n\n\n")
    # print(f"Object properties with domain and range: {ontology_data['object_property_domain_range']}")
    # print("\n\n\n\n\n")
    # print(f"Object properties with domain: {ontology_data['object_property_domain']}")
    # print("\n\n\n\n\n")
    print(f"All individuals: {ontology_data['all_individuals']}")
