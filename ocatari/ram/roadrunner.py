from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS =  {'Player': 1, 'Enemy': 1}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Enemy': 1, 'PlayerScore': 1, 'EnemyScore': 1, 'Logo': 1, 'Clock': 4}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 14, 46
        self.rgb = 214, 214, 214
        self.hud = False
        self._above_10 = False


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 14, 46
        self.rgb = 0, 0, 0
        self.hud = False
        self._above_10 = False


class Logo(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 62, 189
        self.wh = 32, 7
        self.rgb = 20, 60, 0
        self.hud = True


class Clock(GameObject):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 20, 60, 0
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 47, 5
        self.wh = 6, 7
        self.hud = True
        self._ten = False

    def tenify(self):
        if not self._ten:
            self._xy = 39, 5
            self.wh = 14, 7
            self._ten = True

    def detenify(self):
        if self._ten:
            self._xy = 47, 5
            self.wh = 6, 7
            self._ten = False

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class EnemyScore(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 111, 5
        self.rgb = 0, 0, 0
        self.wh = 6, 7
        self.hud = True
        self._ten = False

    def tenify(self):
        if not self._ten:
            self._xy = 103, 5
            self.wh = 14, 7
            self._ten = True

    def detenify(self):
        if self._ten:
            self._xy = 111, 5
            self.wh = 6, 7
            self._ten = False


# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


def _init_objects_roadrunner_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Enemy()]
    if hud:
        global plscore
        plscore = PlayerScore()
        global enscore
        enscore = EnemyScore()
        objects.extend([plscore, enscore, Logo(),
                        Clock(63, 17, 6, 7), Clock(73, 18, 2, 5),
                        Clock(79, 17, 6, 7), Clock(87, 17, 6, 7)])
    return objects


def _detect_objects_roadrunner_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy = objects[:2]
    player.xy = ram_state[32]+5, ram_state[34]+38
    enemy.xy = ram_state[33]+4, ram_state[35]+38
    if hud:
        # scores
        global plscore
        global enscore
        if ram_state[19] > 10:  # enemy score
            enscore.tenify()
        else:
            enscore.detenify()
        if ram_state[18] > 10:  # player score
            plscore.tenify()
        else:
            plscore.detenify()


def _detect_objects_roadrunner_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_roadrunner_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
#     objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
#     if hud:
#         objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
#         if ram_state[19] < 10:
#             objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
#         objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
#         if ram_state[18] < 10:
#             objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
#         objects["logo"] = 62, 189, 32, 7, 20, 60, 0
#         objects["time1"] = 63, 17, 6, 7, 20, 60, 0
#         objects["time2"] = 73, 18, 2, 5, 20, 60, 0
#         objects["time3"] = 79, 17, 6, 7, 20, 60, 0
#         objects["time4"] = 87, 17, 6, 7, 20, 60, 0
#     info["objects"] = objects