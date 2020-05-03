# import numpy as np
import cv2
import glob


# TODO: Please use a csv file for labeling. In macOS or linux working with excel files is not so easy as windows.


def add_point_label(event, x, y, flags, param):
    # TODO: add point to the label file and draw it on image
    # global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(param[0], (x, y), 2, (255, 0, 0), -1)
        # mouseX, mouseY = x, y


def show_image_and_labels(image_address, label_file, image_number, total_images):
    img = cv2.imread(image_address)
    image_name = image_address.split("/")[-1]
    height, width, channels = img.shape
    scale_factor = 500 / height
    resized_img = cv2.resize(img, (round(width * scale_factor), 500), interpolation=cv2.INTER_AREA)
    # window_name = str(image_number) + "/" + str(total_images)
    window_name = "image"
    # TODO: read lebels from the label_file and draw them on the image
    cv2.namedWindow(window_name)
    # TODO: resize image to fit in window and pass necessary arguments to add label event function in order to adjust
    #  and y appropriately

    while 1:
        cv2.imshow(window_name, resized_img)
        k = cv2.waitKey(20) & 0xFF
        if k == 27 or k == ord('a') or k == ord('d'):
            # cv2.destroyAllWindows()
            cv2.setMouseCallback(window_name, lambda *args: None)
            return k
        elif k == ord('c'):
            cv2.setMouseCallback(window_name, lambda *args: None)
            print("labels and crop area must be cleared")
        elif k == ord("l"):
            cv2.setMouseCallback(window_name, add_point_label, param=[img, image_name, label_file, scale_factor])
        # TODO: add -1000px label
        # TODO: add line
        # TODO: add crop area rectangle


i = 0
key = 1
images_folder = "../data/renamed/"
label_file = "../data/label.csv"
extension = ".jpeg"
image_names = glob.glob(images_folder + '*' + extension)
n = len(image_names)
while key != 27:
    infile = image_names[i]
    picNumber = str(i) + ".jpg"
    key = show_image_and_labels(infile, label_file, i, n)
    print(key)
    if key == ord('a') and i > 0:
        i -= 1
    elif key == ord('d') and i < n - 1:
        i += 1
