import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

ground_verticies = ((4, -10, 4), (-4, -10, 4),
                    (-4, -10, 0), (4, -10, 0))


class Particle:
    def __init__(self):
        radius = 3
        a = random.uniform(0, math.pi)
        rand = random.randint(0, 1)
        if rand == 0:
            self.x = radius * math.cos(a)
            self.y = radius * math.sin(a)
        else:
            self.x = -radius * math.cos(a)
            self.y = -radius * math.sin(a)
        self.position = [self.x, self.y, random.uniform(-2, 5)]
        self.velocity = [-self.x, -self.y, 0]
        self.coef = 0.6
        self.counter = 0
        self.is_handle = False

        self.track_size = random.randint(10, 40)
        self.track = [self.position, [self.position[0], self.position[1], self.position[2]]]

        self.lifetime = random.randint(4, 9)

    def handle_collision(self):
        if 0 <= self.position[0] <= 4.5 and self.position[1] < -8 and -0.5 <= self.position[2] <= 2:
            self.velocity[0] = -5
            self.velocity[1] = 2
            self.velocity[2] = 2
            self.track[1] = [self.position[0], self.position[1], self.position[2]]
            self.track_size = random.randint(10, 40)
            self.is_handle = True
        elif -4.5 <= self.position[0] <= 0 and self.position[1] < -8 and -0.5 <= self.position[2] <= 2:
            self.velocity[0] = 5
            self.velocity[1] = 2
            self.velocity[2] = 2
            self.track[1] = [self.position[0], self.position[1], self.position[2]]
            self.track_size = random.randint(10, 40)
            self.is_handle = True
        elif 0 <= self.position[0] <= 4.5 and self.position[1] < -8 and 2 <= self.position[2] <= 4.5:
            self.velocity[0] = -5
            self.velocity[1] = 2
            self.velocity[2] = -2
            self.track[1] = [self.position[0], self.position[1], self.position[2]]
            self.track_size = random.randint(10, 40)
            self.is_handle = True
        elif -4.5 <= self.position[0] <= 0 and self.position[1] < -8 and 2 <= self.position[2] <= 4.5:
            self.velocity[0] = 5
            self.velocity[1] = 2
            self.velocity[2] = -2
            self.track[1] = [self.position[0], self.position[1], self.position[2]]
            self.track_size = random.randint(10, 30)
            self.is_handle = True
        else:
            self.velocity = [-self.x, -self.y, 0]

    def update(self, dtime):
        self.counter += dtime
        self.position[0] -= self.velocity[0] * dtime * self.coef
        self.position[1] -= self.velocity[1] * dtime * self.coef
        self.position[2] -= self.velocity[2] * dtime * self.coef
        self.lifetime -= dtime

        if self.track_size != 0:
            self.track_size -= 1
        else:
            self.track[1][0] -= self.velocity[0] * dtime * self.coef
            self.track[1][1] -= self.velocity[1] * dtime * self.coef
            self.track[1][2] -= self.velocity[2] * dtime * self.coef

    def draw(self):
        color = 0.2
        if self.counter > 2:
            self.coef = 0.7
            color = 0.3
        if self.counter > 3:
            self.coef = 0.8
            color = 0.4
        if self.counter > 4:
            self.coef = 0.9
            color = 0.5
        if self.counter > 5:
            self.coef = 1
            color = 0.7
        if self.counter > 6:
            self.coef = 1.2
            color = 0.9
        glLineWidth(3)
        glBegin(GL_LINES)
        if self.is_handle:
            glColor4f(0, 1, 0, 0.1)
        else:
            glColor4f(color, color, color, 0.1)
        glVertex3f(self.track[0][0], self.track[0][1], self.track[0][2])
        glVertex3f(self.track[1][0], self.track[1][1], self.track[1][2])
        glEnd()

        if self.is_handle:
            glColor3f(0, 1, 0)
        else:
            glColor3f(color, color, color)
        glPointSize(3)
        glBegin(GL_POINTS)
        x, y, z = self.position
        glVertex3f(x, y, z)
        glEnd()


def create_particles(num_particles):
    particles = []
    for _ in range(num_particles):
        particle = Particle()
        particles.append(particle)
    return particles


def square():
    glPushMatrix()
    glTranslate(0, 0, 0)
    glBegin(GL_QUADS)
    for vertex in ground_verticies:
        glVertex3fv(vertex)
    glEnd()
    glPopMatrix()


if __name__ == '__main__':
    pygame.init()
    glutInit()
    display = (1200, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(50, 0, 0, 0, 0, 0, 0, 0, 1)

    last_time = pygame.time.get_ticks()
    particles = create_particles(1000)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glRotatef(10, 0, 1, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(10, 0, 0, 1)
                if event.key == pygame.K_RIGHT:
                    glRotatef(-10, 0, 0, 1)
        current_time = pygame.time.get_ticks()
        dtime = (current_time - last_time) / 1000.0
        last_time = current_time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        for particle in particles:
            particle.update(dtime)
            particle.handle_collision()
            if particle.lifetime <= 0:
                particles.remove(particle)
                new_particle = Particle()
                particles.append(new_particle)

        glPushMatrix()

        glColor3f(0.6, 0, 0.2)
        glTranslatef(0, 0, -2)

        slices = 30
        stacks = 30
        radius = 3
        height = 7
        quadric = gluNewQuadric()
        gluCylinder(quadric, radius, radius, height, slices, stacks)

        glPopMatrix()

        square()
        for particle in particles:
            if particle.lifetime > 0:
                particle.draw()

        pygame.display.flip()
        pygame.time.wait(10)
