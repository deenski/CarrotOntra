# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

pygame.display.set_caption("CarrotOntra")
BASE_IMAGES_PATH = "assets/images"

# TODO: loop through this shit and add them to an array, then blit each item in the array
bg_img_layer_1 = pygame.image.load(f"{BASE_IMAGES_PATH}/bg_forest_layers/bg_forest_a.png").convert()
bg_img_layer_2 = pygame.image.load(f"{BASE_IMAGES_PATH}/bg_forest_layers/bg_forest_b.png").convert_alpha()
bg_img_layer_3 = pygame.image.load(f"{BASE_IMAGES_PATH}/bg_forest_layers/bg_forest_c.png").convert_alpha()
bg_img_layer_2_x = 0
bg_img_layer_3_x = 0
bg_img_y = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    screen.fill((0,0,0))
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(bg_img_layer_1, (0,0))
    screen.blit(bg_img_layer_2, (bg_img_layer_2_x, bg_img_y))
    screen.blit(bg_img_layer_3, (bg_img_layer_3_x, bg_img_y))
    

    pygame.draw.circle(screen, "yellow", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()