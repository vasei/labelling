# import numpy as np
import cv2
import glob
from src.csvutils import read_label_file, write_label_file

global_image_data = {}


def add_point_label(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global global_image_data
        print("add point", x, y)
        global_image_data['labels'].append(round(x / param["scale_factor"]))
        global_image_data['labels'].append(round(y / param["scale_factor"]))


def add_line_label(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global global_image_data
        print("add line", x, y)
        global_image_data['lines'].append(round(x / param["scale_factor"]))
        global_image_data['lines'].append(round(y / param["scale_factor"]))


def add_rectangle_label(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global global_image_data
        print("add rect", x, y)
        global_image_data['crop'].append(round(x / param["scale_factor"]))
        global_image_data['crop'].append(round(y / param["scale_factor"]))


def show_image_and_labels(image_address, image_data, image_number, total_images):
    # TODO: add graphical information like point-labelling/line-labelling/cropping states
    # TODO: add -1000px label button
    img = cv2.imread(image_address)
    height, width, channels = img.shape
    scale_factor = 600 / height
    resized_img = cv2.resize(img, (round(width * scale_factor), 600), interpolation=cv2.INTER_AREA)
    # window_name = str(image_number) + "/" + str(total_images)
    window_name = "image"

    cv2.namedWindow(window_name)

    global global_image_data
    global_image_data = image_data.copy()

    while 1:
        cv2.imshow(window_name, resized_img)

        # drawing label points
        for i in range(int(len(global_image_data['labels']) / 2)):
            point_x = round(global_image_data['labels'][2 * i] * scale_factor)
            point_y = round(global_image_data['labels'][2 * i + 1] * scale_factor)
            cv2.circle(resized_img, (point_x, point_y),
                       2, (255, 0, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottom_left_corner_of_text = (point_x, point_y)
            font_scale = .5
            font_color = (0, 150, 150)
            line_type = 2

            cv2.putText(resized_img, str(i),
                        bottom_left_corner_of_text,
                        font,
                        font_scale,
                        font_color,
                        line_type)
        # start and end of line
        for i in range(int(len(global_image_data['lines']) / 2)):
            cv2.circle(resized_img, (round(global_image_data['lines'][2 * i] * scale_factor),
                                     round(global_image_data['lines'][2 * i + 1] * scale_factor)),
                       2, (0, 0, 255), -1)
        # line
        for i in range(int(len(global_image_data['lines']) / 4)):
            start_point = (round(global_image_data['lines'][4 * i] * scale_factor),
                           round(global_image_data['lines'][4 * i + 1] * scale_factor))
            end_point = (round(global_image_data['lines'][4 * i + 2] * scale_factor),
                         round(global_image_data['lines'][4 * i + 3] * scale_factor))
            cv2.line(resized_img, start_point, end_point, (0, 0, 255), 2)

        # start and end of crop
        for i in range(int(len(global_image_data['crop']) / 2)):
            cv2.circle(resized_img, (round(global_image_data['crop'][2 * i] * scale_factor),
                                     round(global_image_data['crop'][2 * i + 1] * scale_factor)),
                       2, (255, 255, 0), -1)
        # line
        for i in range(int(len(global_image_data['crop']) / 4)):
            start_point = (round(global_image_data['crop'][4 * i] * scale_factor),
                           round(global_image_data['crop'][4 * i + 1] * scale_factor))
            end_point = (round(global_image_data['crop'][4 * i + 2] * scale_factor),
                         round(global_image_data['crop'][4 * i + 3] * scale_factor))
            cv2.rectangle(resized_img, start_point, end_point, (255, 255, 0), 2)

        k = cv2.waitKey(20) & 0xFF
        if k == 27 or k == ord('a') or k == ord('d'):
            # cv2.destroyAllWindows()
            cv2.setMouseCallback(window_name, lambda *args: None)
            return k, global_image_data
        elif k == ord('r'):
            # TODO: clear labels here
            cv2.setMouseCallback(window_name, lambda *args: None)
        elif k == ord("p"):
            # point labelling
            cv2.setMouseCallback(window_name, add_point_label,
                                 param={
                                     "scale_factor": scale_factor
                                 })
        elif k == ord("l"):
            cv2.setMouseCallback(window_name, add_line_label,
                                 param={
                                     "scale_factor": scale_factor
                                 })
        elif k == ord("c"):
            cv2.setMouseCallback(window_name, add_rectangle_label,
                                 param={
                                     "scale_factor": scale_factor
                                 })
        elif k == ord("n"):
            # TODO: go to next image with no point labels
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
    # print(key)
    if key == ord('a') and i > 0:
        i -= 1
    elif key == ord('d') and i < n - 1:
        i += 1

cv2.destroyAllWindows()
write_label_file(label_file, data)
