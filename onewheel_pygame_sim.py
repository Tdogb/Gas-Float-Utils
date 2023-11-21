import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    rect = pygame.Rect(0,0,200,20)
    rect.center = player_pos
    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.rect(screen, "red", rect, 100)
    font = pygame.font.Font('RobotoMono-VariableFont_wght.ttf', 32)
    l_force_text = font.render('10', True, "white")
    l_force_rect = l_force_text.get_rect()
    l_force_rect.center = pygame.Vector2(player_pos.x - 90, player_pos.y - 50)
    r_force_text = font.render('9', True, "white")
    r_force_rect = r_force_text.get_rect()
    r_force_rect.center = pygame.Vector2(player_pos.x + 90, player_pos.y - 50)
    screen.blit(l_force_text,l_force_rect)
    screen.blit(r_force_text,r_force_rect)

    rect.

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