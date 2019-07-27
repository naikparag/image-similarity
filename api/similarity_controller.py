import api.image_util as image_util
import api.ml_util as ml_util
import random, uuid
import pandas as pd
from pathlib import Path
from ast import literal_eval

RANDOM_PRODUCT_COUNT = 4

uuids = []
feature_vector = []
feature_vector_low_dimention = []
import numpy as np
def process_images(image_set):

    global uuids
    global feature_vector
    global feature_vector_low_dimention

    product_dict =  image_util.process_images(image_util.STATIC_PATH + image_util.IMAGE_PATH, image_set)
    uuids = list(product_dict.keys())
    products = list(product_dict.values())
    product_images = list(map(get_image_from_product, products))
    
    csv_path = image_util.STATIC_PATH + image_util.IMAGE_PATH +image_set + '/'

    my_file = Path(csv_path+image_set+'.csv')
    if  my_file.is_file():
        
        df = pd.read_csv(my_file)
        feature_vector,feature_vector_low_dimention = get_saved_feature_vectors(image_set)
        
    else:
        feature_vector = ml_util.get_feature_vector(product_images)
        feature_vector_low_dimention = ml_util.process_pca(feature_vector)
        
        df = pd.DataFrame(feature_vector)
        df.insert(0,'UUID',uuids)
       
        df.to_csv(csv_path+"feature_vector"+'.csv',index=False)

        df = pd.DataFrame(feature_vector_low_dimention)
        df.insert(0,'UUID',uuids)
        
        df.to_csv(csv_path+"pca_feature_vector"+'.csv',index=False)
        
        Data = {}
        Data['UUID'] = uuids
        Data['Images'] = product_images
        data_frame = pd.DataFrame(Data, columns = ['UUID','Images'])
        data_frame.to_csv(csv_path + image_set+'.csv')

    
    

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

def get_saved_feature_vectors(image_dir):
    csv_path = image_util.STATIC_PATH + image_util.IMAGE_PATH+image_dir+'/'
    print('Fetching Feature vectores from csv')
    print(csv_path + 'feature_vector.csv')
    fv_df = pd.read_csv(csv_path + 'feature_vector.csv')
    pca_fv_df = pd.read_csv(csv_path + 'pca_feature_vector.csv')
    fv = fv_df.loc[:, fv_df.columns != 'UUID']
    pca_fv = pca_fv_df.loc[:, pca_fv_df.columns != 'UUID']
    return (fv.values.tolist(),pca_fv.values.tolist())
        

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


