from tensorflow.keras import applications
import ssl

import config

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
        return applications.mobilenet.MobileNet(weights='imagenet', include_top=False, pooling='avg')

    return applications.resnet50.ResNet50(weights='imagenet', include_top=False, pooling='avg')
    

from PIL import Image as PILImage
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image as image_preprocessing
import numpy as np

def get_feature_vector(images):
    print("-- inside get feature vector")
    print(images)
    return list(map(process_feature_vector, images))

def process_feature_vector(img_path):
    print("-- process feature vector")
    print(config.IMAGE_DIR)
    img = PILImage.open( config.IMAGE_DIR + img_path)
    img.resize((224,224),PILImage.ANTIALIAS)
    x = image_preprocessing.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # extract the features
    features = get_named_model('MobileNet').predict(x)[0]

    print("processed feature vector for: " + img_path)

    return features

from sklearn.decomposition import PCA
def process_pca(feature_vector):
    print("-- processing PCA")
    pca = PCA(n_components=6)
    pca_result = pca.fit_transform(feature_vector)
    print(pca_result)

    return pca_result

