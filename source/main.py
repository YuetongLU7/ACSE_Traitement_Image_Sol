import os
from elements_grossiers import *

# Emplacement de l'image à analyser en mémoire
image_path = '/home/jidoex/Projet3A/F57084r.jpg'

def density(profile_mask: MatLike, element_mask: MatLike) -> float:
    """
    Calcule la densité des éléments grossiers (fragments rocheux) sur une zone donnée du profil de sol.

    Paramètres :
    - profile_mask (MatLike) : masque booléen représentant l'ensemble du profil analysé.
    - element_mask (MatLike) : masque booléen représentant les éléments grossiers identifiés.

    Retour :
    - float : Densité des éléments grossiers exprimée en pourcentage.
    """
    element_count = np.count_nonzero(np.logical_and(profile_mask, element_mask))
    profile_count = np.count_nonzero(profile_mask)
    return element_count / profile_count

if __name__ == "__main__":

    images_path = os.getcwd() + "/images"

    for _, _, files in os.walk(images_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.JPG'):
                image_path = os.path.join(images_path, file)
                image_bgr = cv2.imread(image_path)
                image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

                rock_final_mask = get_rock_frag_mask(image_hsv) # save it after that
                profile_mask: MatLike = np.full(rock_final_mask.shape, True, dtype=bool)

                rock_density = (density(profile_mask, rock_final_mask) * 100.0) # en %

                print(f'{file} : {rock_density:.2f}%')

                bool_to_int = np.vectorize(lambda b: 255 if b else 0)
                rock_final_mask = bool_to_int(rock_final_mask)
                cv2.imwrite(images_path + '/' + file.split('.')[0] + '_mask.jpg', rock_final_mask)