import pygame, time, random, math
from pygame.locals import *
# THE LEVELS ARE HERE, they
# are created by this program with 's'

from locals.randomize_crystals import *

group = []
class Particles(pygame.sprite.Sprite):
    "Creates particles starting from pos with a color"
 
    def __init__(self, pos, y_dir, color, sparse=0, turn="off"):
        super(Particles, self).__init__()
        self.particles_list = []
        self.pos = pos
        self.color = color
        self.y_dir = y_dir
        self.sparse = sparse # generate particles not from the same starting point
        # self.generate_particles()
        group.append(self)
        self.turn = turn # this makes the effect visible
 
    def choose_y_dir(self):
        "Makes particles go in every direction you want"
 
        # Make the flow go down
        if self.y_dir == "down":
            y_dir = 2
 
        elif self.y_dir == "up":
            y_dir = -2
 
        # Make the particles spread all y_dirs
        elif self.y_dir == "all":
            y_dir = random.randrange(-2, 2, 1)
 
        return y_dir
 
    def generate_particles(self):
        "List with position etc of particles"
 
        if self.sparse == 1:
            self.pos[0] = random.randint(0, 600)
 
        # setting the data for each particles
        origin = [self.pos[0], self.pos[1]] # Starting here each particles
        y_dir = self.choose_y_dir()
        x_dir = random.randint(0, 20) / 10 - 1
        dirs = [x_dir, y_dir] # movement
        radius = random.randint(4,6) # radius
        # Appending data to the list
        self.particles_list.append([origin, dirs, radius])
        self.generate_movements()
 
    def generate_movements(self):
        
        # Moving the coordinates and size of self.particles_list
        for particle in self.particles_list[:]:
            particle[0][0] += particle[1][0] # x pos += x_dir
            particle[0][1] += particle[1][1] # y pos += y_dir
            particle[2] -= 0.05 # how fast circles shrinks
            particle[1][1] += 0.01 # circles speed
            # if particle[2] &lt;= 0:
            if particle[2] >= 0:
                self.particles_list.remove(particle)
            # do not call draw from here: it slows down the frame rate
            # self.draw()
    
    def draw(self):
        "Draws particles based on data in the self.particles_list"
        if self.turn == "on":
            for particle in self.particles_list:
                 pygame.draw.circle(
                    screen, (self.color),
                (round(particle[0][0]), round(particle[0][1])),
                 round(particle[2]))
# Some random colors
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
# Creating the list with particles ready to be drawn

def init():
    pygame.init()
    pygame.display.init()
    pygame.mixer.init()

def generate():
    "Start drawing all circles on the screen"
    for par in group:
        par.generate_particles()
        par.draw()
# this function randomize the crystals
layout = randomize_crystals()
COUNTDOWN_LIMIT = 2000
init()
Particles([0, 0], y_dir="down", color=WHITE, sparse=1)

# DISPLAY SURFACES
# DISPLAY IS THE MAIN SURFACE
# SCREEN IS THE SURFACE TO BLIT ON DISPLAY SCALED

# DISPLAY IS 2x SCREEN

# 24.7.2021 - game5c.py - random crystals in every room
'''
when load the level:
for every -1, put the coords into a list, then
choose one element of the list and put the crystal
to those coords

'''
# next: closed rooms that opens only after getting the crystal
# change crystal to... something referring to skateboard
# better animation for double jumping
# converting collision with daflyffy method or my method (just around the player)

screen_ratio = 3
display = pygame.display.set_mode((480*screen_ratio + 64, 288*screen_ratio))
screen = pygame.Surface((480, 288))
pygame.display.set_caption("Crystals of Time by SmellyFrog")

# ================ I M A G E S =============== LOAD into Surfaces =====
spr_player = pygame.image.load("assets/player3a.png").convert_alpha()
# ======================= IMAGES ==============================
player_rect = spr_player.get_rect()
ball1 = pygame.image.load("assets/ball1.png").convert_alpha()
ball2 = pygame.image.load("assets/ball2.png").convert_alpha()
spr_tiles = pygame.image.load("assets/tiles4.png").convert_alpha()
NUM_OF_TILES = spr_tiles.get_size()[0] // 32
spr_crystal1 = pygame.image.load("assets/crystal.png").convert_alpha()
spr_crystal2 = pygame.image.load("assets/crystal2.png").convert_alpha()
spr_particle = pygame.image.load("assets/particles.png").convert_alpha()
spr_number = pygame.image.load("assets/number.png").convert_alpha()
background = pygame.image.load("assets/background.png").convert()
title = pygame.image.load("assets/title.png").convert()

# ==================== SOUNDS ========================
sfx_crash = pygame.mixer.Sound("assets/crash.wav")
# sfx_crash.set_volume(0.5)
sfx_collect = pygame.mixer.Sound("assets/collect.wav")
sfx_crystal = pygame.mixer.Sound("assets/crystal.wav")
jump = pygame.mixer.Sound("assets/jump.mp3")

# THE SPRITE FOR THE PLAYER
class Player():
    def __init__(self, x, y):
        # super(Player, self).__init__()
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        # credo che siano 1 quanto c'è un tile sotto, sopra...
        self.frame = 0
        self.faceRight = True
        self.timer = 0
        self.jump_once = 0
        self.collision_reset()

    def collision_reset(self):
        self.bottomCollision = False
        self.topCollision = False
        self.leftCollision = False
        self.rightCollision = False

    def inertial_speed(self):
        ''' this makes the player slide on the tiles depending on speed '''
        if self.xSpeed > 0: # decelera quando cade su un tile andando verso destra
            self.xSpeed -= 0.2 # [[[[[[[[ 0.3 valore originale ]]]]]]]]
        elif self.xSpeed < 0: # se va verso sinistra decelera con un + perchè...
            self.xSpeed += 0.2 # CAMBIO!!!! #######>>>> 0.3 valore originale
        if abs(self.xSpeed) < 0.3: # quando la velocità è inferiore a 0.3 si ferma
            self.xSpeed = 0
    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.ySpeed < 8:
            self.ySpeed += 0.5
        if self.bottomCollision: # quando c'è un tile sotto non cade
            self.ySpeed = 0
            self.inertial_speed()
        if keys[pygame.K_x] and (self.bottomCollision or self.rightCollision or self.leftCollision):# and not self.topCollision:
            if self.jump_once < 1:
        # if keys[pygame.K_UP] and self.bottomCollision:
                self.ySpeed = -8
                self.bottomCollision = 0
                self.jump_once += .5
            pygame.mixer.Sound.play(jump)
        elif keys[pygame.K_z] and keys[pygame.K_RIGHT]:
            if self.xSpeed > 3:
                self.xSpeed = 0
        elif keys[pygame.K_z] and keys[pygame.K_LEFT]:
            if self.xSpeed < -3:
                self.xSpeed = 0
             #############
        #    LEFT - RIGHT
             #############
        elif keys[pygame.K_LEFT] and self.xSpeed > -3:
            self.xSpeed -= 0.2
            self.faceRight = False
            self.frame = (timer % 16 < 8) # is 1 or 0
        elif keys[pygame.K_RIGHT] and self.xSpeed < 3:
            self.xSpeed += 0.2
            self.faceRight = True
            self.frame = (timer % 16 < 8) # is 1 or 0
        # else:
        # IT'S IN THE AIR ----------------- ATTEMPT TO MAKE AN ANIMATION
        if not self.bottomCollision and abs(self.ySpeed) > 1:
            self.frame = 1 + (timer % 16 < 1) # ADDED THIS TO ANIMATE IT?
        if self.timer > 0:
            self.frame = (timer % 16 < 8) + 3
            
        self.collision_reset()

            
    def draw(self):

        screen.blit(
            spr_player, 
            (int(self.x), int(self.y)),
            # Here is where he gets the sprite from the spritesheet
            (self.frame * 32, # x position for the pose
            (not self.faceRight) * 32, # y position 0 = left 1=left
            32, 32))
        # pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))

class Terrain():
    def __init__(self, x, y, Type, level):
        self.x = x
        self.y = y
        self.level = level
        self.col = False
        self.type = Type
    def update(self):
        # Se il giocatore si trova sopra ad un tile... cos'è self.col



        if self.type == 4:
            if player.x + 32 > self.x and player.x < self.x + 16:# and not self.col:
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    player.ySpeed = -10
                    player.bottomCollision = False
                    pygame.mixer.Sound.play(jump)
                    remove.append(self)

        # il terzo gruppo di tiles
        elif self.level == 64:
            if player.x + 16 > self.x and player.x < self.x + 31 and not self.col: # collition with self?
            # Se i piedi del player si trovano all'altezza del tile, cioè sopra...
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    # il player viene piazzato esattamente sopra il tile
                    player.y = self.y - 32 # sarebbe che il player si trova 32 pixel sopra la base del tile
                    player.ySpeed = 0
                    player.bottomCollision = True # Collition with the bottom, the player is on the terrain
                    self.col = True #Vuol dire che il tile è in contatto con il player
                    player.jump_once = 0
                    
        
        else:
            if player.x + 16 > self.x and player.x < self.x + 31 and not self.col: # collition with self?
            # Se i piedi del player si trovano all'altezza del tile, cioè sopra...
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    # il player viene piazzato esattamente sopra il tile
                    player.y = self.y - 32 # sarebbe che il player si trova 32 pixel sopra la base del tile
                    player.ySpeed = 0
                    player.bottomCollision = True # Collition with the bottom, the player is on the terrain
                    self.col = True #Vuol dire che il tile è in contatto con il player
                    player.jump_once = 0

                    # Tipes of tiles

                    # BACK
                    if self.type == 3:
                        player.x -= 96
                        pygame.mixer.Sound.play(sfx_crystal)

                    # TRAMPOLINE
                    
                    
                    # DOWN
                    
                    elif self.type == 5:
                        player.y += 64
                        pygame.mixer.Sound.play(sfx_crystal)


                if player.x > self.x and player.x < self.x + 31:
                    if player.y > self.y + 16 and player.y < self.y + 31:
                        player.y = self.y + 31
                        player.ySpeed = 0 # non salta più
                        player.topCollision = True # collide col tile verso l'alto
                        self.col = True # la collisione del player c'è
            
            # se i piedi sono sopra un tile e la testa è minore della base del tile e non c'è collisione
            # if player.y + 32 > self.y and player.y < self.y + 32 and not self.col:
            # if player.y + 31 > self.y and player.y < self.y + 31 and not self.col:
            if player.y + 31 == self.y + 31 and not self.col:

                if player.x + 31 > self.x and player.x + 31 < self.x + 16:
                    player.x = self.x - 32
                    player.xSpeed = -0.4
                    player.rightCollision = True
                    self.col = True
                # COLLITION LEFT
                if player.x > self.x + 16 and player.x < self.x + 31:
                    player.x = self.x + 31
                    player.xSpeed = 0.4
                    player.leftCollision = True
                    self.col = True
            self.col = False
        
    def draw(self):
        # this blits the tiles at the position, but starting with 6*32 end ending 32 further
        if self not in remove:
            if self.type == 4:
                screen.blit(spr_tiles, (int(self.x), int(self.y)+ (timer % 16 < 8)), (self.type * 32, 0 + self.level, 32, 32))
                # screen.blit(spr_tiles, (int(self.x)+ (timer % 16 < 8), int(self.y)+ (timer % 16 < 8)), (self.type * 32 + (timer % 16 < 8) * 32, 0 + self.level, 32, 32))
            else:
                screen.blit(spr_tiles, (int(self.x), int(self.y)), (self.type * 32, 0 + self.level, 32, 32))

class Crystal():
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
    def update(self):
        global countdown
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < 32 and countdown > 0:
            collected.append((self.x, self.y, room_num))
            print(f"Collezionate: {len(collected)} gemme")
            # DO not want the player to stop when collects a crystal (it is annoying)
            player.timer = 15
            # but I do want countdown to go back
            
            # You make the countdown to go back 2.7.21 8:39
            countdown += 150
            

            player.xSpeed = 0
            pygame.mixer.Sound.play(sfx_collect)
        if (self.x, self.y, self.num) in collected:
            remove.append(self)

            
    def draw(self):
        if not self in remove:
            screen.blit(spr_crystal1,(int(self.x), int(self.y) + math.sin(timer*3 / 32) * 16), ((timer % 16 < 8) * 32, 0, 32, 32))
            screen.blit(ball1, ((int(self.x) + math.cos(timer / 32) * random.randrange(8, 16, 8)), int(self.y) + math.sin(timer / 16) * 16), ((timer % 16 < 16) * 32, 0, 32, 32))
            # screen.blit(ball2, ((int(self.x) - math.cos(timer / 8) * 16), int(self.y) + math.cos(timer / 16) * 16), ((timer % 16 < 8) * 32, 0, 32, 32))


class LargeCrystal():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.alive = True
        self.winCountdown = 500
    def update(self):
        global alive
        global room_num
        global player_y
        global player_x
        global countdown
        # Se il la radice quadrata della somma dei quadrati di distanza orizz. e vert. è minore di 96
        if ((player.x - self.x)**2 + (
            player.y - self.y)**2)**0.5 < 96 and self.alive and countdown > 0:
            self.timer += 1
            if self.timer > 80 and self.alive:
                player.timer = 3000
                self.alive = False
                pygame.mixer.Sound.play(sfx_crash)
                pygame.mixer.music.stop()
        if not self.alive:
            self.winCountdown -= 1
            if self.winCountdown <= 0 and countdown > 0:
                game_over()
            
    def draw(self):
        if not self in remove:
            screen.blit(spr_crystal2, (int(self.x), int(self.y)), (self.timer // 32 * 64, 0, 64, 96))



def game_over():
    """ Call this when the player game ends """
    display.fill(0)
    alive = False
    room_num = 0
    player_y = 42069
    countdown = COUNTDOWN_LIMIT
    player_x = 42069
    collected.clear()




   
player_y = 42069
player_x = 42069
collected = []
room_num = 0
timer = 0
countdown = COUNTDOWN_LIMIT
run = True

room_r = len(layout[room_num])
room_c = len(layout[room_num][0])

def music_on():
    music = pygame.mixer.music.load("assets/swinging in the night sky2.wav")
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1)

# str_num_tiles = [str(x) for x in range(NUM_OF_TILES)]
# str_num_tiles = "".join(str_num_tiles)
music_on()
color_line = 255, 255, 0
font = pygame.font.SysFont("Arial", 20)
def room_number():
    rn = font.render(f"{room_num}", 1, (255, 255, 255))
    return rn


def change_room():
    global room_num, player_x, player_y

    if player.x + 16 < 0:
        player_y = player.y
        player_x = 480 - 24
        room_num -= 1
    elif player.x + 16 > 480:
        player_y = player.y
        player_x = -8
        room_num += 1
    if player.y > 288:
        player.y = 0

def time_indicator():
    pygame.draw.line(screen, (200, 255, 255), (239, 280 - (countdown // 7)), (239, -4), 6)
    pygame.draw.circle(screen, (200, 255, 255), (240, 280 - (countdown // 7)), 8)
    pygame.draw.circle(screen, (255, 255, 255), (240, 280 - (countdown // 7)), 4)

font = pygame.font.SysFont("Arial", 14)
msg = font.render("Hello", 1, (0, 255, 0))
def message(text):
    global msg
    # screen0.fill(0, (0, 288, 480, 32))
    msg = font.render(text, 1, (0, 255, 0))
    return msg

while run:
    ### level generation

    load = []
    remove = []
    player = Player(0, 0)


    for i in range(room_r):
        for j in range(room_c): # ================= Put the plauer in position
            if layout[room_num][i][j] == "P":
                player = Player(j*32, i*32)
                load.append(player)
                # ========================================== Here go the tiles
            elif layout[room_num][i][j] != " ":# and layout[room_num][i][j] != "P":
                if int(layout[room_num][i][j]) < 100:
                    level = 0
                    val = int(layout[room_num][i][j])
                    # if val == 10:
                    #     pass
                    if val > 10 and val < 22:
                        val = val - 11
                        level = 32
                        load.append(Terrain(j*32, i*32, val, level))
                    elif val > 20:
                        val = val - 22
                        level = 64
                        load.append(Terrain(j*32, i*32, val, level))
                    else:
                        load.append(Terrain(j*32, i*32, val, level))
                    # ======================================= CRYSTAL
                elif layout[room_num][i][j] == "100":
                    load.append(Crystal(j*32, i*32, room_num))
                elif layout[room_num][i][j] == "101":
                    load.append(LargeCrystal(j*32, i*32))

    if player not in load:# and room_num not in (0, 14, 15):
        load.append(player)

    if player_y != 42069:
        player.y = player_y
        player.x = player_x



    
    clock = pygame.time.Clock()
    alive = True
    while run and alive:



        timer += 1
        # Countdown starts from second room
        if countdown <= 3000 and room_num >= 1:
            countdown -= 1

        clock.tick(60)

        screen.fill((0, 0, 0))
        if room_num == 0:
            screen.blit(title, (0, 0))
        else:
            screen.blit(background, (0, 0))

        # meteor

        # WHEN TIME'S OVER
        if countdown == 0:
            pygame.mixer.Sound.play(sfx_crash)
            pygame.mixer.music.stop()
        # This draws the the circle
        if countdown < 0:
            pygame.draw.circle(screen, (255, 255, 255), (240, 204), -10 * countdown)
        if countdown < -100:
            alive = False
            room_num = 0
            countdown = 1500
            player_y = 42069
            player_x = 42069
            collected = []

        if player.timer > 0:
            player.timer -= 1
            countdown += 11
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # 
        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            load.remove(obj)
        # load = []
        remove = []

        if player.x + 16 > 480 or player.x + 16 < 0:
            alive = False

        # counter

        if countdown > 0 and countdown < COUNTDOWN_LIMIT and room_num >= 1:
            for i in range(len(str(countdown))):
                screen.blit(spr_number, (16 + i *16, 16), (int(str(countdown)[i]) * 16, 0, 16, 32))

        if room_num == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            room_num += 1
            alive = False

            player_y = 42069
            countdown = COUNTDOWN_LIMIT
            player_x = 42069
            collected = []
        

        # COLOR OF THE BACKGROUND OF THE PRIMARY SCREEN
        display.fill((0, 255, 255))
        

        if countdown > 0:
            if countdown < 300 and countdown > 200:
                color_line = 255, 100, 0
            elif countdown < 200:
                color_line = 255, 0, 0



            # INDICATES THE TIME PASSING ON THE RIGHT OF THE SCREEN
            pygame.draw.line(display,
                color_line, # color
                (488*2 + 32, 0 - countdown // 10), # (x, y)
                (488*2 + 32, 100 - countdown // 10), # (x, y)
                100)
        # pygame.draw.circle(display, (100, 255, 0), (488*2 + 32, 160 - (countdown // 10)), 8)
        # pygame.draw.circle(display, (255, 255, 255), (488*2 + 32, 164 - (countdown // 10)), 4)

        generate()
        time_indicator()
        display.blit(pygame.transform.scale(screen, (488*screen_ratio  , 288*screen_ratio)),(0, 0))
        display.blit(room_number(), (480, 288))
        msg = message(f"Crystals: {len(collected)}")
        display.blit(msg, (10, 10))
        pygame.display.flip()
        change_room()

    # if player.y + 16 < 0:
    #     room = 0
            
pygame.quit()
