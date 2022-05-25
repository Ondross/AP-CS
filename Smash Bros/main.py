import pygame
from pygame.locals import JOYBUTTONDOWN, JOYBUTTONUP, JOYAXISMOTION, JOYHATMOTION
from Player import Player
from Level import Level
import time

pygame.init()
pygame.joystick.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 48)
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(len(joysticks), " controllers detected.")

clock = pygame.time.Clock()


pixelSize = 20
screen = pygame.display.set_mode((50 * pixelSize, 40 * pixelSize))


ready = False
state = 0





level = Level(pixelSize)
level.addObstacle(10, 20, 30, 1, 1)
level.addObstacle(10, 15, 2, 10, 2)
level.addObstacle(23, 25, 10, 1)
level.addObstacle(5, 30, 15, 1, 1)
level.addObstacle(35, 30, 15, 1, 1)



players = []


lastUpdate = time.time()

while True:
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    if state == 0:
        text_surface = my_font.render('Welcome! press any button to continue', False, (255, 255, 255))
        screen.blit(text_surface, (80,400))
        for event in events:
            if event.type == pygame.KEYDOWN:
                state =1
                players = [Player(1, 20, 3, (255, 0, 255)), Player(2, 30, 3, (255, 255, 0)), Player(3, 40, 3, (0, 255, 0))]
                lastUpdate = time.time()
            if event.type == pygame.QUIT:
                exit()

    if state == 2:
        text_surface = my_font.render('winner: player ' + str(livingPlayers[0] + 1), False, (255, 255, 255))
        screen.blit(text_surface, (80,50))
        text_surface2 = my_font.render("press return to play again", False, (255, 255, 255))
        screen.blit(text_surface2, (80,100))
        killtext = my_font.render("kills", False, (255, 255, 255))
        screen.blit(killtext, (20,300))
        damagetext = my_font.render("damage", False, (255, 255, 255))
        screen.blit(damagetext, (20,400))

        for player in players:
            names = my_font.render("player " + str(player.num), False, (255, 255, 255))
            screen.blit(names, (200*player.num,200))
            killstext = my_font.render(str(player.kills), False, (255, 255, 255))
            screen.blit(killstext, (200*player.num,300))
            damagestext = my_font.render(str(player.damagedone), False, (255, 255, 255))
            screen.blit(damagestext, (200*player.num,400))


        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 1
            if event.type == pygame.QUIT:
                exit()
    if state == 1:
        
        keys = pygame.key.get_pressed()
        p = players[pygame.joystick.get_count()]

        if keys[pygame.K_LEFT]:
            p.setXVel(-1)
        elif keys[pygame.K_RIGHT]:
            p.setXVel(1)
        else:
            p.setXVel(0)

        for event in events:
            if event.type == JOYBUTTONDOWN:
                if event.button == 1:
                    players[event.joy].jump()
                if event.button == 2:
                    players[event.joy].attack(players)
                if event.button == 3:
                    players[event.joy].shoot()
                if event.button == 0:
                    players[event.joy].shield()
            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    players[event.joy].setXVel(event.value)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("CLICK!")
            if event.type == pygame.KEYDOWN:
                p = players[pygame.joystick.get_count()]
                if event.key == pygame.K_UP:
                    p.jump()
                if event.key == pygame.K_x:
                    p.shoot()
                if event.key == pygame.K_z:
                    p.attack(players)
                if event.key == pygame.K_c:
                    p.shield()
                            
                # if event.key == pygame.K_LEFT:
                #     p.goLeft()
                    
            #     if event.key == pygame.K_RIGHT:
            #        p.goRight()
                    
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         p.stop()
            if event.type == pygame.QUIT:
                exit()

        level.draw(screen)

        dt = time.time() - lastUpdate
        lastUpdate = time.time()
        for i in range(len(players)):
            p = players[i]
            p.update(level, players, dt)
            p.draw(screen, pixelSize, i)

        livingPlayers = []
        for i in range(len(players)):
            if players[i].health > 0:
                livingPlayers.append(i)
        if len(livingPlayers) == 1:
            state = 2
    

    pygame.display.update()
    clock.tick(30)


