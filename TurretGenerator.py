from SpriteGroup import SpriteGroup
from Turret import Turret


class TurretGenerator:

    def __init__(self, game_controller):
        self.turrets = SpriteGroup()
        self.game_controller = game_controller

    def generate_turrets(self, level):
        levels = self.game_controller.levels
        textures = self.game_controller.textures
        turret_list = levels["turrets"][str(level)]
        pos = levels["turret_positions"]
        for i in range(len(turret_list)):
            turret = turret_list[i]
            self.turrets.add(Turret(self.turrets, pos[str(i + 1)], (72, 72),
                                    image=textures[turret],
                                    game_controller=self.game_controller,
                                    turret_type=turret,
                                    shot_period=levels["shot_periods"][turret],
                                    recharging_speed=levels["repairing_speed"][
                                        turret]))

    def update(self):
        for turret in self.turrets:
            turret.update()