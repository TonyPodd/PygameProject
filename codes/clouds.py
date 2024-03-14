import random 
from config import *

class Cloud():
    def __init__(self, pos, img, speed, depth) -> None:
        self.pos = list(pos).copy()
        self.img = img
        self.speed = speed
        self.depth = depth
        
    def update(self):
        self.pos[0] -= self.speed
        
    def render(self, surf, scroll):
        render_pos = (self.pos[0] - scroll[0] * self.depth, self.pos[1] - scroll[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height() - BORDER_SKY))
        


    
class Clouds():
    def __init__(self, cloud_images, count = 10) -> None:
        self.clouds = []
        
        for _ in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.3, random.random() * 0.06 + 0.1))
            
        self.clouds.sort(key=lambda cloud: cloud.depth)
        
    def update(self):
        for cloud in self.clouds:
            cloud.update()
            
    def render(self, surf, scroll = (0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, scroll)