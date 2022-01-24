import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from keras.datasets import mnist
import pickle as pk


#charger le fichier mnist
def model_train():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    X_train = x_train.reshape(x_train.shape[0],-1)/255 #division par 255 pour avoir des valeurs entre 0 et 1
    X_test = x_test.reshape(x_test.shape[0],-1)/255
    model_knn = KNeighborsClassifier(metric='euclidean', n_neighbors=3)
    model_knn.fit(X_train, y_train)
    pd.to_pickle(model_knn,"data/model_knn.pkl")