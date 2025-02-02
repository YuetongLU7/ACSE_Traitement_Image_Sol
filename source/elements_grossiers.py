import cv2
from cv2.typing import MatLike
import numpy as np
from matplotlib import pyplot as plt

# ___PARAMETRES___

# Emplacement de l'image à analyser en mémoire
image_path = '~/Projet3A/F57084r.jpg'

# Liste des noms des canaux du format HSV pour chaque index
channel_names = ['Hue', 'Saturation', 'Value']

'''
Si True, alors on applique un filtre de suppression d'ombres 
au canal de valeur
True par défaut
'''
shadow_free_value: bool = True

'''
Si True, alors on applique un filtre maximum
au canal de saturation
False par défaut
'''
max_filter_saturation: bool = False

'''
Seuils minimaux et maximaux pour les éléments de contrastes différents
Et pour chaque canaux
Valeur des seuils trouvés dans l'article
'''
low_contrast_thresh = [(0, 30), (0, 200), (0, 220)]
med_contrast_thresh = [(30, 120),(0, 50),(0, 150)]
high_contrast_thresh = [(120, 170), (0, 150), (0, 130)]

# Noyaux du filtre de flou Gaussien pour chaque canal HSV
kernel_sizes : list = [2 * 7 + 1, 2 * 2 + 1, 2 * 10 + 1]

# ___FONCTIONS___

# Efface les ombres du canal de valeur
def unshadow(
        channel: MatLike,
        shadow_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    ) -> MatLike:
    # Morphological operations
    background = cv2.morphologyEx(channel, cv2.MORPH_CLOSE, shadow_kernel)

    # Normalize image to remove shadows
    shadow_free = cv2.divide(channel, background, scale=255)
    return shadow_free

'''
On applique un filtre maximum au canal de saturation 
pour augmenter le contraste entre les petits objets et la matrice du sol
''' 
def max_filter(
        channel: MatLike,
        max_kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    ) -> MatLike:
    max_filtered = cv2.dilate(channel, max_kernel)
    max_filtered = cv2.normalize(max_filtered, None, 0, 255, cv2.NORM_MINMAX) # optional
    return max_filtered

def preprocessing(image_hsv: MatLike) -> list[MatLike]:
    # Séparation des canaux teinte, saturation et valeur
    hue, saturation, value = cv2.split(image_hsv)
    split_hsv = [hue, saturation, value]

    # Suppression des ombres du canal de valeur
    if shadow_free_value:
        split_hsv[2] = unshadow(value)

    if max_filter_saturation:
        split_hsv[1] = max_filter(saturation)

    # Application d'un filtre Gaussien à chacun des canaux
    for i in range(len(split_hsv)):
        split_hsv[i] = cv2.GaussianBlur(split_hsv[i], (kernel_sizes[i], kernel_sizes[i]), 0)
    
    return split_hsv

# Segmentation binaire de l'image à l'aide des seuils donnés dans l'article
def threshold_segmentation(split_hsv: list[MatLike]) -> tuple[list[MatLike]]:
    low_contrast_masks: list[MatLike] = []
    med_contrast_masks: list[MatLike] = []
    high_contrast_masks: list[MatLike] = []

    for i in range(3):      
        '''
        Looking at the results, it might be better to take the logical opposite 
        for low contrast rfs and for the value channel altogether
        '''
        low_contrast_masks += [cv2.inRange(split_hsv[i], low_contrast_thresh[i][0], low_contrast_thresh[i][1])]
        med_contrast_masks += [cv2.inRange(split_hsv[i], med_contrast_thresh[i][0], med_contrast_thresh[i][1])]
        high_contrast_masks += [cv2.inRange(split_hsv[i], high_contrast_thresh[i][0], high_contrast_thresh[i][1])]

        return (low_contrast_masks, med_contrast_masks, low_contrast_masks)

'''
Rassemble les différents masques produits par la segmentation 
en un masque qui contiendrait tous les fragments rocheux.

D'après l'article prendre la réunion 
    du masque de teinte pour les roches à faible contraste
    du masque de saturation pour les roches à haut contraste
    du masque de valeur pour les roches à contraste moyen.
Mais les résultats ne sont pas très concluents.

TODO trouver les bonnes opérations à mener
'''
def post_segmentation(masks: tuple[list[MatLike]]) -> MatLike:
    low_contrast_masks, med_contrast_masks, high_contrast_masks = masks 
    
    #TODO
    
    return np.logical_not(low_contrast_masks[0])


# ___EXEMPLE___
if __name__ == "__main__":
    # Lecture de l'image au format BGR
    image_bgr = cv2.imread(image_path)
    # Conversion de l'image vers le format HSV
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    split_hsv: list[MatLike] = preprocessing(image_hsv)
    rock_masks = threshold_segmentation(split_hsv)

    print("Segmentation finie.\n")