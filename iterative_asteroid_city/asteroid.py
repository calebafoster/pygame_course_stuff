import pygame, sys
from pathlib import Path
from random import randint, uniform

ROOT_DIR = Path(__file__).parent
IMG_DIR = Path(__file__).parent / 'graphics'
SOUND_DIR = ROOT_DIR / 'sounds'


# func that shoots laser
def laser_update(laser_list, speed = 300):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed = 300):
    for meteor_tuple in meteor_list:

        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]

        meteor_rect.center += direction * speed * dt

        if meteor_rect.top > reso_height:
            meteor_list.remove(meteor_tuple)


def display_score():
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_text, True, (255,255,255))
    text_rect = text_surf.get_rect(center = (reso_width / 2, reso_height - 80))

    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30,30), width = 8, border_radius = 5)


def laser_timer(can_shoot, duration):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot




# DISPLAY
pygame.init()
reso_width, reso_height = 1280,720
display_surface = pygame.display.set_mode((reso_width,reso_height))
pygame.display.set_caption("Asteroid City")
clock = pygame.time.Clock()

# ship immport
ship_surf = pygame.image.load(IMG_DIR / 'ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (reso_width/2,reso_height/2))

# laser import
laser_surf = pygame.image.load(IMG_DIR / 'laser.png').convert_alpha()
laser_list = []

# meteor import
meteor_surf = pygame.image.load(IMG_DIR / 'meteor.png').convert_alpha()
meteor_list = []

# background import
background = pygame.image.load(IMG_DIR / 'background.png').convert()

# laser timer
can_shoot = True
shoot_time = None

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,500)

# sound import
explosion = pygame.mixer.Sound(SOUND_DIR / 'explosion.wav')
background_music = pygame.mixer.Sound(SOUND_DIR / 'music.wav')
laser_sound = pygame.mixer.Sound(SOUND_DIR / 'laser.ogg')

# TEXT
font = pygame.font.Font(IMG_DIR / 'subatomic.ttf', 50)


while True:

    # event list
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom = (ship_rect.midtop))
            laser_list.append(laser_rect)

            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # play sound
            laser_sound.play()

        if event.type == meteor_timer:

            # random pos
            x_pos = randint(-0,reso_width + 100)
            y_pos = randint(-100,-50)

            # creating the rect
            meteor_rect = meteor_surf.get_rect(midbottom = (x_pos,y_pos))

            # random direction
            direction = pygame.math.Vector2(uniform(-0.5,0.5),1)

            meteor_list.append((meteor_rect,direction))

    
    # framerate
    dt = clock.tick(144) / 1000

    # mouse movement
    ship_rect.center = pygame.mouse.get_pos()


    # 2. Updates
    laser_update(laser_list)
    can_shoot = laser_timer(can_shoot, 300)

    meteor_update(meteor_list)

    # meteor ship collisions
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()
        

    # laser meteor collisions
    for rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if rect.colliderect(meteor_rect):
                explosion.play()
                laser_list.remove(rect)
                meteor_list.remove(meteor_tuple)

    # background
    display_surface.fill((0,0,0))
    display_surface.blit(background,(0,0))

    # score
    display_score()

    # ship
    display_surface.blit(ship_surf,ship_rect)

    # laser logic
    for rect in laser_list:
        display_surface.blit(laser_surf,rect)

    # meteor logic
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf,meteor_tuple[0])    # 3. show the frame to the player / update the display surface

    pygame.display.update()
