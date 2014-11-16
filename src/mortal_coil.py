import requests
import numpy as np
from graph_tool.all import *

def solve():
	board_info = get_board_info()	#get raw board info
	board = make_board(board_info)	#generate a matrix from the board info 
	graph_info = make_vertices(board)
	graph = make_edges(graph_info)
	graph_draw(graph, vertex_text=graph.vertex_index, vertex_font_size=4, output_size=(300, 300), fit_view=True)

def make_edges(graph_info):
	(g, vertices, dimx, dimy) = graph_info
	for i in range(dimy):
		for j in range(dimx):
			if vertices[i][j] != None and i > 0 and vertices[i-1][j] != None:
				g.add_edge(vertices[i][j], vertices[i-1][j])
			if vertices[i][j] != None and j < dimx-1 and vertices[i][j+1] != None:
				g.add_edge(vertices[i][j], vertices[i][j+1])
			if vertices[i][j] != None and i < dimy-1 and vertices[i+1][j] != None:
				g.add_edge(vertices[i][j], vertices[i+1][j])
			if vertices[i][j] != None and j > 0 and vertices[i][j-1] != None:
				g.add_edge(vertices[i][j], vertices[i][j-1])
	return g

def make_vertices(board):
	g = Graph(directed=False)
	(dimy, dimx) = board.shape
	vertices = []
	for i in range(dimy):
		new_row = []
		for j in range(dimx):
			if board[i,j] == 0:
				new_vertex = g.add_vertex()
				new_row.append(new_vertex)
			else:
				new_row.append(None)
				continue
		vertices.append(new_row)
	return (g, vertices, dimx, dimy)

def make_board(board_info):
	( dimx, dimy, board_string ) = board_info
	board = [ board_string[i*dimx:i*dimx+dimx] for i in range(0,dimy) ]	
	return np.matrix(board, dtype=np.uint8)

def get_board_info():
	username = 'SpaceMonkey'
	password = 'fuckyou'
	html_code = str(requests.get('http://www.hacker.org/coil/', params={'name': username, 'password': password}).content)
	info_start = html_code.find('FlashVars') + 18
	info_end = info_start + html_code[info_start:].find('"')
	raw_info = html_code[info_start:info_end].split('&')
	[raw_dimx, raw_dimy, board_string] = [ data.split('=')[1] for data in raw_info ]
	return ( int(raw_dimx), int(raw_dimy), [int(i) for i in board_string.replace('.','0').replace('X','1')] )

