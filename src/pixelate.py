import cv2
import numpy as np


def sort_by_brightness(palette: np.uint8):
    """
    Sorts given color palette by brightness.
    
    https://stackoverflow.com/a/596241
    """
    
    luminosity = (
        0.2126 * palette[:, 2] + 0.7152 * palette[:, 1] + 0.0722 * palette[:, 0]
    )
    return palette[np.argsort(luminosity)]


def display_palette(palette: np.uint8, sort=True):
    """
    Generates an image displaying given color palette.
    """
    swatch_size = 100
    num_colors = palette.shape[0]
    palette_image = np.zeros((swatch_size, swatch_size * num_colors, 3), dtype=np.uint8)

    if sort:
        palette = sort_by_brightness(palette)

    for i, color in enumerate(palette):
        palette_image[:, i * swatch_size : (i + 1) * swatch_size] = color

    return palette_image


def extract_color_palette(img, k: int):
    """
    Extracts color palette from the given image using k-means clustering.
    """

    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    palette = np.uint8(centers)
    return palette, labels


def pixelate(img, pixel_size: int, blur=False, use_palette=False, k=8):
    """
    Pixelates an image by reducing its pixel resolution and optionally applying blur effect and color quantization.
    """

    palette = None
    if use_palette:
        palette, labels = extract_color_palette(img, k)
        res = palette[labels.flatten()]
        img = res.reshape((img.shape))
        palette = display_palette(palette, sort=True)

    if blur:
        img = cv2.blur(img, (7, 7))

    for i in range(0, img.shape[0], pixel_size):
        for j in range(0, img.shape[1], pixel_size):
            img[i : i + pixel_size, j : j + pixel_size] = img[i][j]

    return img, palette
