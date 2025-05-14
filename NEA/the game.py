import pygame, random
from classes import SCREEN_SIZE, WHITE, BLUE, BLACK, RED, GREEN, TILE_SIZE, characters, Character
from classes import Weapons, Sword, Object, weapons, objects

pygame.display.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

def create_objects():
    for i in range(random.randint(1, 10)):
        x = random.randint(0, SCREEN_SIZE[0])
        y = random.randint(0, SCREEN_SIZE[0])
        o = Object(x, y)
        objects.add(o)

def run_game():
    c = Character(400, 400)
    create_objects()
    s = Sword(100, 200)
    characters.add(c)
    weapons.add(s)
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_u]:
                    c.pick_up_weapon()
                if keys[pygame.K_j]:
                    if s.have_owner():
                        o, power = s.attack()
        s.update_position()
        c.move()
        c.animation()
        characters.draw(screen)
        objects.draw(screen)
        weapons.draw(screen)
        pygame.display.update()
        clock.tick(60)

run_game()