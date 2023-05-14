import pygame
import sys
import math
import random
import re
import pathlib
from create_graph import criar_grafo

from pygame.locals import *
from models.Graph import Graph, Edge
from models.Note import Note
from models.MST import kruskal, prim

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

def draw_nodes(screen, graph: Graph):
    for node, neighbors in graph.adj_list.items():
        pygame.draw.circle(screen, node.color, (node.x, node.y), node.radius)
        font = pygame.font.SysFont(None, 20)
        label = font.render(node.filename, True, WHITE)
        screen.blit(label, (node.x - label.get_width() // 2, node.y - 20 - label.get_height()))

def draw_line(screen, edge):
    start_node = edge.start_node
    end_node = edge.end_node

    angle = math.atan2(end_node.y - start_node.y, end_node.x - start_node.x)

    start_x = start_node.x + start_node.radius * math.cos(angle)
    start_y = start_node.y + start_node.radius * math.sin(angle)
    end_x = end_node.x - end_node.radius * math.cos(angle)
    end_y = end_node.y - end_node.radius * math.sin(angle)

    # Calculate midpoint coordinates
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    # Draw the line
    edge.color = YELLOW if edge.mst else WHITE

    pygame.draw.line(screen, edge.color, (start_x, start_y), (end_x, end_y), 2)

    # Render the distance value
    font = pygame.font.Font(None, 20)
    text = font.render(str(edge.distance), True, edge.color)
    text_rect = text.get_rect(center=(mid_x -10, mid_y -10))  # Adjust the y-coordinate with an offset
    screen.blit(text, text_rect)

def draw_edges(screen, graph: Graph):
    for edge in graph.edge_list:
        draw_line(screen, edge)

def update_node_positions(screen, graph: Graph, min_distance=100):

    node_list = graph.get_nodes()
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            node1 = node_list[i]
            node2 = node_list[j]
            dx = node1.x - node2.x
            dy = node1.y - node2.y
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            if dist < min_distance:
                force = 1000 / dist ** 2 # adjust the force factor as needed
                node1_x_force = force * dx / dist
                node1_y_force = force * dy / dist
                node2_x_force = -node1_x_force
                node2_y_force = -node1_y_force
                node1.x += node1_x_force
                node1.y += node1_y_force
                node2.x += node2_x_force
                node2.y += node2_y_force

        if node1.x - node1.radius < 0:
            node1.x = node1.radius
        elif node1.x + node1.radius > screen.get_width():
            node1.x = screen.get_width() - node1.radius
        if node1.y - node1.radius < 0:
            node1.y = node1.radius
        elif node1.y + node1.radius > screen.get_height():
            node1.y = screen.get_height() - node1.radius

def handle_events(screen, graph: Graph):
    node_list = graph.get_nodes()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for node in node_list:
                if node.dragging == False:
                    if event.button == 1:
                        if node.x - node.radius <= event.pos[0] <= node.x + node.radius and node.y - node.radius <= event.pos[1] <= node.y + node.radius:
                            node.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for node in node_list:
                if node.dragging == True:
                    node.dragging = False
                    
        elif event.type == pygame.MOUSEMOTION:
            for node in node_list:
                if node.dragging == True:
                    node.update_position(event.pos[0], event.pos[1], screen)
            update_node_positions(screen, graph)
        
        elif event.type == pygame.VIDEORESIZE:
            # If the screen is resized, update the screen size
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)
import click

@click.command()
@click.argument('path')
@click.argument('alg')
def main(path, alg):

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH), pygame.RESIZABLE)

    color = YELLOW if alg == 'kruskal' else WHITE
    main_graph = criar_grafo(path, color)

    running = True

    import asyncio

    async def apply_mst_find(main_graph, alg):
        colorMancha = 0 
        if alg == 'kruskal':
            mst = kruskal(main_graph)
        elif alg == 'prim':
            colorMancha = 1
            mst = prim(main_graph)

        for edge in mst:
            if colorMancha:
                edge.start_node.color = (255, 255, 0)
                edge.end_node.color = (255, 255, 0)
            edge.mst = True
            await asyncio.sleep(2)

    async def main_loop(graph):
        mst_task = asyncio.create_task(apply_mst_find(main_graph, alg))
        while running:
            handle_events(screen, main_graph)
            screen.fill((0, 0, 0))
            draw_edges(screen, main_graph)
            draw_nodes(screen, main_graph) 
            pygame.display.update()
            if mst_task.done():
                await mst_task
            await asyncio.sleep(0.001)

    asyncio.run(main_loop(main_graph))

    # Quit pygame
    pygame.quit()

if __name__ == '__main__':
    main()