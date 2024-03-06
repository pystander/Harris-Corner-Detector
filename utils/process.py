import numpy as np
from scipy.ndimage import convolve1d


def rgb_to_gray(img_rgb):
    Y = np.array([0.299, 0.587, 0.114])
    img_gray = np.dot(img_rgb, Y)

    return img_gray


def smooth_1d(img_gray, sigma, n=3):
    x = np.arange(-n * sigma, n * sigma + 1)
    filter = np.exp(-x ** 2 / (2 * sigma ** 2))

    img_filtered = convolve1d(img_gray, filter, 1, np.float64, "constant")
    weight = convolve1d(np.ones_like(img_gray), filter, 1, np.float64, "constant")
    img_smoothed = img_filtered / weight

    return img_smoothed


def smooth_2d(img_gray, sigma, n=3):
    img_smoothed = smooth_1d(img_gray, sigma, n)
    img_smoothed = smooth_1d(img_smoothed.T, sigma, n).T

    return img_smoothed
