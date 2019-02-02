from SpriteGroup import SpriteGroup
from Enemy import Enemy


class EnemyGenerator:

    def __init__(self, game_controller):
        self.enemies = SpriteGroup()
        self.game_controller = game_controller

    def generate_enemies(self, level):
        levels = self.game_controller.levels
        textures = self.game_controller.textures
        width = textures["soldier"][0].get_rect().width
        height = textures["soldier"][0].get_rect().height
        size = [width * levels["enemy_scale"], height * levels["enemy_scale"]]
        Enemy(self.enemies, [400, 300], size, enemy_type="soldier",
              game_controller=self.game_controller)

    def update(self):
        for enemy in self.enemies:
            enemy.update()
