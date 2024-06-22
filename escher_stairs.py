#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <set>
#include <ctime>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"

struct Color {
    float r, g, b;
};

struct Vertex {
    float x, y, z;
};

struct Cube {
    Vertex position;
    float size;
    Color colors[6];  // Different colors for each face
    float perspectiveFactor;
};

std::vector<Cube> cubes;
std::set<std::tuple<int, int, int>> occupiedPositions;

void drawCube(const Cube& cube) {
    float halfSize = cube.size / 2.0f;

    std::vector<Vertex> vertices = {
        {cube.position.x - halfSize, cube.position.y - halfSize, cube.position.z - halfSize},
        {cube.position.x + halfSize, cube.position.y - halfSize, cube.position.z - halfSize},
        {cube.position.x + halfSize, cube.position.y + halfSize, cube.position.z - halfSize},
        {cube.position.x - halfSize, cube.position.y + halfSize, cube.position.z - halfSize},
        {cube.position.x - halfSize, cube.position.y - halfSize, cube.position.z + halfSize},
        {cube.position.x + halfSize, cube.position.y - halfSize, cube.position.z + halfSize},
        {cube.position.x + halfSize, cube.position.y + halfSize, cube.position.z + halfSize},
        {cube.position.x - halfSize, cube.position.y + halfSize, cube.position.z + halfSize}
    };

    std::vector<unsigned int> indices = {
        0, 1, 2, 3, // bottom
        4, 5, 6, 7, // top
        0, 1, 5, 4, // front
        2, 3, 7, 6, // back
        0, 3, 7, 4, // left
        1, 2, 6, 5  // right
    };

    // Different colors for each face
    for (int i = 0; i < 6; ++i) {
        glColor3f(cube.colors[i].r * cube.perspectiveFactor, cube.colors[i].g * cube.perspectiveFactor, cube.colors[i].b * cube.perspectiveFactor);
        glBegin(GL_QUADS);
        for (int j = 0; j < 4; ++j) {
            Vertex v = vertices[indices[i * 4 + j]];
            glVertex3f(v.x * cube.perspectiveFactor, v.y * cube.perspectiveFactor, v.z * cube.perspectiveFactor);
        }
        glEnd();
    }
}

Color calculateShade(Color base, float factor) {
    return { base.r * factor, base.g * factor, base.b * factor };
}

void generateCubeColors(Cube& cube, Color baseColor, float lightDir[3]) {
    float shadeFactors[6];
    Vertex normals[6] = {
        {0, 0, -1}, // bottom
        {0, 0, 1},  // top
        {0, -1, 0}, // front
        {0, 1, 0},  // back
        {-1, 0, 0}, // left
        {1, 0, 0}   // right
    };

    for (int i = 0; i < 6; ++i) {
        float dotProduct = normals[i].x * lightDir[0] + normals[i].y * lightDir[1] + normals[i].z * lightDir[2];
        shadeFactors[i] = std::max(0.0f, dotProduct);
        cube.colors[i] = calculateShade(baseColor, 0.5f + 0.5f * shadeFactors[i]);
    }
}

bool isOccupied(int x, int y, int z) {
    return occupiedPositions.find(std::make_tuple(x, y, z)) != occupiedPositions.end();
}

void addCube(Vertex& start, float stepSize, float perspectiveFactor, Color baseColor, float lightDir[3], bool fillBelow) {
    int posX = static_cast<int>(start.x / stepSize);
    int posY = static_cast<int>(start.y / stepSize);
    int posZ = static_cast<int>(start.z / stepSize);
    if (!isOccupied(posX, posY, posZ)) {
        Cube cube;
        cube.position = start;
        cube.size = stepSize;
        cube.perspectiveFactor = perspectiveFactor;
        generateCubeColors(cube, baseColor, lightDir);

        cubes.push_back(cube);
        occupiedPositions.insert(std::make_tuple(posX, posY, posZ));

        if (fillBelow) {
            for (int i = 1; i <= 3; ++i) {
                int belowPosZ = posZ - i;
                if (!isOccupied(posX, posY, belowPosZ)) {
                    Cube belowCube;
                    belowCube.position = {start.x, start.y, start.z - i * stepSize};
                    belowCube.size = stepSize;
                    belowCube.perspectiveFactor = perspectiveFactor;
                    generateCubeColors(belowCube, baseColor, lightDir);

                    cubes.push_back(belowCube);
                    occupiedPositions.insert(std::make_tuple(posX, posY, belowPosZ));
                }
            }
        }
    }
}

std::vector<Vertex> generateStructuredPath(int length, float stepSize) {
    std::default_random_engine generator(static_cast<unsigned int>(std::time(0)));
    std::uniform_int_distribution<int> patternDist(0, 2);
    std::vector<Vertex> path;
    Vertex current = {0, 0, 0};

    for (int i = 0; i < length; ++i) {
        int pattern = patternDist(generator);
        switch (pattern) {
            case 0: // Straight line
                current.x += stepSize;
                break;
            case 1: // Staircase
                current.x += stepSize;
                current.z += stepSize;
                break;
            case 2: // Zigzag
                current.x += stepSize;
                current.y += (i % 2 == 0) ? stepSize : -stepSize;
                break;
        }
        path.push_back(current);
    }

    return path;
}

void fillPathWithBlocks(const std::vector<Vertex>& path, float stepSize, Color baseColor, float lightDir[3]) {
    std::default_random_engine generator(static_cast<unsigned int>(std::time(0)));
    std::uniform_real_distribution<float> perspectiveDist(0.5f, 1.5f);
    std::uniform_int_distribution<int> fillDist(0, 4);

    for (const auto& pos : path) {
        float perspectiveFactor = perspectiveDist(generator);
        bool fillBelow = (fillDist(generator) == 0);
        addCube(const_cast<Vertex&>(pos), stepSize, perspectiveFactor, baseColor, lightDir, fillBelow);
    }
}

void generateRandomCubes(int pathLength, float stepSize, Color baseColor) {
    cubes.clear();
    occupiedPositions.clear();
    float lightDir[3] = {0.5f, 0.5f, -1.0f};  // Direction of the light

    std::vector<Vertex> path = generateStructuredPath(pathLength, stepSize);
    fillPathWithBlocks(path, stepSize, baseColor, lightDir);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    for (const Cube& cube : cubes) {
        drawCube(cube);
    }
    glfwSwapBuffers(glfwGetCurrentContext());
}

void initOpenGL() {
    glEnable(GL_DEPTH_TEST);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0);
    glMatrixMode(GL_MODELVIEW);
    glTranslatef(0.0f, 0.0f, -50.0f);
    glRotatef(45, 1.0f, 1.0f, 0.0f);
}

void errorCallback(int error, const char* description) {
    std::cerr << "Error: " << description << std::endl;
}

void keyCallback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (key == GLFW_KEY_R && action == GLFW_PRESS) {
        Color baseColor = {0.8f, 0.7f, 0.6f};
        generateRandomCubes(100, 2.0f, baseColor);
    }
}

int main() {
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return -1;
    }

    glfwSetErrorCallback(errorCallback);
    GLFWwindow* window = glfwCreateWindow(800, 800, "Escher 3D Stairs", NULL, NULL);
    if (!window) {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glewInit();
    initOpenGL();

    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;

    // Setup Dear ImGui style
    ImGui::StyleColorsDark();

    // Setup Platform/Renderer bindings
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init("#version 330");

    Color baseColor = {0.8f, 0.7f, 0.6f};
    generateRandomCubes(200, 1.0f, baseColor);

    glfwSetKeyCallback(window, keyCallback);

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        // Start the ImGui frame
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // Create ImGui window
        ImGui::Begin("Controls");
        if (ImGui::Button("Regenerate")) {
            generateRandomCubes(100, 2.0f, baseColor);
        }
        ImGui::End();

        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        display();

        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        glfwSwapBuffers(window);
    }

    // Cleanup ImGui
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}