from owlready2 import *


def find_ontology_entities(owl_path: str):
    try:
        # Load the ontology 
        onto = get_ontology(owl_path).load()  
        
        # List of classes
        classes_list = [cls.name for cls in onto.classes()]
        individuals_list = [individual.name for individual in onto.individuals()]
        object_properties_list = [obj_property.name for obj_property in onto.object_properties()]
        data_properties_list = [data_property.name for data_property in onto.data_properties()]
        
        
        if not classes_list or not individuals_list or not object_properties_list or not data_properties_list:
            print("Some items were not found.")
        else:
            print(f"Classes found ({len(classes_list)}): {classes_list[:4]} . . . and more . . .")
            print(f"Individuals found ({len(individuals_list)}): {individuals_list[:4]} . . . and more . . .")
            print(f"Obj. properties found ({len(object_properties_list)}): {object_properties_list[:4]} . . . and more . . .")
            print(f"Data properties found ({len(data_properties_list)}): {data_properties_list[:4]} . . . and more . . .")
        
        return classes_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__=="__main__":
    find_ontology_entities('ontology3.owl')