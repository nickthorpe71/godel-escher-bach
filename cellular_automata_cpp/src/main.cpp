#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <ctime>

const int WINDOW_SIZE = 1200;
const int GRID_SIZE = 300;
const int CELL_SIZE = WINDOW_SIZE / GRID_SIZE;
const int BUTTON_HEIGHT = 50;
const int BUTTON_WIDTH = 150;

struct Cell
{
    int x, y;
    bool alive;
    int liveNeighbors;
};

using Grid = std::vector<std::vector<Cell>>;

Grid createGrid(int size)
{
    Grid grid(size, std::vector<Cell>(size));
    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < size; ++j)
        {
            bool isAlive = static_cast<bool>(rand() % 2);
            grid[i][j] = {j, i, isAlive, 0};
        }
    }
    return grid;
}

void initializeNeighbors(Grid &grid)
{
    int size = grid.size();
    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < size; ++j)
        {
            for (int y = -1; y <= 1; ++y)
            {
                for (int x = -1; x <= 1; ++x)
                {
                    if (y == 0 && x == 0)
                        continue;
                    int ni = (i + y + size) % size;
                    int nj = (j + x + size) % size;
                    if (grid[ni][nj].alive)
                        grid[i][j].liveNeighbors++;
                }
            }
        }
    }
}

void updateGrid(Grid &grid)
{
    int size = grid.size();
    std::vector<std::pair<int, int>> toRevive, toKill;

    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < size; ++j)
        {
            int aliveNeighbors = grid[i][j].liveNeighbors;
            if (grid[i][j].alive)
            {
                if (aliveNeighbors < 2 || aliveNeighbors > 3)
                    toKill.push_back({i, j});
            }
            else
            {
                if (aliveNeighbors == 3)
                    toRevive.push_back({i, j});
            }
        }
    }

    for (const auto &[i, j] : toRevive)
    {
        grid[i][j].alive = true;
        for (int y = -1; y <= 1; ++y)
        {
            for (int x = -1; x <= 1; ++x)
            {
                if (y == 0 && x == 0)
                    continue;
                int ni = (i + y + size) % size;
                int nj = (j + x + size) % size;
                grid[ni][nj].liveNeighbors++;
            }
        }
    }

    for (const auto &[i, j] : toKill)
    {
        grid[i][j].alive = false;
        for (int y = -1; y <= 1; ++y)
        {
            for (int x = -1; x <= 1; ++x)
            {
                if (y == 0 && x == 0)
                    continue;
                int ni = (i + y + size) % size;
                int nj = (j + x + size) % size;
                grid[ni][nj].liveNeighbors--;
            }
        }
    }
}

void drawGrid(sf::RenderWindow &window, const Grid &grid, sf::Color cellColor = sf::Color::White, sf::Color backgroundColor = sf::Color::Black)
{
    sf::VertexArray quads(sf::Quads, grid.size() * grid.size() * 4);
    int index = 0;
    for (const auto &row : grid)
    {
        for (const auto &cell : row)
        {
            sf::Color color = cell.alive ? cellColor : backgroundColor;
            quads[index].position = sf::Vector2f(cell.x * CELL_SIZE, cell.y * CELL_SIZE);
            quads[index].color = color;
            quads[index + 1].position = sf::Vector2f((cell.x + 1) * CELL_SIZE, cell.y * CELL_SIZE);
            quads[index + 1].color = color;
            quads[index + 2].position = sf::Vector2f((cell.x + 1) * CELL_SIZE, (cell.y + 1) * CELL_SIZE);
            quads[index + 2].color = color;
            quads[index + 3].position = sf::Vector2f(cell.x * CELL_SIZE, (cell.y + 1) * CELL_SIZE);
            quads[index + 3].color = color;
            index += 4;
        }
    }
    window.draw(quads);
}

sf::Color getRandomColor(int brightness)
{
    return sf::Color(rand() % brightness, rand() % brightness, rand() % brightness);
}

bool isMouseOverButton(const sf::RectangleShape &button, const sf::Vector2i &mousePos)
{
    return button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePos));
}

int main()
{
    srand(static_cast<unsigned int>(time(0)));

    sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE, WINDOW_SIZE + 100), "Conway's Game of Life");
    Grid grid = createGrid(GRID_SIZE);
    initializeNeighbors(grid);

    sf::Color cellColor = getRandomColor(128);
    sf::Color backgroundColor = getRandomColor(64);

    sf::RectangleShape restartButton(sf::Vector2f(BUTTON_WIDTH, BUTTON_HEIGHT));
    restartButton.setPosition(50, WINDOW_SIZE + 25);
    restartButton.setFillColor(sf::Color::Green);

    sf::RectangleShape colorButton(sf::Vector2f(BUTTON_WIDTH, BUTTON_HEIGHT));
    colorButton.setPosition(250, WINDOW_SIZE + 25);
    colorButton.setFillColor(sf::Color::Blue);

    sf::Clock clock;
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }
            if (event.type == sf::Event::MouseButtonPressed)
            {
                if (event.mouseButton.button == sf::Mouse::Left)
                {
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);
                    if (isMouseOverButton(restartButton, mousePos))
                    {
                        grid = createGrid(GRID_SIZE);
                        initializeNeighbors(grid);
                    }
                    else if (isMouseOverButton(colorButton, mousePos))
                    {
                        cellColor = getRandomColor(128);
                        backgroundColor = getRandomColor(64);
                    }
                }
            }
        }

        if (clock.getElapsedTime().asMilliseconds() > 50)
        {
            updateGrid(grid);
            window.clear();
            drawGrid(window, grid, cellColor, backgroundColor);
            window.draw(restartButton);
            window.draw(colorButton);
            window.display();
            clock.restart();
        }
    }

    return 0;
}