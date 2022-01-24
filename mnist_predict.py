import numpy as np
import pandas as pd
from pathlib import Path

# Importer la fonction pour convertir l'image
from img_to_mnist import traitement_img

#importer le modèle
CUR_DIR = Path.cwd()
MODEL_DIR = CUR_DIR/"data"
MODEL_FIC = MODEL_DIR/"model_knn.pkl"

print(MODEL_FIC)

def predict_img(img):

    # les dimension standard d'une image mnist.
    height, width = 28, 28
    model_knn = pd.read_pickle(MODEL_FIC)
    # Traiter l'image (avec les fonctions du fichier  img_to_mnist.py) et la convertir en array
    X = traitement_img(img)
    X_array = np.array(X)

    # applatir l'image
    X_transform = X_array.reshape(1, height * width)

    #narmaliser l'image en 0 et 1 1 == blanc.
    X_transform = X_transform.astype('float32')
    X_transform /= 255


    # Obtenir la prédiction
    prediction = model_knn.predict(X_transform)

    return prediction[0]