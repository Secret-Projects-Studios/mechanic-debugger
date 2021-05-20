import pygame, logging, inspect


SCREENWIDTH = 1366
SCREENHEIGHT = 768
FACING_DIRECTION = ""
PLAYERX = int(SCREENWIDTH * 0.2)
last_update = 0
PLAYER_GRAV = 0.8
PLAYER_FRIC = -0.12
PLAYER_ACC = 0.5
FPS = 500
FPSCLOCK = pygame.time.Clock()
BASEY = SCREENHEIGHT * 0.79
canvas = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
logger = logging.getLogger()
handler = logging.StreamHandler()
walls = pygame.sprite.Group()
sprites = pygame.sprite.LayeredUpdates()
players = pygame.sprite.LayeredUpdates()
trees = pygame.sprite.LayeredUpdates()
obstacles = pygame.sprite.LayeredUpdates()
moved = False
GAME_METHOD = True


def log_data(method, message, class_name, func_name):
	logger.setLevel(logging.DEBUG)
	f_format = logging.Formatter(f'%(asctime)s [{class_name} - {func_name} - %(levelname)s]  - %(message)s')
	handler.setFormatter(f_format)
	logger.addHandler(handler)

	_log = getattr(logger, method)
	_log(message)