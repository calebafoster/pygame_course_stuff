import pygame,sys
from pathlib import Path
from settings import *
from player import Player
from car import Car
from random import choice,randint
from sprite import SimpleSprite, TallSprite

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load(GRAPHICS_DIR / 'main/map.png').convert()
        self.fg = pygame.image.load(GRAPHICS_DIR / 'main/overlay.png').convert_alpha()
    
    def customize_draw(self):

        self.offset.x = player.rect.centerx - WIDTH_RESO / 2
        self.offset.y = player.rect.centery - HEIGHT_RESO / 2

        display_surface.blit(self.bg,-self.offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)

        display_surface.blit(self.fg,-self.offset)


# display shit
pygame.init()
display_surface = pygame.display.set_mode((WIDTH_RESO, HEIGHT_RESO))
pygame.display.set_caption('FUCK MUNGUS')
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# sprites
player = Player((2062,3274),all_sprites,obstacle_sprites)

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

# font
font = pygame.font.Font(None,50)
text_surf = font.render('YOU WON',True,'white')
text_rect = text_surf.get_rect(center = (WIDTH_RESO / 2,HEIGHT_RESO / 2))

# music
music = pygame.mixer.Sound(ROOT_DIR / 'audio/music.mp3')
music.play(loops=-1)

# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = GRAPHICS_DIR / f'objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf,pos,[all_sprites,obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
    path = GRAPHICS_DIR / f'objects/long/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        TallSprite(surf,pos,[all_sprites,obstacle_sprites])


while True:

    #event list
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # car timer stuff
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0],random_pos[1] + randint(-8,8))
                Car(pos,[all_sprites,obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]


    # delta time
    dt = clock.tick() / 1200



    if player.pos.y > 1180:
        
        display_surface.fill('black')

        all_sprites.update(dt)

        all_sprites.customize_draw()
    else:
        display_surface.fill((20,20,20))
        display_surface.blit(text_surf,text_rect)

    # draw the frame
    pygame.display.update()
