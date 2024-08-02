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

def build_grid(size: int) -> np.ndarray:
    initial_grid = np.random.choice([0, 1], size=(size, size))
    grid = np.empty((size, size), dtype=object)

    for i in range(size):
        for j in range(size):
            pos = Vec2(j, i)
            grid[i, j] = Cell(pos, initial_grid[i, j])

    for i in range(size):
        for j in range(size):
            grid[i, j].neighbors = get_neighbors(grid, Vec2(j, i), size)
    
    return grid

def update(frameNum: int, img, grid: np.ndarray, size: int, rule: Callable[[Cell], int], counter: List[int], max_iterations: int):
    new_grid = np.empty_like(grid)
    for i in range(size):
        for j in range(size):
            current = grid[i, j]
            new_val = rule(current)
            new_grid[i, j] = Cell(current.pos, new_val)

    for i in range(size):
        for j in range(size):
            new_grid[i, j].neighbors = get_neighbors(new_grid, Vec2(j, i), size)
    
    img.set_data([[cell.val for cell in row] for row in new_grid])
    grid[:, :] = new_grid[:, :]

    counter[0] += 1
    if counter[0] >= max_iterations:
        counter[0] = 0
        new_grid = build_grid(size)
        img.set_data([[cell.val for cell in row] for row in new_grid])
        grid[:, :] = new_grid[:, :]
    
    return img

def run(grid_size: int, frames: int, interval: int, rule: Callable[[Cell], int], max_iterations: int):
    grid = build_grid(grid_size)

    fig, ax = plt.subplots()
    img = ax.imshow([[cell.val for cell in row] for row in grid], interpolation='nearest', cmap='gray')
    counter = [0]  # Using a list to allow modification inside the update function
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, grid_size, rule, counter, max_iterations), frames=frames, interval=interval, repeat=True)

    plt.show()

# Rule Functions
def conway_rule(cell: Cell) -> int:
    """
    Conway's Game of Life rule:
    - Any live cell with fewer than two live neighbors dies (underpopulation).
    - Any live cell with two or three live neighbors lives on to the next generation.
    - Any live cell with more than three live neighbors dies (overpopulation).
    - Any dead cell with exactly three live neighbors becomes a live cell (reproduction).
    """
    total = cell.sum_neighbors()
    if cell.val == 1:
        if total < 2 or total > 3:
            return 0
        else:
            return 1
    else:
        if total == 3:
            return 1
        else:
            return 0

def highlife_rule(cell: Cell) -> int:
    """
    HighLife rule:
    - Similar to Conway's Game of Life with an additional reproduction condition.
    - Any live cell with fewer than two live neighbors dies (underpopulation).
    - Any live cell with two or three live neighbors lives on to the next generation.
    - Any live cell with more than three live neighbors dies (overpopulation).
    - Any dead cell with exactly three or six live neighbors becomes a live cell (reproduction).
    """
    total = cell.sum_neighbors()
    if cell.val == 1:
        if total < 2 or total > 3:
            return 0
        else:
            return 1
    else:
        if total == 3 or total == 6:
            return 1
        else:
            return 0

def replicator_rule(cell: Cell) -> int:
    """
    Replicator rule:
    - Any cell, whether live or dead, becomes a live cell if it has an odd number of live neighbors.
    - Any cell becomes a dead cell if it has an even number of live neighbors.
    """
    total = cell.sum_neighbors()
    return 1 if total % 2 == 1 else 0

def seeds_rule(cell: Cell) -> int:
    """
    Seeds rule:
    - Any live cell dies (no survival).
    - Any dead cell with exactly two live neighbors becomes a live cell (reproduction).
    """
    total = cell.sum_neighbors()
    if cell.val == 0 and total == 2:
        return 1
    else:
        return 0

def life_without_death_rule(cell: Cell) -> int:
    """
    Life without Death rule:
    - Any live cell stays alive.
    - Any dead cell with exactly three live neighbors becomes a live cell (reproduction).
    """
    total = cell.sum_neighbors()
    if cell.val == 1 or total == 3:
        return 1
    else:
        return 0

if __name__ == "__main__":
    # Test with different rules
    run(grid_size=100, frames=60, interval=50, rule=conway_rule, max_iterations=300)  # Replace with other rule functions to test