from config import *
import pygame as p
import csv
from codes.vspom import Animation
# from сщвуыvspom import Animation

class TileMap():
    def __init__(self, game, size : int = 32) -> None:
        self.size = size
        self.tilemap = {}
        self.palms_top = {}
        self.decormap_back = {}
        self.decormap_front = {}
        self.enemy_spawner = {}
        self.spawnersmap = {}
        self.offgrid_tiles = []
        self.game = game
        self.DATA = [self.tilemap, self.palms_top, self.decormap_back, self.decormap_front, self.spawnersmap]
       
        
    def load_level(self, scv):
        data = []
        with open(scv) as f:
            reader = csv.reader(f, delimiter=',')
            data.append(list(reader))
        data = data[0]    
            
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '-1':
                    variant = int(data[y][x]) - 48
                    if variant <= 46:
                        self.tilemap[str(x) + ';' + str(y)] = {'type': 'blocks', 'variant': variant, 'pos': (x, y)}
                    elif variant == 47:
                        self.tilemap[str(x) + ';' + str(y)] = {'type': 'blocks', 'variant': variant, 'pos': (x, y)}
                        
                        
    def load_palms_top(self, scv):
        data = []
        with open(scv) as f:
            reader = csv.reader(f, delimiter=',')
            data.append(list(reader))
        data = data[0]    
            
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '-1':
                    variant = int(data[y][x])
                    self.palms_top[str(x) + ';' + str(y)] = {'type': 'blocks', 'variant': variant, 'pos': (x, y), 'anim' : self.game.assets['palm_front']}
                    
    def load_decor_front(self, scv):
        data = []
        with open(scv) as f:
            reader = csv.reader(f, delimiter=',')
            data.append(list(reader))
        data = data[0]    
            
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '-1':
                    variant = int(data[y][x])
                    if variant > 100: continue
                    self.decormap_front[str(x) + ';' + str(y)] = {'type': 'decor', 'variant': variant - 14, 'pos': (x, y)}
                    
    def load_palms_back(self, scv):
        data = []
        with open(scv) as f:
            reader = csv.reader(f, delimiter=',')
            data.append(list(reader))
        data = data[0]    
            
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '-1':
                    variant = int(data[y][x])
                    if variant > 100: continue
                    self.decormap_back[str(x) + ';' + str(y)] = {'type': 'blocks', 'variant': variant, 'pos': (x, y), 'anim' : self.game.assets[f'palm_back_{variant-12}']}
    
    
    def load_enemyes(self, scv):
        data = []
        with open(scv) as f:
            reader = csv.reader(f, delimiter=',')
            data.append(list(reader))
        data = data[0]    
            
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '-1':
                    variant = int(data[y][x])
                    if variant > 10: continue
                    self.enemy_spawner[str(x) + ';' + str(y)] = {'type': 'spawner', 'variant': int(variant), 'pos': (x, y)}
    

        
    
    def around(self, pos):
        return_tiles = []
        loc = (int(pos[0] // self.size), int(pos[1] // self.size))
        for offset in OFFSET:
            check = str(loc[0] + offset[0]) + ";" +  str(loc[1] + offset[1])
            for map in self.DATA:
                if check in map:                      
                    return_tiles.append(map[check])
        return return_tiles
    
    def physics_block_around(self, pos):
        # print(23)
        return_tiles = []
        for tile in self.around(pos):
            if tile['type'] in PHYSICS_TYPES:
                return_tiles.append((p.Rect(tile['pos'][0] * self.size, tile['pos'][1] * self.size, self.size, self.size)))
        return return_tiles
        
    def solid_check(self, pos):
        loc = (int(pos[0] // self.size), int(pos[1] // self.size))
        check = str(loc[0]) + ";" +  str(loc[1])
        if check in self.tilemap:
            if self.tilemap[check]['type'] in PHYSICS_TYPES:
                return self.tilemap[check]
        return False
                
    def render(self, surf, scroll = (0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - scroll[0], tile['pos'][1] - scroll[1]))
        
        for x in range(scroll[0] // self.size, (scroll[0] + surf.get_width()) // self.size + 1):
            for y in range(scroll[1] // self.size, (scroll[1] + surf.get_height()) // self.size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.decormap_back:
                    tile = self.decormap_back[loc]
                    tile['anim'].update()
                    surf.blit(tile['anim'].img(), (tile['pos'][0] * self.size - scroll[0], tile['pos'][1] * self.size - scroll[1])) 
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['variant'] == 47:
                        self.game.assets['finish'].update()
                        surf.blit(self.game.assets['finish'].img(), (tile['pos'][0] * self.size - scroll[0], tile['pos'][1] * self.size - scroll[1]))
                    else:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.size - scroll[0], tile['pos'][1] * self.size - scroll[1]))
                if loc in self.decormap_front:
                    tile = self.decormap_front[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.size - scroll[0], tile['pos'][1] * self.size - scroll[1]))
                if loc in self.palms_top:
                    tile = self.palms_top[loc]
                    tile['anim'].update()
                    surf.blit(tile['anim'].img(), (tile['pos'][0] * self.size - scroll[0] -3, tile['pos'][1] * self.size - scroll[1]))
 
        