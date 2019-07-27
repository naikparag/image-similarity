from tensorflow.keras import applications
import ssl, time
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image as PILImage
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image as image_preprocessing
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from keras.preprocessing import image


from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import config, os

IMAGE_SIZE = 126

def get_named_model(name):
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # include_top=False removes the fully connected layer at the end/top of the network
    # This allows us to get the feature vector as opposed to a classification
    if name == 'Xception':
        return applications.xception.Xception(weights='imagenet', include_top=False, pooling='avg')

    if name == 'VGG16':
        return applications.vgg16.VGG16(weights='imagenet', include_top=False, pooling='avg')

    if name == 'VGG19':
        return applications.vgg19.VGG19(weights='imagenet', include_top=False, pooling='avg')

    if name == 'InceptionV3':
        return applications.inception_v3.InceptionV3(weights='imagenet', include_top=False, pooling='avg')

    if name == 'MobileNet':
        return applications.mobilenet.MobileNet(weights='imagenet', include_top=False, pooling='avg', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

    return applications.resnet50.ResNet50(weights='imagenet', include_top=False, pooling='avg')

base_model = get_named_model('default')


def get_feature_vector(images):
    time_start = time.time()
    feature_vector = list(map(process_feature_vector, images))
    print('Feature vector processing! Time elapsed: {} seconds'.format(time.time()-time_start))
    return feature_vector

def process_feature_vector(img_path):

    print("processing feature vector for: " + img_path)

    img = PILImage.open( config.IMAGE_DIR + img_path)
    img = img.resize((IMAGE_SIZE,IMAGE_SIZE))
    if not img.mode == 'RGB':
        img = img.convert('RGB')
    x = image_preprocessing.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # extract the features
    features = base_model.predict(x)[0]

    return features

def process_pca(feature_vector):

    time_start = time.time()

    print("-- processing PCA")
    pca = PCA(n_components=0.99, svd_solver='full')
    pca_result = pca.fit_transform(feature_vector)

    print('PCA done! Time elapsed: {} seconds'.format(time.time()-time_start))
    

    return list(pca_result)

def process_tsne(feature_vector):

    time_start = time.time()

    print("-- processing TSNE")
    results = TSNE(n_components=2).fit_transform(feature_vector)

    print('TSNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
    print(results)

    return results

def process_cosine_similarity(feature_vector, product):
    return cosine_similarity(feature_vector, [product])

def save_feature_vector(image_set, feature_vector):
    print("-- saving feature vector: " + config.MODEL_DIR + image_set)
    np.save(config.MODEL_DIR + image_set, feature_vector)

def get_saved_feature_vector(image_set):
    model = config.MODEL_DIR + image_set + '.npy'
    if os.path.exists(model):
        return np.load(model)
    else:
        return None