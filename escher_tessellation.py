import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def draw_hexagon(ax, center, size):
    """Draws a hexagon at a given center with a specified size."""
    angles = np.linspace(0, 2 * np.pi, 7)
    x_hex = center[0] + size * np.cos(angles)
    y_hex = center[1] + size * np.sin(angles)
    hexagon = ax.fill(x_hex, y_hex, edgecolor='black', fill=False)
    return hexagon

def draw_triangle(ax, center, size, orientation):
    """Draws a triangle at a given center with a specified size and orientation."""
    angles = np.array([0, 2 * np.pi / 3, 4 * np.pi / 3, 0]) + orientation
    x_tri = center[0] + size * np.cos(angles)
    y_tri = center[1] + size * np.sin(angles)
    triangle = ax.fill(x_tri, y_tri, edgecolor='black', fill=False)
    return triangle

def draw_tessellation(ax, rows, cols, size, current_frame):
    """Draws a tessellation pattern using hexagons and triangles."""
    ax.clear()
    ax.set_aspect('equal')
    h = size * np.sqrt(3)
    count = 0

    for row in range(rows):
        for col in range(cols):
            if count > current_frame:
                return
            x_offset = col * 1.5 * size
            y_offset = row * h + (col % 2) * (h / 2)
            
            # Draw hexagon
            draw_hexagon(ax, (x_offset, y_offset), size)
            
            # Draw surrounding triangles
            for i in range(6):
                if count > current_frame:
                    return
                angle = i * np.pi / 3
                tri_center = (x_offset + size * np.cos(angle), y_offset + size * np.sin(angle))
                draw_triangle(ax, tri_center, size / 2, angle + np.pi / 6)
                count += 1
    
    ax.set_xlim(-size, cols * 1.5 * size)
    ax.set_ylim(-size, rows * h)
    ax.axis('off')

def update(frame):
    draw_tessellation(ax, rows, cols, size, frame)

# Parameters for the tessellation
rows = 10
cols = 10
size = 30

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, frames=range(rows * cols * 7), repeat=False)

plt.show()