import time
import pygame
import math
from Projectile import Projectile

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 48)

class Player:
    def __init__(self, num, x, y, color):
        self.num = num
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.facing = 1
        self.name = "Temporary"
        self.jumps = 0
        self.radius = 1
        self.health = 100
        self.left = False
        self.right = False
        self.jumps = 0
        self.health = 100
        self.color = color
        self.lastShot = 0
        self.projectiles = []
        self.fist = 0
        self.lastpunch = 0

    def update(self, level, players, dt):

        if self.y > 40:
            self.health = 0

        if self.health <= 0:
            return
        
        
            
            

        for projectile in self.projectiles:
            if projectile.alive == True:
                projectile.update(level,players,dt)

        self.vy += 12 * dt

        for obstacle in level.obstacles:
            if self.vy > 0.0 and obstacle.tileType > 0:
                yMatch = obstacle.y + .4 > (self.y + self.radius) > obstacle.y - .4
                xMatch = obstacle.x <= self.x <= obstacle.x + obstacle.width

                if yMatch and xMatch:
                    self.jumps = 2
                    self.vy = 0
                    self.y = obstacle.y - self.radius

        self.y += self.vy * dt
        self.x += self.vx * dt
        

    def checkCollisions(self, projectiles):
        otherProjectiles = list(set(projectiles) - set(self.projectiles)) + list(set(self.projectiles) - set(projectiles))
        for projectile in otherProjectiles:
                yMatch = projectile.y + .4 > (self.y + self.radius) > projectile.y - .4
                xMatch = projectile.x <= self.x <= projectile.x + 1
                if yMatch and xMatch:
                    print("hit")
                    self.health -= 10
                    projectile.alive = False
                    self.vx += .5 * projectile.direction * projectile.vx
            

    def goLeft(self, speed=1):
        
        self.vx = -8 * speed
        self.facing = -1
      
    def goRight(self, speed = 1):
        self.vx = 8 * speed
        self.facing = 1

    def getRect(self):
        return pygame.Rect(self.x,self.y, 2, 2)
    
    def move(self, dir):
        if (dir < 0 ):
            self.goLeft(abs(dir))
        elif (dir > 0):
            self.goRight(dir)
        else:
            self.stop()
    
    def stop(self):
        self.vx *= 0.8

    def jump(self):
        if self.jumps > 0:
            self.vy = -8
            self.jumps -=1

    def shoot(self):
        now = time.time()
        if now - self.lastShot > .8:
            self.lastShot = now
            self.projectiles.append(Projectile(self.num, self.facing, self.x, self.y, 5 + abs(self.vx)))
            if len(self.projectiles) > 10:
                self.projectiles.pop(0)

    def attack(self, players):
        now1 = time.time()

        if (now1 - self.lastpunch > 1):
            self.lastpunch = time.time()
            for player in players:
                if (player != self):
                    #you should only be able to attack when you're facing a player
                    if abs(player.x - self.x) < 3 and abs(player.y - self.y) < 3:
                        self.fist = 1
                        player.health -= 10

    def hit(self, damage):
        self.health -= damage

    def draw(self, screen, pixelSize, playerIndex):
        if self.health<=0:
            pygame.draw.circle(screen, (0,0,0),(self.x * pixelSize,self.y * pixelSize), self.radius * pixelSize)
        else:
            pygame.draw.circle(screen, self.color,(self.x * pixelSize,self.y * pixelSize), self.radius * pixelSize)
            if self.fist > 0 :
                pygame.draw.circle(screen, self.color,((self.x + self.fist*3/4*self.radius*self.facing) * pixelSize,(self.y - self.radius/2) * pixelSize), self.radius/4 * pixelSize)
                self.fist += 1
                self.fist %= 3

        for projectile in self.projectiles:
            if projectile.alive == True:
                projectile.draw(screen)
        if self.health > 0:
            text = str(self.health)
        else:
            text = "DEAD"
        text_surface = my_font.render(text, False, self.color)
        screen.blit(text_surface, (playerIndex * 100,0))