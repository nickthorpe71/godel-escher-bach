import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List, Callable

class Vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, pos: Vec2, val: int, neighbors: List['Cell'] = None):
        self.pos = pos
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def sum_neighbors(self) -> int:
        return np.sum([n.val for n in self.neighbors])

def get_neighbors(grid: np.ndarray, pos: Vec2, size: int) -> List[Cell]:
    x, y = pos.x, pos.y
    neighbors = [
        grid[y, (x-1) % size], grid[y, (x+1) % size],
        grid[(y-1) % size, x], grid[(y+1) % size, x],
        grid[(y-1) % size, (x-1) % size], grid[(y-1) % size, (x+1) % size],
        grid[(y+1) % size, (x-1) % size], grid[(y+1) % size, (x+1) % size]
    ]
    return neighbors

def build_grid(size: int, platform_density: float) -> np.ndarray:
    initial_grid = np.random.choice([0, 1], size=(size, size))
    platform_grid = np.random.choice([0, 1], size=(size, size), p=[1-platform_density, platform_density])
    grid = np.empty((size, size), dtype=object)

    for i in range(size):
        for j in range(size):
            pos = Vec2(j, i)
            if platform_grid[i, j] == 1:
                grid[i, j] = Cell(pos, 2)  # 2 represents a static platform
            else:
                grid[i, j] = Cell(pos, initial_grid[i, j])

    for i in range(size):
        for j in range(size):
            grid[i, j].neighbors = get_neighbors(grid, Vec2(j, i), size)
    
    return grid

def apply_gravity_and_jump(cell: Cell, grid: np.ndarray, size: int) -> int:
    """
    Apply gravity and jumping mechanics to the cell.
    - A cell will fall if there's no platform or another cell beneath it.
    - A cell can jump to a higher position.
    """
    x, y = cell.pos.x, cell.pos.y
    below = grid[(y + 1) % size, x]

    if cell.val == 1:
        # Apply gravity
        if below.val == 0:
            return 0  # Cell falls
        elif below.val == 1:
            return 1  # Cell is supported by another cell
        elif below.val == 2:
            # Cell is on a platform and can jump
            if y > 0 and grid[(y - 1) % size, x].val == 0:
                return 1
    return cell.val

def update(frameNum: int, img, grid: np.ndarray, size: int, rule: Callable[[Cell, np.ndarray, int], int]):
    new_grid = np.empty_like(grid)
    for i in range(size):
        for j in range(size):
            current = grid[i, j]
            if current.val != 2:  # Skip static platforms
                new_val = rule(current, grid, size)
                new_grid[i, j] = Cell(current.pos, new_val)
            else:
                new_grid[i, j] = Cell(current.pos, 2)  # Keep static platforms
    
    for i in range(size):
        for j in range(size):
            new_grid[i, j].neighbors = get_neighbors(new_grid, Vec2(j, i), size)
    
    img.set_data([[cell.val for cell in row] for row in new_grid])
    grid[:, :] = new_grid[:, :]
    return img

def run(grid_size: int, frames: int, interval: int, rule: Callable[[Cell, np.ndarray, int], int], platform_density: float):
    grid = build_grid(grid_size, platform_density)

    fig, ax = plt.subplots()
    img = ax.imshow([[cell.val for cell in row] for row in grid], interpolation='nearest', cmap='gray')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, grid_size, rule), frames=frames, interval=interval, save_count=50)

    plt.show()

# Define the main function to test gravity and jumping
def gravity_and_jump_rule(cell: Cell, grid: np.ndarray, size: int) -> int:
    """
    Apply a combination of gravity and jumping rules to the cell.
    """
    return apply_gravity_and_jump(cell, grid, size)

if __name__ == "__main__":
    # Test with gravity and jumping rules
    run(grid_size=50, frames=30, interval=1000, rule=gravity_and_jump_rule, platform_density=0.3)  # 30% platform density