import pygame as p
import os

# from config import *

PATH = "data/Treasure Hunters/"


def load_image(filename):
    img = p.image.load(PATH + filename).convert_alpha()
    rect = img.get_bounding_rect()
    trimmed_image = img.subsurface(rect)
    # print(trimmed_image.get_size(),filename)
    return img
    # img.set_colorkey(BLACK)


def load_images(filename):
    images = []
    for name in os.listdir(PATH + filename):
        images.append(load_image(filename + "/" + name))
    return images


class Animation:
    def __init__(self, images, duration, loop=True) -> None:
        self.images = images
        self.duration = duration
        self.loop = loop
        self.end = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.duration, self.loop)

    def update(self):
        if self.loop:
            try:
                self.frame = (self.frame + 1) % (self.duration * len(self.images))
            except:
                self.end = True
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame >= self.duration * len(self.images) - 1:
                self.end = True

    def img(self):
        return self.images[int(self.frame / self.duration)]


# print(sorted(["001", "002", "010"]))
