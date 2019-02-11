from SpriteGroup import SpriteGroup
from Turret import Turret


class TurretGenerator:
    """Класс-контроллер турелей"""

    def __init__(self, game_controller):
        """Инициализация контроллера"""
        self.turrets = SpriteGroup()
        self.game_controller = game_controller
        self.active_type = ""

    def generate_turrets(self, level):
        """Инициализация контроллера перед уровнем"""
        self.__init__(game_controller=self.game_controller)
        self.turrets = SpriteGroup()
        levels = self.game_controller.levels
        textures = self.game_controller.textures
        turret_list = levels["turrets"][str(level)]
        pos = levels["turret_positions"]
        self.active_type = turret_list[-1]
        for i in range(len(turret_list)):
            turret = turret_list[i]
            self.turrets.add(Turret(self.turrets, pos[str(i + 1)], (72, 72),
                                    image=textures[turret],
                                    game_controller=self.game_controller,
                                    turret_type=turret))

    def update(self):
        """Обновление состояния турелей"""
        for turret in self.turrets:
            turret.update()

    def change_turret(self, turret):
        """Изменение активной турели"""
        self.active_type = turret.turret_type

    def clear(self):
        """Очистка списка турелей"""
        self.turrets = SpriteGroup()
