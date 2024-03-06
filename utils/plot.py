import matplotlib.pyplot as plt


def load_image(file_path):
    try:
        img_color = plt.imread(file_path)
        return img_color
    except:
        print("Error: Could not load image from file path.")


def show_corners(img_color, corners):
    x = []
    y = []

    for corner in corners:
        x.append(corner[0])
        y.append(corner[1])

    plt.ion()
    plt.figure("Harris Corner Detector")
    plt.imshow(img_color)
    plt.plot(x, y, "r+", markersize=5)
    plt.ioff()
    plt.show()
