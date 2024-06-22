import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

def init():
    gl.glClearClolor(1.0, 1.0, 1.0, 1.0) # Set background to white
    gl.glColor3f(0.0, 0.0, 0.0)          # Set drawing color to black
    gl.glPointSize(4.0)                  # Set point size to 4 pixels
    glu.gluOrtho2D(0, 500, 0, 500)       # Set the orthographic viewing region

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)   # Clear the display
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2i(100, 100)              # Define the line segment
    gl.glVertex2i(400, 400)
    gl.glEnd()
    gl.glFlush()

def main():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_SINGLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(100, 100)
    glut.glutCreateWindow("OpenGL test")
    init()
    glut.glutDisplayFunc(display)
    glut.glutMainLoop()

if __name__ == "__main__":
    main()
    
