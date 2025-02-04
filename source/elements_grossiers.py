import cv2
from cv2.typing import MatLike
import numpy as np
from matplotlib import pyplot as plt

# ___PARAMETRES___

# Emplacement de l'image à analyser en mémoire
image_path = '~/Projet3A/F57084r.jpg'

# Liste des noms des canaux du format HSV pour chaque index
channel_names = ['Hue', 'Saturation', 'Value']

# Si True, alors on applique un filtre de suppression d'ombres au canal de valeur
shadow_free_value: bool = True

# Si True, alors on applique un filtre maximum au canal de saturation
max_filter_saturation: bool = False

# Seuils minimaux et maximaux pour les différents contrastes et chaque canal HSV
low_contrast_thresh = [(0, 30), (0, 200), (0, 220)]
med_contrast_thresh = [(30, 120),(0, 50),(0, 150)]
high_contrast_thresh = [(120, 170), (0, 150), (0, 130)]

# Noyaux du filtre de flou Gaussien pour chaque canal HSV
kernel_sizes : list = [2 * 7 + 1, 2 * 2 + 1, 2 * 10 + 1]

# ___FONCTIONS___

def unshadow(
        channel: MatLike,
        shadow_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    ) -> MatLike:
    """
    Supprime les ombres du canal de valeur.
    Utilise une fermeture morphologique pour estimer l'arrière-plan lumineux et 
    le divise ensuite pour normaliser l'image.

    Paramètres:
    - channel: MatLike, canal d'image à traiter.
    - shadow_kernel: noyau de structuration pour l'opération morphologique.

    Retour:
    - MatLike: canal traité sans ombres.
    """
        
    # Opérations morphologiques
    background = cv2.morphologyEx(channel, cv2.MORPH_CLOSE, shadow_kernel)

    # Normalisation de l'image
    shadow_free = cv2.divide(channel, background, scale=255)
    return shadow_free

def max_filter(
        channel: MatLike,
        max_kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    ) -> MatLike:
    """
    Applique un filtre maximum au canal de saturation pour renforcer les contrastes
    entre les petits objets et la matrice du sol.

    Paramètres:
    - channel: MatLike, canal d'image à traiter.
    - max_kernel: noyau de structuration pour la dilatation.

    Retour:
    - MatLike: canal filtré.
    """
    max_filtered = cv2.dilate(channel, max_kernel)
    # Normalisation de l'image filtrée
    max_filtered = cv2.normalize(max_filtered, None, 0, 255, cv2.NORM_MINMAX) 
    return max_filtered

def preprocessing(image_hsv: MatLike) -> list[MatLike]:
    """
    Prétraite les canaux HSV de l'image : suppression d'ombres, filtrage 
    maximum et flou gaussien.

    Paramètres:
    - image_hsv: MatLike, image en format HSV.

    Retour:
    - list[MatLike]: liste des canaux prétraités.
    """
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

def threshold_segmentation(split_hsv: list[MatLike]) -> tuple[list[MatLike]]:
    """
    Effectue une segmentation binaire de chaque canal HSV en fonction des seuils
    pour différents niveaux de contraste.

    Paramètres:
    - split_hsv: liste des canaux prétraités.

    Retour:
    - tuple[list[MatLike]]: masques binaires pour les contrastes faible, moyen et fort.
    """
    low_contrast_masks: list[MatLike] = []
    med_contrast_masks: list[MatLike] = []
    high_contrast_masks: list[MatLike] = []

    for i in range(3):      
        '''
        NOTE Looking at the results, it might be better to take the logical opposite 
        for low contrast rfs and for the value channel altogether
        '''
        low_contrast_masks += [cv2.inRange(split_hsv[i], low_contrast_thresh[i][0], low_contrast_thresh[i][1])]
        med_contrast_masks += [cv2.inRange(split_hsv[i], med_contrast_thresh[i][0], med_contrast_thresh[i][1])]
        high_contrast_masks += [cv2.inRange(split_hsv[i], high_contrast_thresh[i][0], high_contrast_thresh[i][1])]

        return (low_contrast_masks, med_contrast_masks, low_contrast_masks)

'''
NOTE D'après l'article prendre la réunion 
    du masque de teinte pour les roches à faible contraste
    du masque de saturation pour les roches à haut contraste
    du masque de valeur pour les roches à contraste moyen.
Mais les résultats ne sont pas très concluents.
'''
def post_processing(masks: tuple[list[MatLike]]) -> MatLike:
    """
    Combine les masques produits par la segmentation pour identifier les fragments rocheux.

    Paramètres:
    - masks: tuple contenant les masques pour les contrastes faible, moyen et fort.

    Retour:
    - MatLike: masque combiné des fragments rocheux.
    """
    low_contrast_masks, med_contrast_masks, high_contrast_masks = masks 
    
    #TODO trouver les bonnes opérations à mener
    
    return np.logical_not(low_contrast_masks[0])

def get_rock_frag_mask(image_hsv: MatLike) -> MatLike:
    """
    Génère un masque binaire pour les fragments rocheux à partir d'une image HSV.

    Cette fonction effectue plusieurs étapes pour identifier les fragments rocheux :
    1. Prétraitement de l'image en séparant et filtrant les canaux HSV.
    2. Segmentation à l'aide de seuils prédéfinis pour détecter les fragments 
    de différents contrastes.
    3. Post-traitement pour combiner les masques de segmentation et obtenir 
    une détection finale des fragments rocheux.

    Paramètres :
    - image_hsv (MatLike) : Image source au format HSV.

    Retour :
    - MatLike : Masque binaire où les pixels correspondant aux fragments rocheux 
    sont marqués en blanc (True) et les autres en noir (False).

    Exemple :
    ```
    rock_mask = get_rock_frag_mask(image_hsv)
    cv2.imshow("Masque des fragments rocheux", rock_mask)
    ```
    """
    split_hsv: list[MatLike] = preprocessing(image_hsv)
    rock_masks = threshold_segmentation(split_hsv)
    return post_processing(rock_masks)

# ___EXEMPLE___
if __name__ == "__main__":
    # Lecture de l'image au format BGR
    image_bgr = cv2.imread(image_path)
    # Conversion de l'image vers le format HSV
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Prétraitement et segmentation
    rock_mask = get_rock_frag_mask(image_hsv)
    print("Segmentation finie.\n")
    cv2.imshow("Masque des fragments rocheux", rock_mask)