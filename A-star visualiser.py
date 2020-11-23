import pygame

window_size = 800
node_size = 20

black = (0, 0, 0)
grey = (237, 245, 225)

red = (214, 40, 40)
orange = (255, 128, 0)
yellow = (253, 210, 25)
green = (83, 211, 209)
maroon = (255, 0, 127)
blue = (0, 0, 255)

start_node_color = yellow
end_node_color = green
open_set_color = green
closed_set_color = (142, 228, 175)
path_color = red

def draw_rect(screen, pos, color):
    pygame.draw.rect(screen, black, (pos[1], pos[0], node_size, node_size))
    pygame.draw.rect(screen, color, (pos[1] + 1, pos[0] + 1, node_size - 2, node_size - 2))

class Node:
    def __init__(self, color, pos):
        self.color = color
        self.row = pos[0]
        self.column = pos[1]
        self.g = None
        self.h = None
        self.f = None
        self.parent = None

    def draw(self, screen):
        draw_rect(screen, (self.row * node_size, self.column * node_size), self.color)

    def neighbours(self, nodes):
        neighbours = []
        for i, row in enumerate(nodes):
            for j, el in enumerate(row):
                if i == self.row:
                    if j == self.column - 1 or j == self.column + 1:
                        if el.color != black:
                            neighbours.append(el)
                elif i == self.row -1 or i == self.row + 1:
                    if j == self.column:
                        if el.color != black:
                            neighbours.append(el)
        return neighbours
    
    def scores(self, node, end):
        g = node.g + 1
        h = abs(end.row - self.row) + abs(end.column - self.column)
        return (g, h)

class Queue:
    def __init__(self):
        self.elements = []
    
    def insert(self, element, priority):
        self.elements.append((priority, element))
    
    def remove(self, element):
        for el in self.elements:
            if el[1] == element:
                self.elements.remove(el)
    
    def get(self):
        priorities = [el[0] for el in self.elements]
        priorities.sort()
        min = priorities[0]
        for el in self.elements:
            if el[0] == min:
                return el[1]
    
    def contains(self, element):
        for el in self.elements:
            if el[1] == element:
                return True
        return False

def init_nodes():
    nodes = [[None for i in range(0, window_size, node_size)] for j in range(0, window_size, node_size)]
    for i, row in enumerate(nodes):
        for j, _ in enumerate(row):
            if i == 0 or i == len(nodes) - 1:
                nodes[i][j] = Node(black, (i, j))
            elif j == 0 or j == len(nodes) - 1:
                nodes[i][j] = Node(black, (i, j))
            else:
                nodes[i][j] = Node(grey, (i, j))
    return nodes

def draw_nodes(screen, nodes):
    for row in nodes:
        for el in row:
            el.draw(screen)

def set_barrier(screen, status, nodes):
    if status == 0:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // node_size
            row = pos[1] // node_size
            for i, k in enumerate(nodes):
                for j, el in enumerate(k):
                    if el.row == row and el.column == column:
                        if el.color == grey:
                            nodes[i][j].color = black
        elif pygame.mouse.get_pressed()[2]:
            for i, row in enumerate(nodes):
                for j, _ in enumerate(row):
                    if i != 0 and i != len(nodes) - 1 and j != 0 and j != len(nodes) - 1:
                        if nodes[i][j].color == black:
                            nodes[i][j].color = grey
    else:
        return

def set_start(screen, status, nodes):
    if status == 1:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // node_size
            row = pos[1] // node_size
            for i, k in enumerate(nodes):
                for j, el in enumerate(k):
                    if el.row == row and el.column == column:
                        if el.color == grey:
                            nodes[i][j].color = start_node_color
                            return 2
        else:
            return status
    elif status == 2:
        if pygame.mouse.get_pressed()[2]:
            for i, row in enumerate(nodes):
                for j, _ in enumerate(row):
                    if nodes[i][j].color == start_node_color:
                        nodes[i][j].color = grey
                        return 1
        else:
            return status
    else:
        return status

def set_end(screen, status, nodes):
    if status == 3:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // node_size
            row = pos[1] // node_size
            for i, k in enumerate(nodes):
                for j, el in enumerate(k):
                    if el.row == row and el.column == column:
                        if el.color == grey:
                            nodes[i][j].color = end_node_color
                            return 4
        else:
            return status
    elif status == 4:
        if pygame.mouse.get_pressed()[2]:
            for i, row in enumerate(nodes):
                for j, _ in enumerate(row):
                    if nodes[i][j].color == end_node_color:
                        nodes[i][j].color = grey
                        return 3
        else:
            return status
    else:
        return status





def initialise_astar(nodes):
    global open_set
    global closed_set
    global start
    global end
    open_set = Queue()
    closed_set = Queue()
    for row in nodes:
        for el in row:
            if el.color == start_node_color:
                start = el
            if el.color == end_node_color:
                end = el
    start.f = 0
    start.g = 0
    start.h = 0
    open_set.insert(start, start.f)
    

def pathfinder(screen, status, nodes):
    if status == 5:
        initialise_astar(nodes)
        return 6
    elif status == 6:
        node = open_set.get()
        open_set.remove(node)
        neighbours = node.neighbours(nodes)
        for neighbour in neighbours:
            if (neighbour.row, neighbour.column) == (end.row, end.column):
                end.parent = node
                update_nodes(open_set, closed_set)
                return 7
            g, h = neighbour.scores(node, end)
            f = g + h
            if open_set.contains(neighbour) and neighbour.f <= f:
                pass
            elif closed_set.contains(neighbour) and neighbour.f <= f:
                pass
            else:
                neighbour.g = g
                neighbour.h = h
                neighbour.f = f
                neighbour.parent = node
                open_set.insert(neighbour, neighbour.f)
        closed_set.insert(node, 0)
        update_nodes(open_set, closed_set)
        return status
    else:
        return status

def update_nodes(open_set, closed_set):
    for el in open_set.elements:
        el[1].color = open_set_color
    for el in closed_set.elements:
        el[1].color = closed_set_color

def draw_path(status, end, start):
    if status == 7:
        end.color = path_color
        if end.parent == start:
            end.parent.color = path_color
            return end.parent, 8
        return end.parent, status
    else:
        return end, status


def main():
    global end
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption('A* algorithm visualiser')
    clock = pygame.time.Clock()
    nodes = init_nodes()
    run = True
    status = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif pygame.event.event_name(event.type) == 'KeyDown':
                status += 1
        
        set_barrier(screen, status, nodes)
        status = set_start(screen, status, nodes)
        status = set_end(screen, status, nodes)
        status = pathfinder(screen, status, nodes)
        if status == 7:
            end, status = draw_path(status, end, start)
        draw_nodes(screen, nodes)
        pygame.display.update()
        clock.tick(90)
    pygame.quit()
    return



print('enter to start: ', end='')
if input() == '':
    main()