import numpy as np
import argparse

from utils.process import smooth_2d
from utils.plot import load_image, show_corners
from utils.process import rgb_to_gray


class HarrisCornerDetector:
    def __init__(self, sigma, k, threshold):
        self.sigma = sigma
        self.k = k
        self.threshold = threshold

    def detect(self, img_gray):
        # Compute gradients
        Ix, Iy = np.gradient(img_gray)

        # Compute components for R matrix
        Ix2 = Ix ** 2
        Iy2 = Iy ** 2
        IxIy = Ix * Iy

        Ix2 = smooth_2d(Ix2, self.sigma)
        Iy2 = smooth_2d(Iy2, self.sigma)
        IxIy = smooth_2d(IxIy, self.sigma)

        # R = det(A) - k * trace(A)^2
        detA = Ix2 * Iy2 - IxIy ** 2
        traceA = Ix2 + Iy2
        R = detA - self.k * traceA ** 2

        # Check for local maxima within 8-neighbourhood
        candidates = []

        for y in range(1, R.shape[0] - 1):
            for x in range(1, R.shape[1] - 1):
                neighbours = [R[y-1, x-1], R[y-1, x], R[y-1, x+1], R[y, x-1], R[y, x+1], R[y+1, x-1], R[y+1, x], R[y+1, x+1]]

                # Consider only if center pixel is greater than all its neighbours
                if R[y, x] > np.max(neighbours):
                    # Perform 4-neighbourhood quadratic approximation
                    a = (R[y, x-1] + R[y, x+1] - 2 * R[y, x]) / 2               # a = [f(-1, 0) + f(1, 0) - 2 * f(0, 0)] / 2
                    b = (R[y-1, x] + R[y+1, x] - 2 * R[y, x]) / 2               # b = [f(0, -1) + f(0, 1) - 2 * f(0, 0)] / 2
                    c = (R[y, x+1] - R[y, x-1]) / 2                             # c = [f(1, 0) - f(-1, 0)] / 2
                    d = (R[y+1, x] - R[y-1, x]) / 2                             # d = [f(0, 1) - f(0, -1)] / 2
                    e = R[y, x]                                                 # e = f(0, 0)

                    dx = -c / (2 * a)                                           # x = - c / 2a
                    dy = -d / (2 * b)                                           # y = - d / 2b
                    r = a * dx ** 2 + b * dy ** 2 + c * dx + d * dy + e         # f(x, y) = ax^2 + by^2 + cx + dy + e

                    candidates.append((x + dx, y + dy, r))

        # Discard weak corners
        corners = []

        for x, y, r in candidates:
            if r > self.threshold:
                corners.append((x, y, r))

        return corners


if __name__ == "__main__" :
    arg_parser = argparse.ArgumentParser(description = "Harris Corner Detector")
    arg_parser.add_argument("-i", "--image", type = str,
                        help = "file path of the input color JPEG image")
    arg_parser.add_argument("-s", "--sigma", type = float, default = 1.0,
                        help = "sigma value for Gaussain filter (default = 1.0)")
    arg_parser.add_argument("-k", "--kappa", type = float, default = 0.04,
                        help = "kappa value for R matrix (default = 0.04)")
    arg_parser.add_argument("-t", "--threshold", type = float, default = 1e6,
                        help = "threshold value for corner detection (default = 1e6)")
    args = arg_parser.parse_args()

    hcd = HarrisCornerDetector(args.sigma, args.kappa, args.threshold)
    img_color = load_image(args.image)
    img_gray = rgb_to_gray(img_color)

    corners = hcd.detect(img_gray)
    show_corners(img_color, corners)
