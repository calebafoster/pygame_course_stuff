import pygame, sys
from pathlib import Path
from random import randint, uniform


class Ship(pygame.sprite.Sprite):

    def __init__(self,groups): 

        # init parent class
        super().__init__(groups)

        # create surface
        self.image = pygame.image.load(IMG_DIR / 'ship.png').convert_alpha()

        # create rect
        self.rect = self.image.get_rect(center = (RESO_W / 2, RESO_H / 2))

        self.mask = pygame.mask.from_surface(self.image)

        # Timer
        self.can_shoot = True
        self.shoot_time = None
        self.laser_cd = 50
    

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos


    def laser_timer(self,duration = 300):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > duration:
                self.can_shoot = True

    def laser_shoot(self):
        m1_bool = pygame.mouse.get_pressed()[0]
        if m1_bool and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Laser(self.rect.midtop,laser_group)
            sound.laser.play()

    def meteor_collisions(self):
        if pygame.sprite.spritecollide(self,meteor_group,True,pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()


    def update(self):
        self.laser_timer(self.laser_cd)
        self.input_position()
        self.laser_shoot()
        self.meteor_collisions()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups, speed = 1000):
        # basic setup
        super().__init__(groups)
        self.image = pygame.image.load(IMG_DIR / 'laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

        # motion setup
        self.speed = speed
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)

    def meteor_collisions(self):
        if pygame.sprite.spritecollide(self,meteor_group,True,pygame.sprite.collide_mask):
            self.kill()
            sound.explosion.play()
            score.count += 5
    

    def update(self):
        # motion calc
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.meteor_collisions()
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):

    def __init__(self, pos, groups):
        # Basic Setup
        super().__init__(groups)
        meteor_surf = pygame.image.load(IMG_DIR / 'meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf,meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

        # motion setup
        self.speed = randint(400,600)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)

        # rotation logic
        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation,1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # motion calc
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.rotate()

        if self.rect.top > RESO_H:
            self.kill()

class Score:
    def __init__(self) -> None:
        self.font = pygame.font.Font(IMG_DIR / 'subatomic.ttf',50)

        self.score = 0
        self.count = 0

    def display(self):
        self.score = (pygame.time.get_ticks() // 1000) + self.count
        score_text = f'Score: {self.score}'
        text_surf = self.font.render(score_text, True, "white")
        text_rect = text_surf.get_rect(topleft = (20, 20))
        display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(
            display_surface,
            ('white'),
            text_rect.inflate(30,30),
            width = 8,
            border_radius = 5
        )

class SoundFX:
    def __init__(self):
        self.laser = pygame.mixer.Sound(SOUND_DIR / 'laser.ogg')
        self.explosion = pygame.mixer.Sound(SOUND_DIR / 'explosion.wav')
        self.background = pygame.mixer.Sound(SOUND_DIR / 'music.wav')


# basic pathing
ROOT_DIR = Path(__file__).parent
IMG_DIR = ROOT_DIR / 'graphics'
SOUND_DIR = ROOT_DIR / 'sounds'


# basic setup
pygame.init()
RESO_W,RESO_H = 1280,720
display_surface = pygame.display.set_mode((RESO_W,RESO_H))
pygame.display.set_caption("Asteroid City")
clock = pygame.time.Clock()

background_surf = pygame.image.load(IMG_DIR / 'background.png').convert()

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,50)

# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

ship = Ship(spaceship_group)
score = Score()
sound = SoundFX()

sound.background.play(loops=-1)

while True:

    #event list
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == meteor_timer:
            meteor_y_pos = randint(-100,-50)
            meteor_x_pos = randint(-100,RESO_W + 100)
            Meteor(pos = (meteor_x_pos,meteor_y_pos), groups = meteor_group)


    # delta time
    dt = clock.tick() / 1000

    # draw graphics
    display_surface.blit(background_surf,(0,0))

    # update
    score.display()
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)


    # draw the frame
    pygame.display.update()