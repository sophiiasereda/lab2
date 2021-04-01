#!/usr/bin/python

import sys
import re
import hungalg
import eulerian

def check_uneven_vertices(edges, vertices):
    even_graph = True;
    deg_vertices = dict()
    for i, vertex in enumerate(vertices):
        deg_vertices[vertex] = 0
        for edge in edges:
            if edge['vertex1'] == vertex or edge['vertex2'] == vertex:
                deg_vertices[vertex] += 1
        if (deg_vertices[vertex] % 2 == 1): even_graph = False

    if even_graph == True: return True;

    print('Граф має непарні вузли:')
    countOfUnevenVertices = 0
    uneven_keys = []
    
    for vertex in deg_vertices.keys():
        if deg_vertices[vertex] % 2 == 1:
            countOfUnevenVertices += 1
            uneven_keys.append(vertex)
            print(vertex, '=', deg_vertices[vertex])
    
    print('Для вирішення задачі листоноші всі вузли повинні бути парними.')
    print('Деякі з ребер слід продублювати')
    return uneven_keys


file = open("l2-2.txt")

size = int(file.readline())
vertices = []
matrix = []
edges = []
tour_matrix = []

for i in range(size):
    vertices.append(chr(65 + i))

for line_index, line in enumerate(file):
    matrix.append(re.split('\s', re.sub('\n', '', line)))
    matrix[line_index] = list(map(float, matrix[line_index]))

for i in range(size - 1):
    for j in range(i + 1, size):
        value = matrix[i][j]
        if value <= 0: continue
        edges.append({'vertex1': vertices[i], 'vertex2': vertices[j], 'weight': value})
        tour_matrix.append((i + 1, j + 1))

uneven_vertices = check_uneven_vertices(edges, vertices)
uneven_matrix = []

for i, vertex_i in enumerate(uneven_vertices):
    uneven_matrix.append([])
    for j, vertex_j in enumerate(uneven_vertices):
        uneven_matrix[i].append(matrix[ord(vertex_i) - 65][ord(vertex_j) - 65])

print('Отримаємо наступні пари')
for edge in hungalg.minimize(uneven_matrix):
    print('(', uneven_vertices[edge[0]], '->', uneven_vertices[edge[1]], ')')
    vertex_index_1 = ord(uneven_vertices[edge[0]]) - 65
    vertex_index_2 = ord(uneven_vertices[edge[1]]) - 65
    matrix[vertex_index_1][vertex_index_2] *= 2 
    tour_matrix.append((vertex_index_1 + 1, vertex_index_2 + 1))

print('Отриманий шлях:')
tour = []
eulerian_tour = eulerian.find_eulerian_tour(sorted(list(set(tour_matrix))))
print('->'.join(map(str, eulerian_tour)))

print('Вага шляху: ', end = '')
tour_weight = 0
for i in range(size - 1):
    for j in range(i + 1, size):
        tour_weight += matrix[i][j]

print(tour_weight)
