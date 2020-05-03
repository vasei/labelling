# import numpy as np
import cv2
import glob
from src.csvutils import read_label_file, write_label_file

global_image_data = {}


def add_point_label(event, x, y, flags, param):
    global global_image_data
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global_image_data['labels'].append(round(x / param["scale_factor"]))
        global_image_data['labels'].append(round(y / param["scale_factor"]))


def show_image_and_labels(image_address, image_data, image_number, total_images):
    # TODO: add graphical information like point-labelling/line-labelling/cropping states
    # TODO: add -1000px label button
    img = cv2.imread(image_address)
    height, width, channels = img.shape
    scale_factor = 500 / height
    resized_img = cv2.resize(img, (round(width * scale_factor), 500), interpolation=cv2.INTER_AREA)
    # window_name = str(image_number) + "/" + str(total_images)
    window_name = "image"

    cv2.namedWindow(window_name)

    global global_image_data
    global_image_data = image_data.copy()

    while 1:
        cv2.imshow(window_name, resized_img)
        # TODO: draw lines and crop area
        # TODO: draw label numbers instead of points

        # drawing label points
        for i in range(int(len(global_image_data['labels']) / 2)):
            cv2.circle(resized_img, (round(global_image_data['labels'][2 * i] * scale_factor),
                             round(global_image_data['labels'][2 * i + 1] * scale_factor)),
                       2, (255, 0, 0), -1)

        k = cv2.waitKey(20) & 0xFF
        if k == 27 or k == ord('a') or k == ord('d'):
            # cv2.destroyAllWindows()
            cv2.setMouseCallback(window_name, lambda *args: None)
            return k, global_image_data
        elif k == ord('r'):
            # TODO: clear labels here
            cv2.setMouseCallback(window_name, lambda *args: None)
            print("labels and crop area must be cleared")
        elif k == ord("p"):
            # point labelling
            cv2.setMouseCallback(window_name, add_point_label,
                                 param={
                                     "scale_factor": scale_factor
                                 })
        elif k == ord("l"):
            # TODO: add line with appropriate callback function
            cv2.setMouseCallback(window_name, lambda *args: None)
        elif k == ord("c"):
            # TODO: add crop area rectangle with appropriate callback function
            cv2.setMouseCallback(window_name, lambda *args: None)


i = 0
key = 1
images_folder = "../data/renamed/"
label_file = "../data/label.csv"
extension = ".jpeg"
image_names = glob.glob(images_folder + '*' + extension)
n = len(image_names)

data = read_label_file(label_file)

while key != 27:
    infile = image_names[i]
    picNumber = str(i) + ".jpg"
    image_name = infile.split("/")[-1]
    if image_name in data:
        image_data = data[image_name]
    else:
        image_data = {"labels": [], "lines": [], "crop": []}
    [key, modified_image_data] = show_image_and_labels(infile, image_data, i, n)
    data[image_name] = modified_image_data.copy()
    print(key)
    if key == ord('a') and i > 0:
        i -= 1
    elif key == ord('d') and i < n - 1:
        i += 1

cv2.destroyAllWindows()
write_label_file(label_file, data)
