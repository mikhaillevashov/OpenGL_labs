from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

xRot = 0
yRot = 0
zRot = 1
red = 1
green = 0


def specialkeys(key, x, y):
    global xRot
    global yRot
    global zRot
    global red
    global green

    if key == GLUT_KEY_UP and xRot < 1:
        xRot += 1.0
    if key == GLUT_KEY_DOWN and xRot > -1:
        xRot -= 1
    if key == GLUT_KEY_LEFT and yRot > -1:
        yRot -= 1
    if key == GLUT_KEY_RIGHT and yRot < 1:
        yRot += 1
    if key == GLUT_KEY_F1 and zRot < 1:
        zRot += 1
    if key == GLUT_KEY_F2 and zRot > -1:
        zRot -= 1
    if key == GLUT_KEY_F3:
        red = 1
        green = 0
    if key == GLUT_KEY_F4:
        red -= 0.2
    if key == GLUT_KEY_F5:
        red = 0
        green = 1
    if key == GLUT_KEY_F6:
        green -= 0.2

    glutPostRedisplay()


def display():
    global xRot
    global yRot
    global zRot
    global red
    global green

    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [yRot, xRot, zRot, 0.0])
    light_diffuse = [red, green, 0.0, 0.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_diffuse)

    # Drawing Cube
    glDisable(GL_CULL_FACE)
    glPushMatrix()
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 0.4])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 0.4))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0, 0, 0, 0.4))
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)

    glRotatef(45, 1.0, 1.0, 1.0)
    glTranslatef(-0.4, 0.8, 0)
    glColor4f(1.0, 1.0, 1.0, 0.4)
    glutSolidCube(0.3)
    glPopMatrix()

    # Drawing shininess Sphere
    glEnable(GL_CULL_FACE)
    glPushMatrix()
    sphere = gluNewQuadric()
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 128)

    glTranslatef(0.5, 0.5, 0)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    gluSphere(sphere, 0.3, 100, 100)
    glPopMatrix()

    # Drawing textured Sphere
    glPushMatrix()
    texture = load_texture('MicrosoftTeams-image.jpg')
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)

    glRotatef(45, 1.0, 1.0, 0.0)
    glTranslatef(-0.5, -0.5, 0)
    glColor3f(1.0, 1.0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    sphere2 = gluNewQuadric()
    gluQuadricTexture(sphere2, texture)
    gluQuadricOrientation(sphere2, GLU_OUTSIDE)
    gluSphere(sphere2, 0.3, 100, 100)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glutSwapBuffers()


def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    width, height = image.size
    image_data = image.convert("RGBA").tobytes()

    # Creating OpenGL texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    return texture_id


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1200, 800)
    glutInitWindowPosition(100, 100)
    glutInit(sys.argv)

    glutCreateWindow("Graphics")
    glutDisplayFunc(display)
    glutSpecialFunc(specialkeys)
    glutMainLoop()
