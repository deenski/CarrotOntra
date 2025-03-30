# Example file showing a circle moving on screen
import logging

import pygame

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="game.log", level=logging.DEBUG)

# pygame setup
logging.info("initializing pygame")
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

pygame.display.set_caption("CarrotOntra")

BASE_IMAGES_PATH = "assets/images"

logging.info("pygame initialized")
logging.info("loading assets")

# game variables
scroll = 0
bg_imgs = []
level_length = 5000

# load images from 0-2, 0 being furthest back
for i in range(3):
    bg_img = pygame.image.load(
        f"{BASE_IMAGES_PATH}/bg_forest_layers/bg_forest_{i}.png"
    ).convert_alpha()
    logging.info(bg_img.__dir__)
    bg_imgs.append(bg_img)


bg_width = bg_imgs[0].get_width()


# first image is furthest in the background
def draw_bg():
    screen_width = screen.get_width()
    num_tiles = (screen_width // bg_width) + 2

    for layer_idx, img in enumerate(bg_imgs):
        # Assign increasing speed to background layers from back to front
        # 1 * 0 * 0.333 = 0, 1*1*.0333 = .0333 (layer 1),
        # 1*2*.0333 = 0.666 (foreground)
        speed = 1 + layer_idx * 0.333 # adjust decimal to go faster or slower .1 is slower 0 is stopped

        # the secret to infinite scrolling is the modulus
        # first loop: (0 * 0) % anything = 0
        # sixth loop: (foreground after 1 keypress): (5 * .666) % 1024 = 3.33
        # 600th loop: (3000 * .666) % 1024 = 974
        offset = (scroll * speed) % bg_width 

        # Draw tiles
        for x in range(-1, num_tiles):
            screen.blit(img, ((x * bg_width) - offset, 0))


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
logging.info("assets loaded")
logging.info("starting game")
while running:
    screen.fill((0, 0, 0))
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background images
    draw_bg()

    # draw player
    pygame.draw.circle(screen, "yellow", player_pos, 40)

    # keypress event handlers
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a] and scroll > 0:
        if player_pos.x > 500:
            player_pos.x -= 300 * dt
        scroll -= 5
    if keys[pygame.K_d] and scroll < level_length:
        logger.info("player moving to the right")
        if player_pos.x < 300:
            player_pos.x += 300 * dt
        scroll += 5

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
logging.info("game shut down gracefully")
logging.info("-------------------------")
