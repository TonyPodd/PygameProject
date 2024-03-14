import pygame as p
from config import *
from codes.particles import Partiсle
import random

class Entity:
    def __init__(self, parent, typ, pos, size):
        self.game = parent
        self.pos = list(pos).copy()
        self.size = list(size).copy()
        self.velocity = [0, 0]
        self.img = self.game.assets[typ]
        self.collisions = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.type = typ
        self.have_sword = False

        self.action = ""
        self.set_action("idle")

        self.part_type = ""
        self.set_particles("idle")

        self.anim_offset = (0, 0)
        self.flip = False

    def rect(self):
        return p.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def update(self, tilemap, movement=(0, 0), gv = True):
        frame_move = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.collisions = {"up": 0, "down": 0, "left": 0, "right": 0}

        self.pos[0] += frame_move[0]
        entity_rect = self.rect()

        for rect in tilemap.physics_block_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_move[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = 1

                if frame_move[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = 1

                self.pos[0] = entity_rect.x

        if gv:
            if movement[0] > 0:
                self.flip = False
            elif movement[0] < 0:
                self.flip = True

        self.pos[1] += frame_move[1]
        entity_rect = self.rect()

        for rect in tilemap.physics_block_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_move[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = 1

                if frame_move[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = 1

                self.pos[1] = entity_rect.y

        self.velocity[1] = min(MAX_GRAVITY_FORCE, self.velocity[1] + GRAVITY_FORCE)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()
        self.particle_animation.update()

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def set_particles(self, part_type):
        if part_type != self.part_type:
            self.part_type = part_type
            self.particle_animation = self.game.assets[
                "particles/" + self.part_type
            ].copy()

    def render(self, surf, scroll=(0, 0)):
        surf.blit(
            p.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - scroll[0] + self.anim_offset[0],
                self.pos[1] - scroll[1] + self.anim_offset[1],
            ),
        )
        
        if DRAW_HITBOX:
            p.draw.rect(surf, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1], *self.size), 1)


class Hero(Entity):
    def __init__(self, game, pos, size):
        self.pos = list(pos)
        super().__init__(game, "hero", pos, size)

        self.anim_offset = (-26, -3)
        self.air_time = 0

        self.set_action("idle")
        self.jumps = MAX_JUMP_COUNT

        self.active = 0
        self.last_pos_on_ground = self.pos.copy()

        self.particles_offset = [0, -8]
        self.have_sword = 1
        self.is_on_floor = False
        self.alive = True
        
        self.iskicked = False
        self.frame_kicked = 0
        self.attacking = False
        self.attack_type = 1
        self.cooldown = 40
        self.cooldown_combo = 50
        self.frame_cooldown = 0
        self.attack_counter = 0
        self.health = 100
        self.attack_rect = p.Rect((self.rect().centerx, self.rect().y) , (HERO_ATTACK_RANGE + self.size[0] // 2, self.size[1]))
        # self.have_sword = False

    def set_action(self, action):
        if action != self.action:
            self.action = action
            if not self.have_sword:
                self.animation = self.game.assets[self.type + "/" + self.action].copy()
            else:
                self.animation = self.game.assets[
                    self.type + "/" + self.action + "_sword"
                ].copy()
        
                
    def attack(self):
        if self.frame_cooldown >= self.cooldown:
            if self.frame_cooldown <=self.cooldown_combo:
                self.attack_counter += 1
            else:
                self.attack_counter = 0
                
            
            if self.attack_counter > 0:
                if self.attack_counter % 4 == 0:
                    self.attack_type = 3
                elif self.attack_counter % 3 == 0:
                    self.attack_type = 2
            else: 
                self.attack_type = 1
            
            if self.have_sword:
                self.game.sfx['attack'].play()
                if self.is_on_floor:
                    self.set_action(f'attack{self.attack_type}')
                else:
                    if self.attack_counter % 2 == 1:
                        self.set_action('air_attack_2')
                    else:
                        self.set_action('air_attack_1')
            self.frame_cooldown = 0
            

            
    def update(self, tilemap, movement=(0, 0)):
        self.attacking = 'attack'in self.action and self.alive and self.have_sword
        
        if not self.alive:
            self.jumps = 0
            self.frame_cooldown = 0
            
        self.frame_cooldown += 1
        
        if self.air_time >= 200:
            self.alive = False
    
        self.is_on_floor = abs(self.velocity[1]) <= 0.4 and self.air_time <= 6
        
        if self.is_on_floor:
            if not self.flip:
                self.attack_rect = p.Rect((self.rect().centerx, self.rect().y) , (HERO_ATTACK_RANGE + self.size[0] // 2, self.size[1]))
            else:
                self.attack_rect = p.Rect((self.rect().x - HERO_ATTACK_RANGE, self.rect().y) , (HERO_ATTACK_RANGE + self.size[0] // 2, self.size[1]))
        else:
            self.attack_rect = p.Rect((self.rect().left - 10, self.rect().bottom) , (20 + self.size[0], self.size[1] // 2))
            
            
        if self.iskicked:
            if self.frame_kicked < 35:
                movement = (movement[0] + 2 if self.flip else -2, movement[1] - 2)
                self.frame_kicked += 1
            else:
                self.iskicked = False
                self.frame_kicked = 0
                
        super().update(tilemap, movement=movement if self.alive else [0, 0], gv = 0 if self.iskicked else 1)
                
        if self.health <= 0:
            self.game.screenshake = max(16, self.game.screenshake)
            
            self.alive = False
            
            self.size = [20, 12]
            self.anim_offset = [-20, -18]
            self.particles_offset = [10, 10]
            
            if not self.iskicked and self.is_on_floor:
                if self.action != 'dead_ground':
                    self.set_action('dead_ground')

                    self.set_particles('fall')
                return
            
            if self.action != 'dead_hit' and self.action != 'dead_ground':
                self.set_action('dead_hit')
            
            self.set_particles('idle')
            return
            # else:
            #     return
        
        
        if self.action == 'hit':
            self.game.screenshake = max(8, self.game.screenshake)
            if self.animation.end:
                self.set_action('idle')
            else:
                self.game.sfx['hit'].play()
                return
        
        if self.action == 'air_attack_1' or self.action == 'air_attack_2':
            if self.flip:
                self.particles_offset = [20, -25]
            else:
                self.particles_offset = [-10, -25]
            if self.action == 'air_attack_1':
                self.set_particles('air_attack_1')
            if self.action == 'air_attack_2':
                self.set_particles('air_attack_2')
            if self.animation.end:
                self.set_action('fall')
            else:
                return
            
        if self.action == 'attack1' or self.action == 'attack2' or self.action == 'attack3' :
            
            if self.flip:
                self.particles_offset = [50, -5]
            else:
                self.particles_offset = [-25, -5]
                
            if self.action == 'attack1':
                self.particles_offset[1] = -12
            self.set_particles(f'attack{self.attack_type}')
            if self.animation.end:
                self.set_action('idle')
            else:
                return
            
        self.air_time += 1
        fall_part = False
        if self.collisions["down"]:
            self.last_pos_on_ground = self.pos.copy()
            if self.air_time > 10:
                fall_part = True

            self.air_time = 0
            self.jumps = MAX_JUMP_COUNT

        if fall_part:
            self.set_particles("fall")
            self.set_action("ground")

        if self.velocity[1] < 0:
            self.set_action("jump")
            
        elif self.velocity[1] > 0.4:
            self.set_action("fall")
            if self.part_type == 'jump' and not self.particle_animation.end:
                pass
            
            else:
                self.set_particles("idle")

        elif movement[0] != 0 and self.jumps == 1:
            self.set_action("run")
            self.set_particles("run")

        else:
            if self.action == "ground" and not self.animation.end:
                pass
            else:
                self.set_action("idle")

            if self.part_type == "fall":
                if self.particle_animation.end:
                    self.set_particles("idle")
            else:
                self.set_particles("idle")

        if self.part_type == "run":
            if self.flip:
                self.particles_offset = [12, -8]
            else:
                self.particles_offset = [26, -8]

        else:
            self.particles_offset = [20, -7]

        if self.part_type == "jump":
            self.particles_offset[1] += self.velocity[1]

    def jump(self):
        if self.jumps:
            self.game.sfx['jump'].play()
            self.velocity[1] = JUMP_FORCE
            self.jumps -= 1
            self.air_time = 5
            if self.is_on_floor:
                self.set_particles("jump")


    def render(self, surf, scroll=(0, 0)):
        surf.blit(
            p.transform.flip(self.animation.img(), self.flip , False),
            (
                self.pos[0] - scroll[0] + self.anim_offset[0],
                self.pos[1] - scroll[1] + self.anim_offset[1],
            ),
        )
        
        if self.part_type != "idle":
            if 'attack' in self.part_type and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
            if self.part_type == "jump" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.last_pos_on_ground[0]
                        - scroll[0]
                        - self.particles_offset[0],
                        self.last_pos_on_ground[1]
                        - scroll[1]
                        - self.particles_offset[1],
                    ),
                )
            if self.part_type == "fall" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
            if self.part_type == "run" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
                
        if DRAW_HITBOX:
            p.draw.rect(surf, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1], *self.size), 1)
            p.draw.rect(surf, (0, 0, 255), (self.attack_rect.x - scroll[0], self.attack_rect.y - scroll[1], self.attack_rect.width, self.attack_rect.height), 1)


class Enemy(Entity):
    def __init__(self, game, size, pos, type):
        super().__init__(game, 'enemy/'+type, pos, size)
        self.walking = 0
        self.air_time = 0
        self.jumps = 1
        self.iskicked = 0
        self.contact_time = 0
        self.frame_kicked = 0
        self.health = ENEMY_HARACTER[type]['health']
        self.flip_cooldown = 0
        self.alive = True
        self.anim_offset = [5, 6]
        if type == 'Crabby':
            self.anim_offset = [25, 6]
        self.take_damage_cooldown = 0
        
    def update(self, tilemap, hero, movement=(0, 0)):
        type = self.type.split("/")[1]
        hero_detected = False
        can_attack = False
        
        self.flip_cooldown += 1
        self.take_damage_cooldown += 1
        
        
        if not self.flip:
            self.vision_rect = p.Rect((self.rect().centerx, self.rect().centery) , (ENEMY_HARACTER[type]['vision_area'], 1))
            self.attack_rect = p.Rect((self.rect().centerx, self.rect().y) , (ENEMY_HARACTER[type]['attack_range'] + self.size[0] // 2, self.size[1]))
        else:
            self.vision_rect = p.Rect((self.rect().centerx-ENEMY_HARACTER[type]['vision_area'], self.rect().centery) , (ENEMY_HARACTER[type]['vision_area'], 1))
            self.attack_rect = p.Rect((self.rect().x - ENEMY_HARACTER[type]['attack_range'], self.rect().y) , (ENEMY_HARACTER[type]['attack_range'] + self.size[0] // 2, self.size[1]))
            
        if type == 'Crabby':
            self.vspom_rect = p.Rect((self.rect().centerx-ENEMY_HARACTER[type]['vision_area'], self.rect().centery) , (ENEMY_HARACTER[type]['vision_area'], 1))
            self.vision_rect = p.Rect((self.rect().centerx-ENEMY_HARACTER[type]['vision_area'], self.rect().centery) , (ENEMY_HARACTER[type]['vision_area'] * 2, 1))
            self.attack_rect = p.Rect((self.rect().centerx - ENEMY_HARACTER[type]['attack_range'], self.rect().y) , (ENEMY_HARACTER[type]['attack_range'] * 2, self.size[1]))
                

        if self.alive:
            if self.vision_rect.colliderect(hero.rect()) and hero.alive:
                hero_detected = True
                
                
            if self.walking and not hero_detected:
                if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 40)):
                    if self.collisions['right'] or self.collisions['left']:
                        self.flip = not self.flip
                    movement = (movement[0] - ENEMY_HARACTER[type]['speed'] if self.flip else + ENEMY_HARACTER[type]['speed'], movement[1])
                else:
                    if self.flip_cooldown >= 20 and not self.iskicked:
                        self.flip = not self.flip
                        self.flip_cooldown = 0
                    
                self.walking = max(0, self.walking - 1)
            elif random.random() < 0.01:
                self.walking = random.randint(80, 120)
            elif not hero_detected:
                self.set_action("idle")
            
            if hero_detected:
                if type == 'Crabby':
                    if self.vspom_rect.colliderect(hero.rect()):
                        self.flip = 1
                    else:
                        self.flip = 0
                movement = ((movement[0] - ENEMY_HARACTER[type]['catch_speed'] if self.flip else + ENEMY_HARACTER[type]['catch_speed'], movement[1]))  
                if type == 'Pink Star':
                    if self.action != 'attack':
                        self.set_action("attack")
                if self.attack_rect.colliderect(hero.rect()):
                    can_attack = True
                    if self.contact_time % ENEMY_HARACTER[type]['attack_cooldown'] == 0 and self.alive and not self.iskicked and hero.alive:

                        hero.set_action('hit')
                        
                        hero.flip = not self.flip
                        hero.iskicked = True
                        
                        hero.health -= ENEMY_HARACTER[type]['damage']
                    self.contact_time += 1
                
                else:
                    self.contact_time = 1
            
            if not hero_detected and self.rect().colliderect(hero.rect()) and self.flip_cooldown > 20:
                self.flip = not self.flip
                self.flip_cooldown = 0
            
        if not self.alive:
            movement = [0, 0]      
            
        
        if hero.attack_rect.colliderect(self.rect()):
            if hero.attacking and self.alive:
                self.set_action('hit')
                self.flip = not hero.flip
                self.iskicked = True
                
                if self.take_damage_cooldown > 20:
                    self.health -= HERO_ATTACK_DAMAGE[hero.attack_type - 1]
                    self.take_damage_cooldown = 0   
                 
                
        if self.iskicked:
            if self.frame_kicked < 35:
                movement = (movement[0] + 2 if self.flip else -2, movement[1] - 1.6)
                    
                self.frame_kicked += 1
            else:
                self.iskicked = False
                self.frame_kicked = 0
                
        super().update(tilemap, movement, gv = False)   
        
        if self.action == 'hit':
            if self.animation.end:
                self.set_action('idle')
            else:
                return               

        self.is_on_floor = abs(self.velocity[1]) <= 0.4
        
        if self.health <= 0:
            self.alive = False
            
            self.size = [16, 12]
            self.anim_offset = [5, 14]
            self.particles_offset = [10, 10]
            
            if not self.iskicked and self.is_on_floor:
                if self.action != 'dead_ground':
                    self.game.screenshake = max(4, self.game.screenshake)
                    self.set_action('dead_ground')
                    self.set_particles('fall')
                return
            
            if self.action != 'dead_hit' and self.action != 'dead_ground':
                self.set_action('dead_hit')
            
            self.set_particles('idle')
            return
        
        
        if type == 'Fierce Tooth' or type == 'Crabby':
            if can_attack:
                if not self.animation.end:
                    self.set_action("attack")
                    
                    if type == 'Fierce Tooth':
                        self.set_particles("fiercetooth_attack")
                    
                    if self.flip:
                        self.particles_offset = [20, 5]
                    else:
                        self.particles_offset = [-20, 5]
                    return
        if type == 'Pink Star':
            if self.action == 'attack':
                if not self.animation.end:
                    return
                else:
                    self.set_action('idle')
        
                
                
            
        self.air_time += 1
        fall_part = False
            
        if self.collisions["down"]:
            self.last_pos_on_ground = self.pos.copy()
            if self.air_time > 10:
                fall_part = True

            self.air_time = 0
            self.jumps = MAX_JUMP_COUNT

        if fall_part:
            self.set_particles("fall")
            self.set_action("ground")

        if self.velocity[1] < 0:
            self.set_action("jump")
            
        elif self.velocity[1] > 0.4:
            self.set_action("fall")
            if self.part_type == 'jump' and not self.particle_animation.end:
                pass
            
            else:
                self.set_particles("idle")

        elif movement[0] != 0:
            self.set_action("run")
            self.set_particles("run")

        else:
            if self.action == "ground" and not self.animation.end:
                pass
            else:
                self.set_action("idle")

            if self.part_type == "fall":
                if self.particle_animation.end:
                    self.set_particles("idle")
            else:
                self.set_particles("idle")

        if self.part_type == "run":
            if self.flip:
                self.particles_offset = [5, -1]
            else:
                self.particles_offset = [26, -1]

        else:
            self.particles_offset = [20, -7]

        if self.part_type == "jump":
            self.particles_offset[1] += self.velocity[1]
            
        
    def render(self, surf, scroll=(0, 0)):
        
        surf.blit(
            p.transform.flip(self.animation.img(), not self.flip, False),
            (
                self.pos[0] - scroll[0] - self.anim_offset[0],
                self.pos[1] - scroll[1] - self.anim_offset[1],
            ),
        )
        
        if self.part_type != "idle":
            if self.part_type == "fiercetooth_attack" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), not self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
            if self.part_type == "jump" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.last_pos_on_ground[0]
                        - scroll[0]
                        - self.particles_offset[0],
                        self.last_pos_on_ground[1]
                        - scroll[1]
                        - self.particles_offset[1],
                    ),
                )
            if self.part_type == "fall" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
            if self.part_type == "run" and not self.particle_animation.end:
                surf.blit(
                    p.transform.flip(self.particle_animation.img(), self.flip, False),
                    (
                        self.pos[0] - scroll[0] - self.particles_offset[0],
                        self.pos[1] - scroll[1] - self.particles_offset[1],
                    ),
                )
                
        if DRAW_HITBOX:
            p.draw.rect(surf, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1], *self.size), 1)
            p.draw.rect(surf, (255, 0, 0), (self.vision_rect.x - scroll[0], self.vision_rect.y - scroll[1], self.vision_rect.width, 1), 1)
            p.draw.rect(surf, (0, 0, 255), (self.attack_rect.x - scroll[0], self.attack_rect.y - scroll[1], self.attack_rect.width, self.attack_rect.height), 1)
            if 'Crabby' in self.type:
                p.draw.rect(surf, (0, 255, 0), (self.vspom_rect.x - scroll[0], self.vspom_rect.y - scroll[1], self.vspom_rect.width, self.vspom_rect.height), 1)
