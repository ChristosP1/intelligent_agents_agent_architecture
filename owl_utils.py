from owlready2 import *
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Union
import numpy as np
import pickle
import os
import Levenshtein


# Initialize the HuggingFace embeddings model
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    

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
            "data_property_domain": data_property_domain_dict,
            "all_individuals": all_individuals_list
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def get_embedding(text: str) -> np.ndarray:
    """Generate the embedding for a given text using HuggingFace embeddings."""
    return np.array(embeddings_model.embed_query(text))


def save_embeddings_to_file(embeddings: Dict, filepath: str):
    with open(filepath, "wb") as f:
        pickle.dump(embeddings, f)


def load_embeddings_from_file(filepath: str) -> Dict:
    with open(filepath, "rb") as f:
        return pickle.load(f)
    
        
def precompute_ontology_embeddings(ontology_data: Dict) -> Dict:
    # Unpack the ontology data
    class_individuals_dict = ontology_data["class_individuals"]
    class_subclasses_dict = ontology_data["class_subclasses"]
    obj_property_domain_range_dict = ontology_data["object_property_domain_range"]
    data_property_domain_dict = ontology_data["data_property_domain"]
    
    # Precompute embeddings and store them in dictionaries
    class_embeddings = {class_name: embeddings_model.embed_query(class_name) for class_name in class_subclasses_dict.keys()}
    individual_embeddings = {individual: embeddings_model.embed_query(individual) for class_name, individuals in class_individuals_dict.items() for individual in individuals}
    obj_property_embeddings = {prop_name: embeddings_model.embed_query(prop_name) for prop_name in obj_property_domain_range_dict.keys()}
    data_property_embeddings = {data_prop_name: embeddings_model.embed_query(data_prop_name) for data_prop_name in data_property_domain_dict.keys()}
    
    # Return a dictionary of all precomputed embeddings
    return {
        "class_embeddings": class_embeddings,
        "individual_embeddings": individual_embeddings,
        "obj_property_embeddings": obj_property_embeddings,
        "data_property_embeddings": data_property_embeddings
    }
    

def precompute_or_load_embeddings(ontology_data: Dict, embeddings_filepath: str) -> Dict:
    # Check if the embeddings file exists
    if os.path.exists(embeddings_filepath):
        print("Loading precomputed embeddings from file...")
        return load_embeddings_from_file(embeddings_filepath)
    else:
        print("Precomputing embeddings...")
        # Precompute embeddings for ontology
        embeddings = precompute_ontology_embeddings(ontology_data)
        # Save embeddings to file
        save_embeddings_to_file(embeddings, embeddings_filepath)
        return embeddings



def is_similar(word: str, prop_name: str, word_embedding: np.ndarray, prop_embedding: np.ndarray, threshold: float = 0.4) -> bool:
    """
    Combines cosine similarity and Levenshtein distance to determine whether two words are similar enough.
    """
    # Compute cosine similarity for semantic matching
    embedding_similarity = cosine_similarity([word_embedding], [prop_embedding])[0][0]
    
    # Compute Levenshtein distance for structural string similarity
    levenshtein_similarity = 1 - (Levenshtein.distance(word, prop_name) / max(len(word), len(prop_name)))
    
    # Combine both similarities (you can tweak the weights as needed)
    combined_similarity = (embedding_similarity * 0.7) + (levenshtein_similarity * 0.3)
    
    return combined_similarity >= threshold

    
def find_relevant_ontology_items(statement_tokens: List[str], pos_tagged_tokens: List[Tuple[str, str]], 
                                 ontology_data: Dict, embeddings_filepath: str):
    
    # Load or compute embeddings
    ontology_embeddings = precompute_or_load_embeddings(ontology_data, embeddings_filepath)
    
    # Initialize lists
    classes = []
    obj_properties = []
    data_properties = []
    
    # Unpack the ontology data
    class_individuals_dict = ontology_data["class_individuals"]
    class_subclasses_dict = ontology_data["class_subclasses"]
    obj_property_domain_range_dict = ontology_data["object_property_domain_range"]
    data_property_domain_dict = ontology_data["data_property_domain"]
    
    # Unpack the precomputed embeddings
    class_embeddings = ontology_embeddings["class_embeddings"]
    individual_embeddings = ontology_embeddings["individual_embeddings"]
    obj_property_embeddings = ontology_embeddings["obj_property_embeddings"]
    data_property_embeddings = ontology_embeddings["data_property_embeddings"]
    
    
    # Step 1: Compare nouns to individuals in class_individuals_dict
    for word, pos in pos_tagged_tokens:
        if pos.startswith('NN'):  # Nouns
            word_embedding = get_embedding(word)  # Compute embedding for the dynamic input
            for class_name, individuals in class_individuals_dict.items():
                for individual in individuals:
                    if individual in individual_embeddings:  # Use precomputed embedding for the individual
                        individual_embedding = individual_embeddings[individual]
                        if is_similar(word, individual, word_embedding, individual_embedding, threshold=0.65):  # Combine similarity
                            if class_name not in classes:
                                classes.append(class_name)
                            break  # No need to check other individuals in this class!
                    
    
    # Step 2: Compare nouns to class names in class_subclasses_dict
    for word, pos in pos_tagged_tokens:
        if pos.startswith('NN'):  # Nouns
            word_embedding = get_embedding(word)  # Compute embedding for the dynamic input
            for class_name in class_subclasses_dict.keys():
                if class_name in class_embeddings:  # Use precomputed embedding for the class
                    class_embedding = class_embeddings[class_name]
                    if is_similar(word, class_name, word_embedding, class_embedding, threshold=0.65):  # Combine similarity
                        if class_name not in classes:
                            classes.append(class_name)

                        
    
    # Step 3: Compare words to object properties in obj_property_domain_range_dict
    for word in statement_tokens:
        word_embedding = get_embedding(word)  # Compute embedding for the dynamic input word
        for prop_name, (domain, range_) in obj_property_domain_range_dict.items():
            if prop_name in obj_property_embeddings:  # Use precomputed embedding for the object property
                prop_embedding = obj_property_embeddings[prop_name]
                if is_similar(word, prop_name, word_embedding, prop_embedding, threshold=0.4):  # Combine similarity
                    if prop_name not in obj_properties:
                        obj_properties.append(prop_name)
                    if domain[0] not in classes:
                        classes.append(domain[0])
                    if range_[0] not in classes:
                        classes.append(range_[0])

                    
        
    # Step 4: Compare words to data properties in data_property_domain_dict
    for word in statement_tokens:
        word_embedding = get_embedding(word)  # Compute embedding for the dynamic input word
        for data_prop_name, domain in data_property_domain_dict.items():
            if data_prop_name in data_property_embeddings:  # Use precomputed embedding for the data property
                data_prop_embedding = data_property_embeddings[data_prop_name]
                if is_similar(word, data_prop_name, word_embedding, data_prop_embedding, threshold=0.4):  # Combine similarity
                    if data_prop_name not in data_properties:
                        data_properties.append(data_prop_name)
                    if domain[0] not in classes:
                        classes.append(domain[0])
                        
    
    ### Final Step: Scan all individuals of relevant classes and gather their data properties
    for class_name in classes:
        if class_name in class_individuals_dict:  # Ensure the class has individuals
            individuals = class_individuals_dict[class_name]
            for individual in individuals:
                for data_prop_name, domain in data_property_domain_dict.items():
                    # Check if the individual's class is in the domain of the data property
                    if domain[0] == class_name and data_prop_name not in data_properties:
                        data_properties.append(data_prop_name)
                        

    

    # Step 5: Filter the dictionaries based on collected classes and properties
    filtered_class_individuals = {cls: inds for cls, inds in class_individuals_dict.items() if cls in classes}
    filtered_obj_properties = {prop: dom_rng for prop, dom_rng in obj_property_domain_range_dict.items() if prop in obj_properties}
    filtered_data_properties = {data_prop: dom for data_prop, dom in data_property_domain_dict.items() if data_prop in data_properties}

    return {
        "filtered_classes": filtered_class_individuals,
        "filtered_obj_properties": filtered_obj_properties,
        "filtered_data_properties": filtered_data_properties
    }
    
    
    
    
    

if __name__ == "__main__":
    ontology_data = find_ontology_entities('ontology3.owl')
    # print(type(ontology_data))
    # Accessing different parts of the returned data
    # print(f"Classes and subclasses: {ontology_data['class_subclasses']}")
    # print("\n\n\n\n\n")
    # print(f"Classes and individuals: {ontology_data['class_individuals']}")
    # print("\n\n\n\n\n")
    # print(f"Object properties with domain and range: {ontology_data['object_property_domain_range']}")
    # print("\n\n\n\n\n")
    # print(f"Object properties with domain: {ontology_data['data_property_domain']}")
    # print("\n\n\n\n\n")
    # print(f"All individuals: {ontology_data['all_individuals']}")

    