import pygame
from pygame import *

pygame.init()

page = 0
screenWidth = 1200
screenHeight = 480
bulletRange = 200
bullets = []
clock = pygame.time.Clock()
# =====================================================================================================================
# setup pictures and music
# =====================================================================================================================
win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("On your own")
Title = pygame.image.load('TITLE.png')
title = pygame.transform.scale(Title, (300, 60))
TREE = pygame.image.load('tree.png')
tree = pygame.transform.scale(TREE, (150, 300))
exp = pygame.image.load("EXP.png")
EXP = pygame.transform.smoothscale(exp, (15, 15))

Sw = pygame.image.load("SW.png")
SW = pygame.transform.smoothscale(Sw, (15, 50))
SW_item = pygame.transform.rotate(SW, 90)
# =====================================================================================================================
# backGround images
# =====================================================================================================================
bg_0 = pygame.image.load('bg3.png')
bg_1 = pygame.image.load('bg2.png')
bg = pygame.image.load('bg4.png')
bg_2 = pygame.transform.smoothscale(bg, (1200, 480))

# =====================================================================================================================
# food images
# =====================================================================================================================
apple = pygame.image.load('apple.png')
pot = pygame.image.load('potion.png')
potion = pygame.transform.smoothscale(pot, (40, 40))
# =====================================================================================================================
# sound effects and music
# =====================================================================================================================

bulletSound = pygame.mixer.Sound('throw.wav')
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# =====================================================================================================================
# bird and goblin images
# =====================================================================================================================


bRight = [pygame.image.load('RB1.png'), pygame.image.load('RB2.png'), pygame.image.load('RB3.png'),
          pygame.image.load('RB4.png'), pygame.image.load('RB5.png'), pygame.image.load('RB6.png'),
          pygame.image.load('RB7.png'), pygame.image.load('RB8.png')]
bLeft = [pygame.image.load('LB1.png'), pygame.image.load('LB4.png'), pygame.image.load('LB3.png'),
         pygame.image.load('LB4.png'), pygame.image.load('LB5.png'), pygame.image.load('LB6.png'),
         pygame.image.load('LB7.png'), pygame.image.load('LB8.png')]

gRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
          pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
          pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
          pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
gLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
         pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
         pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
         pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
b_hitbox = [30, 40, 100, 60, bRight, bLeft]
g_hitbox = [17, 2, 31, 57, gRight, gLeft]


class player(object):
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                 pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 20
        self.visible = True
        self.score = 0

    def draw(self, window):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not self.standing:
                if self.left:
                    window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    window.blit(self.walkRight[0], (self.x, self.y))
                else:
                    window.blit(self.walkLeft[0], (self.x, self.y))
            pygame.draw.rect(window, (128, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health / 2)), 10))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = self.x - 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenWidth - 650 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, Colour, Facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = Colour
        self.Facing = Facing
        self.vel = 8 * Facing

    def draw(self, window):
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        window.blit(EXP, (self.x - 8, self.y - 8))
        # bulletSound.play


class enemy(object):
    def __init__(self, x, y, width, height, end, health, enemy_type, on_page):
        self.on_page = on_page
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.health = health
        self.full_health = self.health
        self.visible = True
        self.killCount = 0
        self.hh = self.enemy_type[3]
        self.hw = self.enemy_type[2]
        self.hy = self.enemy_type[1]
        self.hx = self.enemy_type[0]
        self.hitbox = (self.x + self.hx, self.y + self.hy, self.hw, self.hh)
        self.Image_right = self.enemy_type[4]
        self.Image_left = self.enemy_type[5]
        self.hp = self.health / 10

    def draw(self, window):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 3 * len(self.Image_right):
                self.walkCount = 0

            if self.vel > 0:
                window.blit(self.Image_right[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.Image_left[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (128, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health / self.hp)), 10))

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        self.hitbox = (self.x + self.hx, self.y + self.hy, self.hw, self.hh)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self, damage):
        hitSound.play()
        if self.health > 0:
            self.health -= damage
        else:
            self.visible = False
            self.killCount += 1
        print('hit')


class item(object):
    def __init__(self, x, y, width, height, Image, on_page):
        self.on_page = on_page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Image = Image
        self.visible = True
        self.collected = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        if self.visible:
            window.blit(self.Image, (self.x, self.y))


class Health_item(item):
    def __init__(self, x, y, width, height, health_points, Image, on_page):
        super().__init__(x, y, width, height, Image, on_page)
        self.health_points = health_points


def bullet_goblin_collision(bad_guy):
    if man.visible:
        for Bullet in bullets:
            if bad_guy.visible:
                if bad_guy.hitbox[1] + bad_guy.hitbox[3] > Bullet.y + Bullet.radius > bad_guy.hitbox[1]:
                    if Bullet.x + Bullet.radius > bad_guy.hitbox[0] - bad_guy.hitbox[2] and Bullet.x - Bullet.radius < \
                            bad_guy.hitbox[0] + bad_guy.hitbox[2]:
                        bad_guy.hit(2)
                        if bad_guy.visible:
                            man.score += 1
                            bullets.pop(bullets.index(Bullet))

            if screenWidth > Bullet.x > 0:
                Bullet.x += Bullet.vel
            else:
                bullets.pop(bullets.index(Bullet))


def player_enemy_collision(bad_guy):
    if man.visible:
        if bad_guy.visible:
            if man.hitbox[1] < bad_guy.hitbox[1] + bad_guy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    bad_guy.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > bad_guy.hitbox[0] and man.hitbox[0] < bad_guy.hitbox[0] + \
                        bad_guy.hitbox[2]:
                    man.hit()
                    man.health -= 5


def sword_enemy_collision(bad_guy):
    if bad_guy.visible:
        if man.right:
            if man.hitbox[1] < bad_guy.hitbox[1] + bad_guy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    bad_guy.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] + 50 > bad_guy.hitbox[0] and man.hitbox[0] < bad_guy.hitbox[0] + \
                        bad_guy.hitbox[2]:
                    bad_guy.hit(0.5)
                    man.score += 1
        if man.left:
            if man.hitbox[1] < bad_guy.hitbox[1] + bad_guy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    bad_guy.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > bad_guy.hitbox[0] and man.hitbox[0] < bad_guy.hitbox[0] + \
                        bad_guy.hitbox[2] + 50:
                    bad_guy.hit(0.5)
                    man.score += 1


def player_item_collision(Item_):
    if not Item_.collected:
        if Item_.visible:
            if man.hitbox[1] < Item_.hitbox[1] + Item_.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    Item_.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > Item_.hitbox[0] - Item_.hitbox[2] and man.hitbox[0] < \
                        Item_.hitbox[0] + \
                        Item_.hitbox[2]:
                    Item_.collected = True


def player_food_collision(health_item):
    if health_item.visible:
        if man.hitbox[1] < health_item.hitbox[1] + health_item.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                health_item.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > health_item.hitbox[0] - health_item.hitbox[2] and man.hitbox[0] < \
                    health_item.hitbox[0] + \
                    health_item.hitbox[2]:
                if health_item == golden_apple:
                    if man.health < 20:
                        man.health += 10
                        if man.health > 20:
                            man.health = 20
                        health_item.visible = False
                        health_item.collected = True
                    else:
                        man.health = 20
                        health_item.visible = True
                        health_item.collected = True
                if health_item == health_potion:
                    if man.health < 20:
                        man.health = 20
                        health_item.visible = False
                        health_item.collected = True


def redraw_game_window():
    if page == 0:
        win.blit(bg_0, (0, 0))
    elif page == 1:
        win.blit(bg_1, (0, 0))
    else:
        win.blit(bg_2, (0, 0))
    win.blit(title, (160, 10))
    for bad_guy in enemys:
        bad_guy.draw(win)
    # win.blit(tree, (500, 170))
    man.draw(win)

    if not sword.collected:
        sword.draw(win)

    if man.visible:
        if sword.collected:
            if man.right:
                win.blit(SW, (man.x + 35, man.y))
            else:
                win.blit(SW, (man.x + 15, man.y))
    text = font.render('score: ' + str(man.score), 1, (0, 0, 0))
    text_test = font.render('page: ' + str(page), 1, (0, 0, 0))

    for I in foods:
        if I.visible:
            I.draw(win)

    win.blit(text, (screenWidth - 160, 10))
    win.blit(text_test, (screenWidth - 400, 10))

    if man.visible:
        for Bullet in bullets:
            Bullet.draw(win)

    text1 = font.render('kills: ' + str(
        goblin1.killCount + goblin2.killCount + goblin3.killCount + bird1.killCount + bird2.killCount + bird3.killCount
        + bird4.killCount),
                        1, (0, 0, 0))
    win.blit(text1, (screenWidth - 260, 10))

    if man.health <= 0:
        deadText = font.render('you are dead', 1, (0, 0, 0))
        win.blit(deadText, (screenWidth / 2 - 100, 200))
        man.visible = False

    pygame.display.update()

    # =================================================================================================================
    # setup for main loop
    # =================================================================================================================


def bullet_range_limiter():
    for bullet in bullets:
        if bullet.Facing == 1:
            if bullet.x > man.x + man.width / 2 + bulletRange:
                bullets.pop(bullets.index(bullet))
        else:
            if bullet.x < man.x + man.width / 2 - bulletRange:
                bullets.pop(bullets.index(bullet))


# =====================================================================================================================
# create all object
# =====================================================================================================================
font = pygame.font.SysFont('comicsans', 30, True, True)

man = player(200, 410, 64, 64)

bird1 = enemy(500, 200, 64, 64, screenWidth - 100, 10, b_hitbox, 0)
bird2 = enemy(100, 200, 64, 64, screenWidth - 600, 10, b_hitbox, 2)
bird3 = enemy(500, 300, 64, 64, screenWidth - 100, 10, b_hitbox, 2)
bird4 = enemy(800, 200, 64, 64, screenWidth - 100, 10, b_hitbox, 2)
goblin1 = enemy(800, 410, 64, 64, screenWidth - 50, 10, g_hitbox, 0)
goblin2 = enemy(800, 410, 64, 64, screenWidth - 50, 20, g_hitbox, 1)
goblin3 = enemy(200, 410, 64, 64, screenWidth - 600, 20, g_hitbox, 1)

enemys = [goblin1, goblin2, goblin3, bird1, bird2, bird3, bird4]

health_potion = Health_item(1000, 430, 50, 50, 10, potion, 1)
golden_apple = Health_item(0, 430, 50, 50, 10, apple, 0)

sword = item(100, 455, 15, 50, SW_item, 1)
foods = [golden_apple, health_potion]
inventory = []
shootLoop = 0
run = True
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()
    redraw_game_window()
    player_item_collision(sword)
    bullet_range_limiter()

    for item in foods:
        if keys[pygame.K_r] and player_item_collision(item):
            if not item.collected:
                inventory.append(item)

    # =================================================================================================================
    # what sprite is visible on each page
    # =================================================================================================================
    for enemy in enemys:
        if enemy.on_page == page:
            if enemy.health > 0:
                enemy.visible = True
        else:
            enemy.visible = False

    for Item in foods:
        if Item.on_page == page:
            if not Item.collected:
                Item.visible = True
        else:
            Item.visible = False

    # =================================================================================================================
    # if the enemy is dead, do not show it
    # =================================================================================================================
    for enemy in enemys:
        if enemy.health <= 0:
            enemy.visible = False
            enemy.killCount = 1

    # =================================================================================================================
    # collisions
    # =================================================================================================================
    for food in foods:
        player_food_collision(food)

    for bird1 in enemys:
        player_enemy_collision(bird1)
        bullet_goblin_collision(bird1)

    # =================================================================================================================
    # anti bullet spam
    # =================================================================================================================
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 10:
        shootLoop = 0
    # =================================================================================================================
    # page switching
    # =================================================================================================================
    if man.x == screenWidth - 80:
        page += 1
        man.x = 20
    elif page > 0:
        if man.x <= 10:
            page -= 1
            man.x = screenWidth - 85

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # =================================================================================================================
    # key event move left and move right
    # =================================================================================================================
    if keys[pygame.K_LEFT or pygame.K_q] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT or pygame.K_d] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    # =================================================================================================================
    # key event jumping
    # =================================================================================================================
    if not man.isJump:
        if keys[pygame.K_UP or pygame.K_z]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    # =================================================================================================================
    # spawn goblin page 0
    # =================================================================================================================

    if keys[pygame.K_r] and not goblin1.visible:
        goblin1.visible = True
        goblin1.health = 10
    # =================================================================================================================
    # spawn goblins page 1
    # =================================================================================================================
    if keys[pygame.K_t] and not goblin2.visible and not goblin3.visible:
        goblin2.visible = True
        goblin2.health = 20
        goblin3.visible = True
        goblin3.health = 20

    # =================================================================================================================
    # sword attack and shoot attack
    # =================================================================================================================
    if keys[pygame.K_b] and sword.collected:
        for bird1 in enemys:
            sword_enemy_collision(bird1)
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1
pygame.quit()
