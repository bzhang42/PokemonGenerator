from skimage.io import imread, imsave

def rgba_to_rgb(filename):
    print(f'Converting {filename}')
    img_rgba = imread(filename)
    # check that this is RGBA
    assert img_rgba.shape[-1] == 4
    # split RGB channels and alpha channel
    img_rgb, img_a = img_rgba[..., :3], img_rgba[..., 3]
    # make all fully transparent pixels white
    img_rgb[img_a == 0] = (255, 255, 255)
    imsave(f'{filename[:-4]}.jpg', img_rgb)
