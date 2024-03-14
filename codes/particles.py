class Partiсle():
    def __init__(self, game, type, frame = 0) -> None:
        self.game = game
        self.type = type
        self.animation = self.game.assets['hero/particles/'+ self.type].copy()
        self.animation.frame = frame
        
    def update(self):
        self.animation.update()
        
    def render(self, surf, pos, scroll = (0, 0)):
        surf.blit(self.animation.img(), (pos[0] - scroll[0] - self.animation.img().get_width() // 2, pos[1] - scroll[1] - self.animation.img().get_height() // 2)) 
           