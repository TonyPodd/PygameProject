from config import *

from codes.entety import Entity, Hero, Enemy
from codes.vspom import load_image
from codes.vspom import load_images
from codes.map import TileMap
from codes.clouds import Clouds
from codes.vspom import Animation
import pygame as p
import os
import random
import sys


class Game:
    def __init__(self) -> None:
        p.init()
        p.display.set_caption("---")
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.clock = p.time.Clock()
        self.running = True
        self.movement = [0, 0]
        self.display_2 = p.Surface((WIDTH // 2, HEIGHT // 2))
        self.display = p.Surface((WIDTH // 2, HEIGHT // 2), p.SRCALPHA)

        # --------------------------------------------------------

        self.assets = {
            "blocks": load_images("Palm Tree Island/Sprites/Terrain"),
            "hero": load_image(
                "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/01-Idle/Idle 01.png"
            ),
            "enemy/Fierce Tooth": load_image(
                "The Crusty Crew/Sprites/Fierce Tooth/01-Idle/idle 01.png"
            ),
            "enemy/Pink Star": load_image(
                "The Crusty Crew/Sprites/Pink Star/01-Idle/idle 01.png"
            ),
            "enemy/Crabby": load_image(
                "The Crusty Crew/Sprites/Crabby/01-Idle/idle 01.png"
            ),
            "bg": load_image("Palm Tree Island/Sprites/Background/BG Image.png"),
            "clouds": load_images("Palm Tree Island/Sprites/Background/clouds"),
            "big_clouds": load_image(
                "Palm Tree Island/Sprites/Background/Big clouds.png"
            ),
            "hero/idle": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/01-Idle"
                ),
                duration=10,
            ),
            "hero/run": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/02-Run"
                ),
                duration=10,
            ),
            "hero/jump": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/03-Jump"
                ),
                duration=10,
            ),
            "hero/fall": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/04-Fall"
                ),
                duration=10,
            ),
            "hero/ground": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/05-Ground"
                ),
                duration=10,
                loop=False,
            ),
            "hero/hit": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/06-Hit"
                ),
                duration=10,
                loop=False,
            ),
            "hero/dead_hit": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/07-Dead Hit"
                ),
                duration=10,
                loop=False,
            ),
            "hero/dead_ground": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/08-Dead Ground"
                ),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/idle": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/01-Idle"),
                duration=10,
            ),
            "enemy/Fierce Tooth/run": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/02-Run"),
                duration=10,
            ),
            "enemy/Fierce Tooth/jump": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/03-Jump"),
                duration=10,
            ),
            "enemy/Fierce Tooth/fall": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/04-Fall"),
                duration=10,
            ),
            "enemy/Fierce Tooth/ground": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/05-Ground"),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/anticipation": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/06-Anticipation"),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/attack": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/07-Attack"),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/hit": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/08-Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/dead_hit": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/09-Dead Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Fierce Tooth/dead_ground": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/10-Dead Ground"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/idle": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/01-Idle"),
                duration=10,
            ),
            "enemy/Pink Star/run": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/02-Run"),
                duration=10,
            ),
            "enemy/Pink Star/jump": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/03-Jump"),
                duration=10,
            ),
            "enemy/Pink Star/fall": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/04-Fall"),
                duration=10,
            ),
            "enemy/Pink Star/ground": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/05-Ground"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/anticipation": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/06-Anticipation"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/attack": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/07-Attack"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/hit": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/08-Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/dead_hit": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/09-Dead Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Pink Star/dead_ground": Animation(
                load_images("The Crusty Crew/Sprites/Pink Star/10-Dead Ground"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/idle": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/01-Idle"),
                duration=10,
            ),
            "enemy/Crabby/run": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/02-Run"),
                duration=10,
            ),
            "enemy/Crabby/jump": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/03-Jump"),
                duration=10,
            ),
            "enemy/Crabby/fall": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/04-Fall"),
                duration=10,
            ),
            "enemy/Crabby/ground": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/05-Ground"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/anticipation": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/06-Anticipation"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/attack": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/07-Attack"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/hit": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/08-Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/dead_hit": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/09-Dead Hit"),
                duration=10,
                loop=False,
            ),
            "enemy/Crabby/dead_ground": Animation(
                load_images("The Crusty Crew/Sprites/Crabby/10-Dead Ground"),
                duration=10,
                loop=False,
            ),
            "hero/idle_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/09-Idle"
                ),
                duration=10,
            ),
            "hero/run_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/10-Run"
                ),
                duration=10,
            ),
            "hero/jump_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/11-Jump"
                ),
                duration=10,
            ),
            "hero/fall_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/12-Fall"
                ),
                duration=10,
            ),
            "hero/ground_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/13-Ground"
                ),
                duration=10,
                loop=False,
            ),
            "hero/hit_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/14-Hit"
                ),
                duration=10,
                loop=False,
            ),
            "hero/dead_hit_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/07-Dead Hit"
                ),
                duration=10,
                loop=False,
            ),
            "hero/dead_ground_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/08-Dead Ground"
                ),
                duration=10,
                loop=False,
            ),
            "hero/attack1_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/15-Attack 1"
                ),
                duration=7,
                loop=False,
            ),
            "hero/attack2_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/16-Attack 2"
                ),
                duration=7,
                loop=False,
            ),
            "hero/attack3_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/17-Attack 3"
                ),
                duration=7,
                loop=False,
            ),
            "hero/air_attack_1_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/18-Air Attack 1"
                ),
                duration=7,
                loop=False,
            ),
            "hero/air_attack_2_sword": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose with Sword/19-Air Attack 2"
                ),
                duration=7,
                loop=False,
            ),
            "particles/jump": Animation(
                load_images("Captain Clown Nose/Sprites/Dust Particles/Jump"),
                duration=6,
                loop=False,
            ),
            "particles/run": Animation(
                load_images("Captain Clown Nose/Sprites/Dust Particles/Run"),
                duration=10,
            ),
            "particles/fall": Animation(
                load_images("Captain Clown Nose/Sprites/Dust Particles/Fall"),
                duration=6,
                loop=False,
            ),
            "particles/idle": Animation(
                load_images("Captain Clown Nose/Sprites/Dust Particles/Idle"),
                duration=10,
            ),
            "particles/fiercetooth_attack": Animation(
                load_images("The Crusty Crew/Sprites/Fierce Tooth/11-Attack Effect"),
                duration=10,
            ),
            "particles/attack1": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Sword Effects/24-Attack 1"
                ),
                duration=7,
            ),
            "particles/attack2": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Sword Effects/25-Attack 2"
                ),
                duration=7,
            ),
            "particles/attack3": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Sword Effects/26-Attack 3"
                ),
                duration=7,
            ),
            "particles/air_attack_1": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Sword Effects/27-Air Attack 1"
                ),
                duration=7,
            ),
            "particles/air_attack_2": Animation(
                load_images(
                    "Captain Clown Nose/Sprites/Captain Clown Nose/Sword Effects/28-Air Attack 2"
                ),
                duration=7,
            ),
            "palm_back_0": Animation(
                load_images("Palm Tree Island/Sprites/Back Palm Trees/left"),
                duration=10,
            ),
            "palm_back_1": Animation(
                load_images("Palm Tree Island/Sprites/Back Palm Trees/regular"),
                duration=10,
            ),
            "palm_back_2": Animation(
                load_images("Palm Tree Island/Sprites/Back Palm Trees/right"),
                duration=10,
            ),
            "palm_front": Animation(
                load_images("Palm Tree Island/Sprites/Front Palm Trees/palm top anim"),
                duration=20,
            ),
            "ui/big_life_bar": load_images(
                "Wood and Paper UI/Sprites/Life Bars/Big Bars"
            ),
            "color_bar": load_image("Wood and Paper UI/Sprites/Life Bars/Colors/1.png"),
            "decor": load_images("Palm Tree Island/Sprites/Front Palm Trees/decor"),
            "finish": Animation(
                load_images("Pirate Treasure/Sprites/Big Map/Idle"),
                duration=10,
            ),
        }

        self.sfx = {
            "jump": p.mixer.Sound("data/sound/jump.mp3"),
            "attack": p.mixer.Sound("data/sound/attack.mp3"),
            "hit": p.mixer.Sound("data/sound/hit.mp3"),
            "music": p.mixer.Sound("data/sound/music.mp3"),
            "next": p.mixer.Sound("data/sound/next.mp3"),
        }

        self.sfx["jump"].set_volume(0.2)
        self.sfx["attack"].set_volume(0.2)
        self.sfx["hit"].set_volume(0.2)

        # ----------------------Подгрузка уровня-------------------------------

        self.current_level = 0
        self.load_level(self.current_level)

        # -------------------------Инициализация-------------------------------

        self.screenshake = 0

    def check_level_completion(self):
        for tile in self.tilemap.around(self.hero.pos):
            if tile["type"] == "blocks" and tile["variant"] == 47:
                return True

    def render_text(
        self, text, font_size=20, letter_spacing=20, line_spacing=0, big=True
    ):
        surface_list = []

        current_x, current_y = 0, 0

        for char in text:
            if char.isalpha() and char.islower():
                char = char.upper()

            if char.isalpha() or char.isdigit():
                image_path = os.path.join(
                    f"data\Treasure Hunters\Wood and Paper UI\Sprites\{'Big' if big else 'Small'} Text",
                    f"{ord(char)- 64}.png",
                )
                char_image = p.image.load(image_path).convert_alpha()

                surface_list.append((char_image, (current_x, current_y)))
                current_x += char_image.get_width() + letter_spacing
            elif char == " ":
                current_x += font_size // 2
            elif char == "\n":
                current_x = 0
                current_y += font_size + line_spacing

        max_width = max(surface.get_width() + x for surface, (x, y) in surface_list)
        total_height = current_y + font_size

        final_surface = p.Surface((max_width, total_height), p.SRCALPHA)

        for surface, (x, y) in surface_list:
            final_surface.blit(surface, (x, y))

        return final_surface

    def load_level(self, level_num):
        self.tilemap = TileMap(self, 32)
        self.tilemap.load_level(f"data/level{level_num}_main_physicks.csv")
        self.tilemap.load_palms_top(f"data/level{level_num}_Palms.csv")
        self.tilemap.load_decor_front(f"data/level{level_num}_decor_front.csv")
        self.tilemap.load_enemyes(f"data/level{level_num}_enemyes.csv")

        self.enemies = []
        self.clouds = Clouds(self.assets["clouds"], count=31)
        self.hero = Hero(self, pos=(0, 0), size=(12, 28))
        self.camera_scroll = [0, 0]
        self.bg_img = p.transform.scale(self.assets["bg"], (WIDTH, HEIGHT))

        self.completed = 0

        for spawner in self.tilemap.enemy_spawner.values():
            # print
            pos = list(spawner["pos"]).copy()
            pos = [pos[0] * 32, pos[1] * 32]
            if spawner["variant"] == 0:
                # print(spawner["pos"])
                self.hero.pos = pos
            else:
                type = ENEMY_TYPES[spawner["variant"] - 1]
                self.enemies.append(Enemy(self, size=(22, 22), pos=pos, type=type))

        self.transition = -30

    def run(self):
        p.mixer.music.load("data/sound/music.mp3")
        p.mixer.music.set_volume(0.2)
        p.mixer.music.play(-1)

        while self.running:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.bg_img, (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                if event.type == p.KEYDOWN:
                    if event.key == p.K_d or event.key == p.K_RIGHT:
                        self.movement[1] = True
                    if event.key == p.K_a or event.key == p.K_LEFT:
                        self.movement[0] = True
                    if event.key == p.K_w:
                        self.hero.jump()
                    if event.key == p.K_SPACE:
                        self.hero.attack()
                elif event.type == p.KEYUP:
                    if event.key == p.K_d or event.key == p.K_RIGHT:
                        self.movement[1] = False
                    if event.key == p.K_a or event.key == p.K_LEFT:
                        self.movement[0] = False

            # --------------------------------------------------

            if self.transition < 0:
                self.transition += 1

            if self.check_level_completion():
                self.completed = True
                self.sfx["next"].play()

            if self.completed:
                self.transition += 1
                if self.transition >= 30:
                    self.current_level += 1
                    self.load_level(self.current_level)

            # --------------------------------------------------

            # --------------------------------------------------

            # self.ui_layer.fill((0, 0, 0, 0))

            # --------------------------------------------------

            self.camera_scroll[0] += (
                self.hero.rect().centerx
                - self.display.get_width() / 2
                - self.camera_scroll[0]
            ) * SMUFF_X
            self.camera_scroll[1] += (
                int(
                    self.hero.rect().centery
                    - self.display.get_height() / 2
                    - self.camera_scroll[1]
                )
            ) * SMUFF_Y

            self.render_scroll = (
                int(self.camera_scroll[0]),
                int(self.camera_scroll[1]),
            )

            # --------------------------------------------------

            self.clouds.update()
            self.clouds.render(self.display_2, self.render_scroll)

            # --------------------------------------------------

            self.tilemap.render(self.display, scroll=self.render_scroll)

            # --------------------------------------------------

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, self.hero, (0, 0))
                enemy.render(self.display, scroll=self.render_scroll)

            # --------------------------------------------------

            if self.current_level == 0:
                self.display_2.blit(
                    self.render_text(" move", letter_spacing=1, big=False),
                    (698 - self.render_scroll[0], 410 - self.render_scroll[1]),
                )
                self.display_2.blit(
                    self.render_text("a  d", letter_spacing=0),
                    (700 - self.render_scroll[0], 420 - self.render_scroll[1]),
                )
                self.display_2.blit(
                    self.render_text("  jump", letter_spacing=1, big=False),
                    (894 - self.render_scroll[0], 410 - self.render_scroll[1]),
                )
                self.display_2.blit(
                    self.render_text("  w", letter_spacing=0),
                    (900 - self.render_scroll[0], 420 - self.render_scroll[1]),
                )
                self.display_2.blit(
                    self.render_text(" attack", letter_spacing=1, big=False),
                    (1194 - self.render_scroll[0], 410 - self.render_scroll[1]),
                )
                self.display_2.blit(
                    self.render_text("space", letter_spacing=0),
                    (1198 - self.render_scroll[0], 420 - self.render_scroll[1]),
                )

                self.display_2.blit(
                    self.render_text("next level", letter_spacing=0),
                    (1411 - self.render_scroll[0], 400 - self.render_scroll[1]),
                )

            # --------------------------------------------------

            # --------------------------------------------------

            self.hero.update(
                self.tilemap, ((self.movement[1] - self.movement[0]) * HERO_SPEED, 0)
            )

            self.hero.render(self.display, scroll=self.render_scroll)

            if not self.hero.alive:
                self.transition += 1
                if self.transition >= 30:
                    self.load_level(self.current_level)

            # --------------------------------------------------

            for bar_part in range(3):
                self.display.blit(
                    self.assets["ui/big_life_bar"][bar_part], (10 + 32 * bar_part, 5)
                )
                self.display.blit(
                    p.transform.scale(
                        self.assets["color_bar"],
                        (max(0, 79 * self.hero.health // 100), 2),
                    ),
                    (25, 19),
                )

            # --------------------------------------------------

            if self.transition:
                transition_surf = p.Surface(self.display.get_size())
                p.draw.circle(
                    transition_surf,
                    (255, 255, 255),
                    (self.display.get_width() // 2, self.display.get_height() // 2),
                    (30 - abs(self.transition)) * 8,
                )
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            # --------------------------------------------------

            mask = p.mask.from_surface(self.display)
            sil = mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            # for off in [(-1 , 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(sil, (1, 1))

            # --------------------------------------------------

            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2,
            )

            self.display_2.blit(self.display, (0, 0))
            self.screen.blit(
                p.transform.scale(self.display_2, self.screen.get_size()),
                screenshake_offset,
            )
            # self.screen.blit(
            #     p.transform.scale(self.display, self.screen.get_size()),
            #     screenshake_offset,
            # )

            # print(POSITION)
            p.display.update()
            self.clock.tick(60)

            # --------------------------------------------------


gm = Game()
gm.run()
p.quit()
