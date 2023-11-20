from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

xRot = 0
yRot = 0
zRot = 0
dx = -0.5


def specialkeys(key, x, y):
    global xRot
    global yRot
    global zRot
    global dx

    if key == GLUT_KEY_LEFT:
        yRot -= 5
    if key == GLUT_KEY_RIGHT:
        yRot += 5
    if key == GLUT_KEY_UP:
        xRot += 5
    if key == GLUT_KEY_DOWN:
        xRot -= 5
    if key == GLUT_KEY_F1:
        zRot -= 90
    if key == GLUT_KEY_F2:
        zRot += 90
    if key == GLUT_KEY_F3:
        dx -= 0.1
    if key == GLUT_KEY_F4:
        dx += 0.1

    glutPostRedisplay()


def Axis():
    # Drawing coordinate axes
    glBegin(GL_LINES)
    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.3, 0.0, 0.0)
    glVertex3f(0.3, 0.0, 0.0)
    # Y axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, -0.3, 0.0)
    glVertex3f(0.0, 0.3, 0.0)
    # Z axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, -0.3)
    glVertex3f(0.0, 0.0, 0.3)
    glEnd()


def display():
    global xRot
    global yRot
    global zRot
    global dx
    glClear(GL_COLOR_BUFFER_BIT)

    # Drawing Sphere
    glPushMatrix()
    glTranslatef(-0.5, 0.5, 0)
    glRotatef(xRot, 1, 0, 0)
    glRotatef(yRot, 0, 1, 0)
    glColor3f(1.0, 1.0, 1.0)
    sphere = gluNewQuadric()
    gluQuadricDrawStyle(sphere, GLU_LINE)
    gluSphere(sphere, 0.2, 20, 40)
    Axis()
    glPopMatrix()

    # Drawing Tetrahedron
    glPushMatrix()
    glTranslatef(0.5, 0.5, 0)
    glRotatef(xRot, 1, 0, 0)
    glRotatef(yRot, 0, 1, 0)
    glRotatef(zRot, 0, 0, 1)
    glColor3f(1.0, 1.0, 1.0)
    glScale(0.3, 0.3, 0.3)
    glutWireTetrahedron()
    Axis()
    glPopMatrix()

    # Drawing Cone
    glPushMatrix()
    glTranslatef(dx, -0.5, 0)
    glRotatef(xRot, 1, 0, 0)
    glRotatef(yRot, 0, 1, 0)
    glColor3f(1.0, 1.0, 1.0)
    glutWireCone(0.1, 0.3, 20, 40)
    Axis()
    glPopMatrix()

    # Drawing Cube
    glPushMatrix()
    glTranslatef(0.5, -0.5, 0)
    glRotatef(xRot, 1, 0, 0)
    glRotatef(yRot, 0, 1, 0)
    glColor3f(1.0, 1.0, 1.0)
    glutWireCube(0.3)
    Axis()
    glPopMatrix()

    glutSwapBuffers()


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1200, 800)
    glutInitWindowPosition(100, 100)
    glutInit(sys.argv)

    glutCreateWindow("Graphics")
    glutDisplayFunc(display)
    glutSpecialFunc(specialkeys)

    glutMainLoop()
