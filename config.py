WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1000, 600
GRAVITY_FORCE = 0.1
MAX_GRAVITY_FORCE = 5
OFFSET =[(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TYPES = {'blocks'}
HERO_SPEED = 2
JUMP_FORCE = -4
SMUFF_X = 0.1
SMUFF_Y = 0.1
BORDER_SKY = 100
MAX_JUMP_COUNT = 1
ENEMY_TYPES = ['Fierce Tooth', 'Pink Star', 'Crabby']
ENEMY_HARACTER = {'Fierce Tooth' : {'health' : 40, 'speed' : 0.5, 'catch_speed' : 1, 'damage' : 25, 'attack_cooldown' : 15, 'attack_range' : 20, 'vision_area' : 100}, 'Pink Star' : {'health' : 100, 'speed' : 0.5, 'catch_speed' : 3, 'damage' : 40, 'attack_cooldown' : 15, 'attack_range' : 20, 'vision_area' : 100}, 'Crabby' : {'health' : 40, 'speed' : 0.5, 'catch_speed' : 1, 'damage' : 35, 'attack_cooldown' : 15, 'attack_range' : 30, 'vision_area' : 100}}
POSITION = []
HERO_ATTACK_RANGE = 29
HERO_ATTACK_DAMAGE = [10, 20, 40]
DRAW_HITBOX = 0


# hero_rect_transf = [0, 0, 0, 0]