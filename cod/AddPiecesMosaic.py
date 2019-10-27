from cod.Parameters import *
import numpy as np
import pdb
import timeit

def get_sorted_idx(mean_color_images, mean_color):
    dist = np.sum((mean_color_images - mean_color) **2, axis =1)
    return np.argsort(dist)

def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                index = np.random.randint(low=0, high=N, size=1)
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':
        mean_color_images = np.mean(params.small_images,axis=(1,2))
        vecini = np.zeros((params.num_pieces_vertical, params.num_pieces_horizontal), np.float32)
        for y in range(params.num_pieces_vertical):
            for x in range(params.num_pieces_horizontal):
                patch = params.image_resized[y * H: (y + 1) * H, x * W: (x + 1) * W]
                mean_color = patch.mean(axis=(0, 1))
                idx = get_sorted_idx(mean_color_images,mean_color)
                if y == 0 and x == 0:
                    img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[0]]
                    vecini[y,x] = idx[0]
                elif y == 0:
                    if vecini[y][x-1] == idx[0]:
                        img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[1]]
                        vecini[y][x] = idx[1]
                    else:
                        vecini[y][x] = idx[0]
                        img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[0]]
                elif x == 0:
                    if vecini[y-1][x] == idx[0]:
                        img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[1]]
                        vecini[y, x] = idx[1]
                    else:
                        img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[0]]
                        vecini[y, x] = idx[0]
                elif x > 0 and y > 0:
                    pos = 0
                    while idx[pos] in [vecini[y-1, x], vecini[y, x-1]]:
                        pos += 1
                    img_mosaic[y * H: (y + 1) * H, x * W: (x + 1) * W] = params.small_images[idx[pos]]
                    vecini[y, x] = idx[pos]
        pass
    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_random(params: Parameters):
    start_time = timeit.default_timer()
    N, H, W, C = params.small_images.shape
    img_mosaic = np.zeros([params.image_resized.shape[0]+H, params.image_resized.shape[1]+W,3])
    print(params.image_resized.shape)
    print(img_mosaic.shape)
    h, w, c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    free_pixels = np.zeros([img_mosaic.shape[0], img_mosaic.shape[1]])
    free_pixels[-H:, :] = -1
    free_pixels[:, -W:] = -1
    mean_color_images = np.mean(params.small_images, axis=(1, 2))
    while True:
        free = free_pixels[free_pixels > -1]
        idH = np.random.randint(0,params.num_pieces_vertical)
        idW = np.random.randint(0,params.num_pieces_horizontal)
        if(free_pixels[idH][idW] == -1):
            continue
        else:
            patch = params.image_resized[idH * H: (idH + 1) * H, idW * W: (idW + 1) * W]
            mean_color = patch.mean(axis=(0, 1))
            idx = get_sorted_idx(mean_color_images, mean_color)
            img_mosaic[idH * H: (idH + 1) * H, idW * W: (idW + 1) * W] = params.small_images[idx[0]]
            free_pixels[idH*H:(idH+1)*H, idW*W:(idW+1)*W] = -1
        if free.shape[0] == 0:
            break
    return img_mosaic


def add_pieces_hexagon(params: Parameters):
    return None
