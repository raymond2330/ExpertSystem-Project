from PIL import Image
import os.path, sys

path = os.path.join(os.getcwd(), 'FullScreenImages')
dirs = os.listdir(path)
size = (0, 0, 26, 42)

def crop():
    for item in dirs:
        fullpath = os.path.join(path,item)         #corrected
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            imCrop = im.crop(size) #corrected
            imCrop.save(os.getcwd() + '\\CroppedImages\\' + item, "PNG", quality=100)

crop()