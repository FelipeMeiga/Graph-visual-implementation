import pygame
import math
import random

pygame.init()

size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Classe Grafo
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.positions = {}
        self.radius = 15

    def add_node(self, node, position):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            self.positions[node] = position

    def add_edge(self, node1, node2):
        if node1 in self.adjacency_list and node2 in self.adjacency_list:
            self.adjacency_list[node1].append(node2)
            self.adjacency_list[node2].append(node1)

    def get_node_at_pos(self, pos):
        for node, position in self.positions.items():
            if math.sqrt((position[0] - pos[0]) ** 2 + (position[1] - pos[1]) ** 2) < self.radius:
                return node
        return None

    def bfs(self, start_node):
        visited = []
        queue = [start_node]
        
        while queue:
            current_node = queue.pop(0)
            if current_node not in visited:
                visited.append(current_node)
                self.visualize_node(current_node, RED)
                pygame.time.wait(500)
                self.visualize_node(current_node, BLUE)
                for neighbor in self.adjacency_list[current_node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

    def visualize_node(self, node, color):
        pygame.draw.circle(screen, color, self.positions[node], self.radius)
        pygame.display.flip()
        self.redraw_graph()

    def redraw_graph(self):
        screen.fill(WHITE)
        
        for node, neighbors in self.adjacency_list.items():
            start_pos = self.positions[node]
            for neighbor in neighbors:
                end_pos = self.positions[neighbor]
                self.draw_edge(start_pos, end_pos)
        
        for node in self.adjacency_list:
            self.draw_node(node, BLUE)

    def draw_edge(self, start_pos, end_pos):
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)

    def draw_node(self, node, color):
        position = self.positions[node]
        pygame.draw.circle(screen, color, position, self.radius)

graph = Graph()

selected_node = None
mouse_down = False
adding_edge = False
node_pair = []
node_name = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 3:
                node = graph.get_node_at_pos(pos)
                if node:
                    graph.bfs(node)
            elif event.button == 1:
                if adding_edge:
                    node = graph.get_node_at_pos(pos)
                    if node:
                        node_pair.append(node)
                        if len(node_pair) == 2:
                            graph.add_edge(node_pair[0], node_pair[1])
                            adding_edge = False
                            node_pair = []
                else:
                    selected_node = graph.get_node_at_pos(pos)
                    mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
                selected_node = None
        elif event.type == pygame.MOUSEMOTION:
            if mouse_down and selected_node:
                graph.positions[selected_node] = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                adding_edge = True
            if event.key == pygame.K_e:
                graph.add_node(str(node_name), (random.choice(range(pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[0] + 50)),
                                                random.choice(range(pygame.mouse.get_pos()[1] - 50, pygame.mouse.get_pos()[1] + 50))))
                node_name += 1

    graph.redraw_graph()
    pygame.display.flip()

pygame.quit()
