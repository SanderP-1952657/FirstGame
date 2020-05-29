import pygame

pygame.init()
screenWidt = 1200
screenHeigt = 480
bulletRange = 200
# =========================================================================================================================================
# setup pictures and music
# =========================================================================================================================================
win = pygame.display.set_mode((screenWidt, screenHeigt))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

bg_start = pygame.image.load('bg3.png')
bg_1 = pygame.image.load('bg2.png')
apple = pygame.image.load('apple.png')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('throw.wav')
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0
page = 0


# =========================================================================================================================================
# player
# =========================================================================================================================================
class player(object):
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

    def draw(self, win):
        if self.visible == True:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not (self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            pygame.draw.rect(win, (128, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health / 2)), 10))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenWidt - 650 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    # =========================================================================================================================================
    # bullet
    # =========================================================================================================================================


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        bulletSound.play
    # =========================================================================================================================================
    # goblin
    # =========================================================================================================================================


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = health
        self.visible = True
        self.killCount = 0

    def draw(self, win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            if self.health == 10:
                pygame.draw.rect(win, (128, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0, 128, 0),
                                 (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            else:
                pygame.draw.rect(win, (128, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0, 128, 0),
                                 (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health / 2)), 10))

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
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        hitSound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            self.killCount += 1
        print('hit')


class food(object):
    def __init__(self, x, y, width, height, healthpoints):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.healthpoints = healthpoints
        self.visible = True
        self.hitbox = (self.x + 50, self.y + 50, 31, 57)

    def draw(self, win):
        if self.visible:
            win.blit(apple, (300, 300))

    # =========================================================================================================================================
    # draw function
    # =========================================================================================================================================


def redrawGameWindow():
    if page == 0:
        win.blit(bg_start, (0, 0))
    else:
        win.blit(bg_1, (0, 0))
    man.draw(win)
    goblin.draw(win)
    goblin2.draw(win)
    goblin3.draw(win)
    text = font.render('score: ' + str(score), 1, (0, 0, 0))
    if food.visible:
        food.draw(win)
    win.blit(text, (screenWidt - 160, 10))
    if man.visible:
        for bullet in bullets:
            bullet.draw(win)
    text1 = font.render('kills: ' + str(goblin.killCount + goblin2.killCount + goblin3.killCount), 1, (0, 0, 0))
    win.blit(text1, (screenWidt - 260, 10))
    if man.health <= 0:
        deadText = font.render('you are dead', 1, (0, 0, 0))
        win.blit(deadText, (screenWidt / 2 - 100, 200))
        man.visible = False
    pygame.display.update()

    # =========================================================================================================================================
    # setup for main loop
    # =========================================================================================================================================


# mainloop
font = pygame.font.SysFont('comicsans', 30, True, True)
man = player(200, 410, 64, 64)
goblin = enemy(800, 410, 64, 64, screenWidt - 50, 10)
goblin2 = enemy(800, 410, 64, 64, screenWidt - 50, 20)
goblin3 = enemy(200, 410, 64, 64, screenWidt - 600, 20)
food = food(600, 300, 50, 50, 10)
bullets = []
shootLoop = 0
run = True

while run:
    clock.tick(27)
    if food.visible == True:
        if man.hitbox[1] < food.hitbox[1] + food.hitbox[3] and man.hitbox[1] + man.hitbox[3] > food.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > food.hitbox[0] - food.hitbox[2] and man.hitbox[0] < food.hitbox[0] + \
                    food.hitbox[2]:
                if man.health <= 10:
                    man.health += 10
                else:
                    man.health = 20
                food.visible = False

    redrawGameWindow()
    # =========================================================================================================================================
    # what goblin is visible on each page
    # =========================================================================================================================================
    if page == 0:
        goblin2.visible = False
        goblin3.visible = False
        if goblin.health > 0:
            goblin.visible = True
    else:
        if goblin2.health > 0:
            goblin2.visible = True
        if goblin3.health > 0:
            goblin3.visible = True
        goblin.visible = False

    # =========================================================================================================================================
    # collision between goblin and man
    # =========================================================================================================================================

    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] - goblin.hitbox[2] and man.hitbox[0] < goblin.hitbox[
                0] + goblin.hitbox[2]:
                man.hit()
                man.health -= 5

    if goblin2.visible:
        if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] - goblin2.hitbox[2] and man.hitbox[0] < goblin2.hitbox[
                0] + goblin2.hitbox[2]:
                man.hit()
                man.health -= 5

    if goblin3.visible:
        if man.hitbox[1] < goblin3.hitbox[1] + goblin3.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin3.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin3.hitbox[0] - goblin3.hitbox[2] and man.hitbox[0] < goblin3.hitbox[
                0] + goblin3.hitbox[2]:
                man.hit()
                man.health -= 5
    # =========================================================================================================================================
    # anti bullet spam
    # =========================================================================================================================================
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # =========================================================================================================================================
    # beperk range van bullet
    # =========================================================================================================================================
    for bullet in bullets:
        if bullet.facing == 1:
            if bullet.x > man.x + man.width / 2 + bulletRange:
                bullets.pop(bullets.index(bullet))
        else:
            if bullet.x < man.x + man.width / 2 - bulletRange:
                bullets.pop(bullets.index(bullet))
    # =========================================================================================================================================
    # collision between bullit and goblin
    # =========================================================================================================================================
    if man.visible:
        for bullet in bullets:
            if goblin.visible:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                        goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] - goblin.hitbox[2] and bullet.x - bullet.radius < \
                            goblin.hitbox[0] + goblin.hitbox[2]:
                        goblin.hit()
                        hitSound.play()
                        if goblin.visible:
                            score += 1
                            bullets.pop(bullets.index(bullet))

            if bullet.x < screenWidt and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
    if man.visible:
        for bullet in bullets:
            if goblin2.visible:
                if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > \
                        goblin2.hitbox[1]:
                    if bullet.x + bullet.radius > goblin2.hitbox[0] - goblin2.hitbox[2] and bullet.x - bullet.radius < \
                            goblin2.hitbox[0] + goblin2.hitbox[2]:
                        goblin2.hit()
                        hitSound.play()
                        if goblin2.visible:
                            score += 1
                            bullets.pop(bullets.index(bullet))

            if bullet.x < screenWidt and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    if man.visible:
        for bullet in bullets:
            if goblin3.visible:
                if bullet.y - bullet.radius < goblin3.hitbox[1] + goblin3.hitbox[3] and bullet.y + bullet.radius > \
                        goblin3.hitbox[1]:
                    if bullet.x + bullet.radius > goblin3.hitbox[0] - goblin3.hitbox[2] and bullet.x - bullet.radius < \
                            goblin3.hitbox[0] + goblin3.hitbox[2]:
                        goblin3.hit()
                        hitSound.play()
                        if goblin3.visible:
                            score += 1
                            bullets.pop(bullets.index(bullet))

            if bullet.x < screenWidt and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    # =========================================================================================================================================
    # key event shoot
    # =========================================================================================================================================
    keys = pygame.key.get_pressed()
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
    # =========================================================================================================================================
    # key event left
    # =========================================================================================================================================
    if keys[pygame.K_LEFT or pygame.K_q] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    # =========================================================================================================================================
    # key event right
    # =========================================================================================================================================
    elif keys[pygame.K_RIGHT or pygame.K_d] and man.x < screenWidt - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    # =========================================================================================================================================
    # page switching
    # =========================================================================================================================================
    if man.x == screenWidt - 80:
        page += 1
        man.x = 20
    elif man.x <= 10:
        page = 0
        man.x = screenWidt - 85
    # =========================================================================================================================================
    # key event jumping
    # =========================================================================================================================================
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
    # =========================================================================================================================================
    # respawn goblin page 0
    # =========================================================================================================================================
    if keys[pygame.K_r] and goblin.visible == False:
        goblin.visible = True
        goblin.health = 10
    # =========================================================================================================================================
    # respawn goblins page 1
    # =========================================================================================================================================
    if keys[pygame.K_t] and goblin2.visible == False and goblin3.visible == False:
        goblin2.visible = True
        goblin2.health = 20
        goblin3.visible = True
        goblin3.health = 20

pygame.quit()
