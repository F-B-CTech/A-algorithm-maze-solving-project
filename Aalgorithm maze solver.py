import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 25 #by changing this variable , you can change the size of the cells in the grid and diffculty of the maze

MAX_GRADIENT = 255  # Maximum intensity for gradient color

# Create the screen with maximized window
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 0, 0)
RED = (255, 0, 0)  # Color for the moving point
BLUE = (0, 0, 255)  # Color for the path

# Maze generation function
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # 1 = wall
    stack = [(1, 1)]
    maze[1][1] = 0  # Start point

    while stack:
        current_cell = stack[-1]
        x, y = current_cell
        neighbors = []

        # Check for unvisited neighbors
        if x > 1 and maze[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < cols - 2 and maze[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 1 and maze[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < rows - 2 and maze[y + 2][x] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            maze[(y + ny) // 2][(x + nx) // 2] = 0  # Remove wall
            maze[ny][nx] = 0  # Mark next cell as passage
            stack.append(next_cell)
        else:
            stack.pop()

    return maze

# A* Pathfinding Algorithm
def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, maze):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get valid neighbors
def get_neighbors(node, maze):
    neighbors = []
    x, y = node
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
            neighbors.append((nx, ny))
    return neighbors

# Reconstruct the path from the came_from map
def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()  # Reverse the path to get from start to goal
    return total_path

# Draw the gradient for visited cells
def draw_gradient(x, y, intensity):
    color = (intensity, intensity // 2, 0)  # Gradient from yellow to transparent
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw the maze function
def draw_maze(maze, visited, path=[]):
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (x, y) in visited:
                draw_gradient(x, y, visited[(x, y)])  # Draw gradient for visited cells
            elif (x, y) in path:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw path
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Create the screen with fullscreen or maximized window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Allow window resizing
pygame.display.set_caption("Maze Navigation with A* Pathfinding and Gradient Effect")

# Generate maze
maze = generate_maze(ROWS, COLS)

# Character position and visited cells
character_pos = [1, 1]  # Start position of the character
visited_cells = {}  # Dictionary to track visited cells and their gradient intensity

# Define start and goal positions for A*
start = (1, 1)
goal = (COLS - 2, ROWS - 2)

# Find the path using A*
path = astar(maze, start, goal)

# Set the initial index for the path
path_index = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check for Esc key
                running = False

    # Move the character along the A* path
    if path and path_index < len(path):
        character_pos = list(path[path_index])
        path_index += 1

    # Track visited cells and their gradient intensity
    visited_cells[(character_pos[0], character_pos[1])] = MAX_GRADIENT

    # Fill the background
    screen.fill(GREEN)

    # Draw the maze
    draw_maze(maze, visited_cells, path)

    # Draw the character
    pygame.draw.circle(screen, RED, (character_pos[0] * CELL_SIZE + CELL_SIZE // 2, character_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    # Update the display
    pygame.display.flip()

    # Control the speed of the character movement
    pygame.time.delay(100)  # Delay in milliseconds

pygame.quit()