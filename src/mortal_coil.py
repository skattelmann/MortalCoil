import requests
import networkx as nx
import numpy as np

def solve():
	board_info = get_board_info()	#get raw board info
	board = make_board(board_info)	#generate a matrix from the board info 
	print(board)

def make_board(board_info):
	[ dimx, dimy, board_string ] = board_info
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
	return [int(raw_dimx), int(raw_dimy), [int(i) for i in board_string.replace('.','0').replace('X','1')] ]

