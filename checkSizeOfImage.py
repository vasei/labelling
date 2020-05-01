import cv2
import os

def load_images_from_folder(folder):
    images = []
    i=496
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            height, width, channels = img.shape
            fname="C:/Users/shayanr/Desktop/tehran/lam/data/allData/"

            cv2.imwrite(fname+"/"+str(i)+".jpg", img)
            print(str(i)+".jpg")
            i=i+1


folderName="C:/Users/shayanr/Desktop/tehran/lateral series 2/"
load_images_from_folder(folderName)
print("End!")