# Le format MNIST standard sont des images en niveaux de gris 28x28 avec 0 == noir.
# De plus, pour que la classification fonctionne correctement, le chiffre doit être centré à l'intérieur d'une case 20x20.
# Ces fonctions prennent un format d'image cv2 (RVB ou niveaux de gris) dans une taille et une position arbitraires
# et renvoie une image formatée comme ci-dessus.

from scipy import ndimage
import numpy as np
import math
import cv2

# Met à l'échelle l'image d'entrée en une image en niveaux de gris max_height * max_width
def converter(img, max_height, max_width):
    height, width = img.shape[:2]
    print(height,width)
    if max_height < height or max_width < width:
    # obtenir le facteur d'échelle
        scal_fact = max_height / float(height)
        if max_width/ float(width) < scal_fact:
            scal_fact = max_width / float(width)
            # resize image
        small = cv2.resize(img, (20,20), fx=scal_fact, fy=scal_fact, interpolation=cv2.INTER_AREA)
        small = 255 - small
        rows,cols = small.shape
        colsPad = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
        rowsPad = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
        small = np.lib.pad(small,(rowsPad,colsPad),'constant')
        return(small)
    else:
        print('Votre image est déjà plus petite que {} x {}'.format(max_height, max_width))
        return(img)

# Recadrer l'image (Se barrasser d'une partie de l'arrière-plan)
def recadrage(myImg):
    retval, thresh_gray = cv2.threshold(myImg, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

    # trouver où se trouve le chiffre et créer une zone autour
    points = np.argwhere(thresh_gray==0) # trouver où sont les pixels noirs
    points = np.fliplr(points) # stockez-les en coordonnées x, y au lieu d'indices de ligne, col
    x, y, w, h = cv2.boundingRect(points) # créer un rectangle autour de ces points
    #x, y, w, h = x-10, y-10, w+20, h+20 # agrandis un peu la zone
    crop = myImg[y:y+h, x:x+w] # créer une zone autour de l'image grise
    print(x,y,w,h)
    # recupérer les zones 
    retval, thresh_crop = cv2.threshold(crop, thresh=100, maxval=255, type=cv2.THRESH_BINARY)
    print(thresh_crop.shape)
    return thresh_crop

# Trouver le décalage vers le centre de l'image recadrée
def getCenterImg(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)
    return shiftx,shifty

# Décaler l'image de sx et sy
def centrer(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted

# traitement de l'image
def traitement_img(img):
    
    max_height = 28
    max_width = 28
    fig_small = converter(recadrage(img), max_height, max_width)
    shiftx, shifty = getCenterImg(fig_small)
    fig_shifted = centrer(fig_small, shiftx, shifty)
    return fig_shifted