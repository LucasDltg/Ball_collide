import random

import numpy
import pygame
import sys
from ball import *
from quadtree import *

black = (0, 0, 0)
red = (255, 0, 0)

balls = []

pygame.init()
screen_info = pygame.display.Info()
size = width, height = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode(size, pygame.SCALED)


quadTreeEnabled = True
main_clock = pygame.time.Clock()
while True:
    main_clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_c:
                balls = []
            if event.key == pygame.K_t:
                quadTreeEnabled = not quadTreeEnabled
            if event.key == pygame.K_SPACE:
                #mass = random.randint(1, 10)
                #size = mass*10
                #max_speed = 10/mass
                bsize = 50
                #balls.append(Ball(random.randint(0, width-bsize), random.randint(0, height-bsize), random.randint(1, 10), random.randint(1,3), bsize, color=(0, 255, 0)))
                balls.append(Ball(200, 200, 0, 0, 50, mass=50))
                balls.append(Ball(0, 200, 10, 0, 50/2, mass=20))

            if event.key == pygame.K_m:
                bsize = 50
                for i in range(0, int(size[0]/50)):
                    for j in range(0, int(size[1] / 50)):
                        balls.append(Ball(i*50, j*50,
                                               random.randint(1, 10), random.randint(1, 3), bsize))

    if quadTreeEnabled:
        quadtree = QuadTree(Rectangle(0, 0, width, height))
        for ball in balls:
            quadtree.insert(ball)

    for i in range(0, len(balls)):
        if balls[i].x_pos + balls[i].size + balls[i].x_speed > width:
            balls[i].x_pos = width - (balls[i].size + balls[i].x_speed)
            balls[i].x_speed *= -1
        elif balls[i].x_pos + balls[i].x_speed < 0:
            balls[i].x_pos = balls[i].x_speed
            balls[i].x_speed *= -1

        if balls[i].y_pos + balls[i].size + balls[i].y_speed > height:
            balls[i].y_pos = height - (balls[i].size + balls[i].y_speed)
            balls[i].y_speed *= -1
        elif balls[i].y_pos + balls[i].y_speed < 0:
            balls[i].y_pos = balls[i].y_speed
            balls[i].y_speed *= -1

        if quadTreeEnabled:
            range_boundary = Rectangle(balls[i].x_pos - balls[i].size, balls[i].y_pos - balls[i].size, 2 * balls[i].size, 2 * balls[i].size)
            found_balls = []
            quadtree.query(range_boundary, found_balls)

            for other_ball in found_balls:
                if balls[i] != other_ball and balls[i].isColliding(other_ball):
                    balls[i].resolveCollision(other_ball)
        else:
            for j in range(i+1, len(balls)):
                if balls[i].isColliding(balls[j]):
                    balls[i].resolveCollision(balls[j])

        balls[i].x_pos += balls[i].x_speed
        balls[i].y_pos += balls[i].y_speed


    screen.fill(black)
    for b in balls:
        pygame.draw.circle(screen, b.color, (b.x_pos + b.size/2, b.y_pos + b.size/2), b.size/2)

    font = pygame.font.SysFont("arial", 40)
    fps = font.render(str(int(main_clock.get_fps())), True, (0, 255, 0), (0, 0, 0))
    screen.blit(fps, (5, 5))
    pygame.display.flip()
