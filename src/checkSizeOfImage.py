import cv2
import os


def load_images_from_folder(src_folder, dest_folder):
    # A similar method should be written for loading dicom images
    # images = []
    # i = 496
    hsh = cv2.img_hash.BlockMeanHash_create()
    for filename in os.listdir(src_folder):
        img = cv2.imread(os.path.join(src_folder, filename))
        if img is not None:
            # height, width, channels = img.shape
            # fname = "C:/Users/shayanr/Desktop/tehran/lam/data/allData/"

            image_hash = hsh.compute(img);
            new_name = ''.join(map(str, image_hash[0]))
            cv2.imwrite(dest_folder + "/" + new_name + ".jpeg", img)
            print(new_name + ".jpeg")
            # i = i + 1


# src_folder = "C:/Users/shayanr/Desktop/tehran/lateral series 2/"
# dest_folder = "C:/Users/shayanr/Desktop/tehran/lam/data/allData/"
src_folder = "../data/original"
dest_folder = "../data/renamed"
load_images_from_folder(src_folder, dest_folder)
print("End!")
