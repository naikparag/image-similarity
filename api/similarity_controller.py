import numpy as np
import api.image_util as image_util
import api.ml_util as ml_util
import os
import collections
import uuid
import random
import config
import pandas as pd
from pathlib import Path
from ast import literal_eval
from api import persist_util

RANDOM_PRODUCT_COUNT = 4
metadata = set()

model_detail = collections.namedtuple(
    'model_detail', 'uuid, product_dict, pca, tsne')
model_dict = {}

METADATA_FILE = 'metadata.pickle'


def process_images_v2(image_set):

    global model_dict
    global metadata

    sync_metadata(image_set)

    model_dict[image_set] = get_model_detail(image_set)

    return 'Processinng Images for - ' + image_set


def sync_metadata(image_set):
    global metadata

    if os.path.exists(config.MODEL_DIR + METADATA_FILE):
        metadata = persist_util.get_from_file(METADATA_FILE)

    metadata.add(image_set)
    persist_util.save_to_file(METADATA_FILE, metadata)

    print(metadata)


def get_model_detail(image_set):
    global model_dict

    # 1. return in memory model if present
    if image_set in model_dict:
        print("-- return in-memory model for - " + image_set)
        return model_dict[image_set]

    saved_model_path = config.MODEL_DIR + image_set + '.pickle'

    # 2. return frozen model if present
    if os.path.exists(saved_model_path):
        print("-- return frozen model for - " + image_set)
        return persist_util.get_from_file(image_set + '.pickle')

    # 3. generate model from source
    model_detail = generate_model_detail(image_set)
    persist_util.save_to_file(image_set + '.pickle', model_detail)

    return model_detail


def generate_model_detail(image_set):

    product_dict = image_util.process_images(
        image_util.STATIC_PATH + image_util.IMAGE_PATH, image_set)
    uuids = list(product_dict.keys())
    products = list(product_dict.values())
    product_images = list(map(get_image_from_product, products))

    feature_vector = ml_util.get_feature_vector(product_images)
    pca = ml_util.process_pca(feature_vector)
    tsne = ml_util.process_tsne(pca)

    return model_detail(uuids, product_dict, pca, tsne)


def get_feature_vector(image_set, product_images):
    model = ml_util.get_saved_feature_vector(image_set)
    if model is None:
        model = ml_util.get_feature_vector(product_images)
        ml_util.save_feature_vector(image_set, model)
    else:
        print("-- returning saved featured vector from disk.")
        # simply return model

    return model


def get_random_products(image_set):
    global model_dict

    product_dict = (model_dict[image_set]).product_dict
    random_products = dict(random.sample(
        product_dict.items(), RANDOM_PRODUCT_COUNT))

    return random_products


def get_similar_products(image_set, product_id):

    global model_dict

    model_detail = model_dict[image_set]

    product_id = uuid.UUID(product_id)
    product_feature_vector = get_feature_vector_for_product_id(
        product_id, model_detail)

    similarity_results = ml_util.process_cosine_similarity(
        model_detail.pca, product_feature_vector)

    similarity_indices = similarity_results.argsort(
        axis=0)[:-5:-1].flatten().tolist()
    print(similarity_indices)

    product_dict = model_detail.product_dict
    products = list(product_dict.values())

    return ([products[i] for i in similarity_indices])

# helper
# --------------------


def get_image_from_product(product):
    return product.image_name


def get_feature_vector_for_product_id(product_id, model_detail):

    product_index = (model_detail.uuid).index(product_id)
    return (model_detail.pca)[product_index]
