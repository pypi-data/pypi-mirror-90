import os
from PIL import Image


class ImageInspector(object):

    def __init__(self, img):
        self.is_img = os.path.isfile(img)
        if self.is_img:
            self.img = img
            try:
                self.open = self.open(self.img)
                self.stat = self.stat(self.img)
            except FileNotFoundError as e:
                print(e)

    @staticmethod
    def open(img):
        return Image.open(img)

    @staticmethod
    def stat(img):
        return os.stat(img)

    def process_name(self):
        names = self.img.split(".")
        return names

    def valid_name(self):
        return str(self.process_name()[0] + '.' + self.process_name()[-1])
