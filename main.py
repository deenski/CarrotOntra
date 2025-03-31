# Example file showing a circle moving on screen
import logging
import sys
import pygame

from pygame.locals import QUIT, KEYUP, KEYDOWN, K_w, K_s, K_a, K_d

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="game.log",
    level=logging.DEBUG,
    filemode="w",  # overwrites file
    format="{%(asctime)s - %(levelname)s - %(message)s}",  # structured logs ftw
)

# pygame setup
clock = pygame.time.Clock()
logging.info("initializing pygame")
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
movement = [0, 0]

pygame.display.set_caption("CarrotOntra")

BASE_IMAGES_PATH = "assets/images"

logging.info("pygame initialized")
logging.info("loading assets")

# game variables
scroll = 0
bg_imgs = []
level_length = 5000
player_pos = pygame.Vector2(50, 50)
player = pygame.draw.circle(screen, "black", player_pos, 40)
right = False
left = False
up = False
down = False


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            logging.info("collision detected")
            collisions.append(tile)

    return collisions


def move(rect, movement, tiles):  # movement = [5,2]
    rect.x += movement[0]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.rect.left
        if movement[0] < 0:
            rect.left = tile.rect.right
    rect.y += movement[1]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.rect.top
        if movement[1] < 0:
            rect.top = tile.rect.bottom
    return rect


class Tile(pygame.sprite.Sprite):
    # Call the parent class (Sprite) constructor
    def __init__(self, image, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image, namehint="tile").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = screen.width / 2
        self.y = 255

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


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
        # 1 * 0 * 0.333 = 0, 1*1*.333 = .333 (layer 1),
        # 1*2*.333 = 0.666 (foreground)
        # adjust decimal to go faster or slower .1 is slower 0 is stopped
        speed = 1 + layer_idx * 0.333

        # the secret to infinite scrolling is the modulus
        # first loop: (0 * 0) % anything = 0
        # sixth loop: (foreground after 1 keypress): (5 * .666) % 1024 = 3.33
        # 600th loop: (3000 * .666) % 1024 = 974
        # 2048 % 1024 = 0
        offset = (scroll * speed) % bg_width

        # Draw tiles
        for x in range(-1, num_tiles):
            screen.blit(img, ((x * bg_width) - offset, 0))


tile = Tile(f"{BASE_IMAGES_PATH}/ground_tile_test.png", 64, 64)
sprite_group = pygame.sprite.Group([tile])


logging.info("assets loaded")
logging.info("starting game")

while running:
    screen.fill((0, 0, 0))

    movement = [0, 0]

    if right:
        movement[0] += 5
    if left:
        movement[0] -= 5
    if up:
        movement[1] -= 5
    if down:
        movement[1] += 5
   
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                right = True 
            if event.key == K_a:
                left = True 
            if event.key == K_s:
                down = True 
            if event.key == K_w:
                up = True 
        if event.type == KEYUP:
            if event.key == K_d:
                right = False 
            if event.key == K_a:
                left = False 
            if event.key == K_s:
                down = False 
            if event.key == K_w:
                up = False 

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background images
    draw_bg()

    # draw tile. TODO: not fuck this up
    sprite_group.draw(screen)

    # draw tile
    tile.update()

    movement = [0, 0]

    if right:
        movement[0] += 5
    if left:
        movement[0] -= 5
    if up:
        movement[1] -= 5
    if down:
        movement[1] += 5
   
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                right = True 
            if event.key == K_a:
                left = True 
            if event.key == K_s:
                down = True 
            if event.key == K_w:
                up = True 
        if event.type == KEYUP:
            if event.key == K_d:
                right = False 
            if event.key == K_a:
                left = False 
            if event.key == K_s:
                down = False 
            if event.key == K_w:
                up = False 


    player = move(player, movement, [tile])
    pygame.draw.rect(screen, (255, 255, 255), player)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a] and scroll > 0:
    #     if player_pos.x > 500:
    #         player_pos.x -= 300 * dt
    #         tile.x -= 300 * dt
    #     scroll -= 5
    # if keys[pygame.K_d] and scroll < level_length:
    #     logger.info("player moving to the right")
    #     if player_pos.x < 300:
    #         player_pos.x += 300 * dt
    #         tile.x += 300 * dt
    #     scroll += 5

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000
    clock.tick(60)

pygame.quit()
logging.info("game shut down gracefully")
logging.info("-------------------------")
