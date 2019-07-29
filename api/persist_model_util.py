import pandas as pd
import os

dirname = 'models/'

TSNE = 'tsne.csv'
PCA = 'pca_feature_vector.csv'
FEATURE_VECTOR = 'feature_vector.csv'

def is_model_present(image_Set):
    
    csv_dir = dirname + image_Set 
    return os.path.isdir(csv_dir)

def get_dataset(image_dir):
    dataset_path =  os.path.join(dirname, image_dir, image_dir + '.csv')
    print('Fectchin dataset from :: '+ dataset_path)
    dataframe = pd.read_csv(dataset_path)
    return dataframe


def get_feature_vectors(image_dir):
    dataset_path =  os.path.join(dirname, image_dir, FEATURE_VECTOR )
    print('Fectching feature vectors from :: '+ dataset_path)
    fv_df = pd.read_csv(dataset_path)
    fv = fv_df.loc[:, fv_df.columns != 'UUID']
    return fv.values.tolist()

def get_pca_feature_vectors(image_dir):
    dataset_path =  os.path.join(dirname, image_dir, PCA )
    print('Fectching pca from :: '+ dataset_path)
    fv_df = pd.read_csv(dataset_path)
    fv = fv_df.loc[:, fv_df.columns != 'UUID']
    return fv.values.tolist()   

def get_tsne_feature_vectors(image_dir):
    dataset_path =  os.path.join(dirname, image_dir, TSNE )
    print('Fectching tsne from :: '+ dataset_path)
    fv_df = pd.read_csv(dataset_path)
    fv = fv_df.loc[:, fv_df.columns != 'UUID']
    return fv.values.tolist()

def get_all_saved_feature_vectors(image_dir):
    fv = get_feature_vectors(image_dir)
    pca = get_pca_feature_vectors(image_dir)
    tsne = get_tsne_feature_vectors(image_dir)
    return (fv,pca,tsne)    

def check_and_create_dir(model_dir):
    # Create target Directory if don't exist
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
        print("Directory " , model_dir ,  " Created ")
    else:    
        print("Directory " , model_dir ,  " already exists")


def save_dataset(image_dir,uuids,product_images):
    dataset_path = os.path.join(dirname, image_dir)
    check_and_create_dir(dataset_path)
    dataset_path = os.path.join(dirname, image_dir,image_dir+'.csv')

    Data = {}
    Data['UUID'] = uuids
    Data['Images'] = product_images
    data_frame = pd.DataFrame(Data, columns = ['UUID','Images'])

    print('Saving dataset ::' + dataset_path)
    data_frame.to_csv(dataset_path)

def save_feature_vectors(image_dir,uuids,feature_vector):
    dataset_path = os.path.join(dirname, image_dir)
    check_and_create_dir(dataset_path)
    dataset_path = os.path.join(dirname, image_dir,FEATURE_VECTOR)

    df = pd.DataFrame(feature_vector)
    df.insert(0,'UUID',uuids) 

    print('Saving dataset ::' + dataset_path)
    df.to_csv(dataset_path,index=False)

def save_pca(image_dir,uuids,pca):
    dataset_path = os.path.join(dirname, image_dir)
    check_and_create_dir(dataset_path)
    dataset_path = os.path.join(dirname, image_dir,PCA)

    df = pd.DataFrame(pca)
    df.insert(0,'UUID',uuids) 
    print('Saving dataset ::' + dataset_path)
    df.to_csv(dataset_path,index=False)

def save_tsne(image_dir,uuids,tsne):
    dataset_path = os.path.join(dirname, image_dir)
    check_and_create_dir(dataset_path)
    dataset_path = os.path.join(dirname, image_dir,TSNE)

    df = pd.DataFrame(tsne)
    df.insert(0,'UUID',uuids) 
    print('Saving dataset ::' + dataset_path)
    df.to_csv(dataset_path,index=False)