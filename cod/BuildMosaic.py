import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import  pdb

from cod.AddPiecesMosaic import *
from cod.Parameters import *


def load_pieces(params: Parameters):
    # citeste toate cele N piese folosite la mozaic din directorul corespunzator
    # toate cele N imagini au aceeasi dimensiune H x W x C, unde:
    # H = inaltime, W = latime, C = nr canale (C=1  gri, C=3 color)
    # functia intoarce pieseMozaic = matrice H x W x C x N in params
    # pieseMoziac(:,:,:,i) reprezinta piesa numarul i
    images = []
    files = os.listdir(params.small_images_dir)
    for file in files:
        img = cv.imread(os.path.join(params.small_images_dir, file))
        images.append(img)
    images = np.array(images,np.float32)
    print(images.__len__())
    # citeste imaginile din director
    print(params.show_small_images)
    if params.show_small_images:
        print("intra")
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RBG format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)
        plt.show()

    params.small_images = images


def compute_dimensions(params: Parameters):
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni
    # ca mozaicul

    # completati codul
    # calculeaza automat numarul de piese pe verticala
    small_images_height, small_images_width = params.small_images[0].shape[0], params.small_images[0].shape[1]
    aspect_ratio = params.image.shape[1]/params.image.shape[0]
    new_height = params.image.shape[0] * small_images_height
    new_width = new_height * aspect_ratio
    print(new_height,new_width)
    params.num_pieces_vertical = round(new_height/small_images_height)
    params.num_pieces_horizontal = round(new_width/small_images_width)
    print(params.num_pieces_horizontal,params.num_pieces_vertical)
    # redimensioneaza imaginea
    params.image_resized = cv.resize(params.image, (int(new_width), int(new_height)))
    cv.waitKey(0)

def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)

    img_mosaic = None
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)

    return img_mosaic
