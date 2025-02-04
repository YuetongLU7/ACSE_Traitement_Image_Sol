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
    # Lecture de l'image au format BGR
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print(f"Erreur : Impossible de charger l'image à l'emplacement {image_path}")
        exit(1)

    # Conversion de l'image vers le format HSV
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    rock_final_mask = get_rock_frag_mask(image_hsv)

    print("Segmentation finie.\n")

    # Pour le moment on utilise un postiche pour le masque délimitant le plan du profil
    profile_mask: MatLike = np.full(rock_final_mask.shape, True, dtype=bool)

    rock_density = (density(profile_mask, rock_final_mask) * 100.0) # en %
    print(f'La densité des éléments grossiers sur le profil est {rock_density:.2f}%')
