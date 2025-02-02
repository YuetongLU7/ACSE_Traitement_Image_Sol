from elements_grossiers import *

# Emplacement de l'image à analyser en mémoire
image_path = '/home/jidoex/Projet3A/F57084r.jpg'

def density(profile_mask: MatLike, element_mask: MatLike) -> float:
    element_count = np.count_nonzero(np.logical_and(profile_mask, element_mask))
    profile_count = np.count_nonzero(profile_mask)
    return element_count / profile_count

if __name__ == "__main__":
    # Lecture de l'image au format BGR
    image_bgr = cv2.imread(image_path)
    # Conversion de l'image vers le format HSV
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    split_hsv: list[MatLike] = preprocessing(image_hsv)
    rock_masks = threshold_segmentation(split_hsv)

    rock_final_mask = post_segmentation(rock_masks)

    print("Segmentation finie.\n")

    ''' 
    TODO 
    Puisqu'il n'y a toujours pas de module 
    permettant d'obtenir la forme exacte du profil,
    On considère l'entièreté de l'image
     '''
    profile_mask: MatLike = np.full(split_hsv[0].shape, True, dtype=bool)
    rock_density = (density(profile_mask, rock_final_mask) * 100.0) # in %

    print(f'La densité des éléments grossiers sur le profil est {rock_density:.2f}%')
