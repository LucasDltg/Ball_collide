import random

import numpy
import pygame
import sys
from ball import *
from quadtree import *

black = (0, 0, 0)
red = (255, 0, 0)
size = width, height = 600, 600

balls = []

pygame.init()

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

quadTreeEnabled = True
main_clock = pygame.time.Clock()
while True:
    main_clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            size = width, height
        if event.type == pygame.KEYDOWN:
            # Exit
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            # Clear the screen
            if event.key == pygame.K_c:
                balls = []
            # Toggle QuadTree
            if event.key == pygame.K_t:
                quadTreeEnabled = not quadTreeEnabled
            # Add ball
            if event.key == pygame.K_SPACE:
                max_mass, min_size, max_size, min_speed, max_speed = 100, 15, 60, 1, 10

                mass = random.randint(1, max_mass)
                size = int(min_size + (max_size-min_size)/max_mass*(mass-1))
                speed = int(max_speed + (min_speed-max_speed)/max_mass*(mass-1))
                balls.append(Ball(random.randint(0, width-size), random.randint(0, height-size),
                                  random.randint(-1, 1)*speed, random.randint(-1, 1)*speed,
                                  size, (0, 255, 0), mass))
            # Add balls fill the screen
            if event.key == pygame.K_m:
                nb = 20
                bsize = min(width, height)/nb
                for i in range(0, int(width/bsize)):
                    for j in range(0, int(height/bsize)):
                        balls.append(Ball(i*bsize, j*bsize, random.randint(-5,5), random.randint(-5,5), bsize))

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
