from os import walk
from os.path import join

import pygame


def import_folder(path):
    surface_list = []
    # get files from inside the folder
    for _, __, img_files in walk(path):
        # for each filename
        for img in img_files:
            # define the full path name using the path and the image filename
            full_path = join(path, img)
            # load the image in and add it to the surface list
            img_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surf)

    return surface_list
