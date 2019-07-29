import api.image_util as image_util
import api.ml_util as ml_util
import random, uuid
import pandas as pd
from pathlib import Path
from ast import literal_eval
from api import persist_model_util as model_util
RANDOM_PRODUCT_COUNT = 4

uuids = []
feature_vector = []
feature_vector_low_dimention = []
tsne = []
import numpy as np
def process_images(image_set):

    global uuids
    global feature_vector
    global feature_vector_low_dimention
    global tsne

    product_dict =  image_util.process_images(image_util.STATIC_PATH + image_util.IMAGE_PATH, image_set)
    uuids = list(product_dict.keys())
    products = list(product_dict.values())
    product_images = list(map(get_image_from_product, products))

    if  model_util.is_model_present(image_set):
        feature_vector,feature_vector_low_dimention,tsne= model_util.get_all_saved_feature_vectors(image_set)

    else:
        feature_vector = ml_util.get_feature_vector(product_images)
        feature_vector_low_dimention = ml_util.process_pca(feature_vector)
        tsne =  ml_util.process_tsne(feature_vector_low_dimention)

        model_util.save_dataset(image_set,uuids,process_images)
        model_util.save_feature_vectors(image_set,uuids,feature_vector)
        model_util.save_pca(image_set,uuids,feature_vector_low_dimention)
        model_util.save_tsne(image_set,uuids,tsne)

    #return products


def get_feature_vector(image_set, product_images):
    model = ml_util.get_saved_feature_vector(image_set)
    if model is None:
        model = ml_util.get_feature_vector(product_images)
        ml_util.save_feature_vector(image_set, model)
    else:
        print("-- returning saved featured vector from disk.")
        # simply return model

    return model

def get_random_products():
    product_dict = image_util.get_product_dict_from_cache()
    random_products = dict(random.sample(
        product_dict.items(), RANDOM_PRODUCT_COUNT))

    return random_products
        
def get_similar_products(product_id):

    global feature_vector_low_dimention

    product_id = uuid.UUID(product_id)
    product_feacture_vector = get_feature_vector_for_product_id(product_id)
    
    similarity_results = ml_util.process_cosine_similarity(feature_vector_low_dimention, product_feacture_vector)
   
    
    similarity_indices = similarity_results.argsort(axis=0)[:-5:-1].flatten().tolist()
    print(similarity_indices)

    product_dict = image_util.get_product_dict_from_cache()
    products = list(product_dict.values())

    return ([products[i] for i in similarity_indices])

# helper
# --------------------

def get_image_from_product(product):
    return product.image_name

def get_feature_vector_for_product_id(product_id):
    global feature_vector_low_dimention
    global uuids

    product_index = uuids.index(product_id)

    return feature_vector_low_dimention[product_index]


