from SpriteGroup import SpriteGroup


class GameController:

    def __init__(self, textures=None, levels=None, screen=None):
        self.frames = 0
        self.turret_gen = None
        self.textures = textures
        self.levels = levels
        self.shells = SpriteGroup()
        self.interface = SpriteGroup()
        self.screen = screen

    def update(self):
        self.shells.get_my_event("check_death")
        self.turret_gen.update()
        self.frames += 1

    def set_turret_gen(self, turret_gen):
        self.turret_gen = turret_gen

    def initialization(self, level=1):
        self.turret_gen.generate_turrets(level)