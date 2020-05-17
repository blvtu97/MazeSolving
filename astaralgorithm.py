#Nguyễn Hoàng Thịnh - 17110372
from math import sqrt
vectorDirections = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]

'''Tạo class Node, đại diện cho một trạng thái. Một trạng thái của grid 10x10
được biểu diễn bởi bộ bốn(position,g,f,prev). Trong đó:
position: Là tọa hiện tại nó đang đứng
g là chi phí thực đi từ node start cho tới node hiện tại
f là chi phí đi từ node start cho tới node hiện tại + ước lượng từ node hiện tại cho tới goal
'''
class Node:
	def __init__(self,position = None, g= 0, f= 0, prev = None):
		self.position = position
		self.g = g
		self.f = f 
		self.prev = prev


	def  __str__(self):
		return str(self.position)

'''Hàm lấy ra node có vị trí position trong hàng đợi'''
def getNode(position,queue):
	for item in queue:
		if position[0] == item.position[0] and position[1] == item.position[1]:
			return item
	return None


def astar(MAP,start,goal):
	PQ = [] #Tạo hàng đợi ưu tiên
	V = [] #Các node đã xet
	S = Node(start)
	S.f = sqrt (goal[0]**2 + goal[1]**2) # heuristic dùng straight-line
	PQ.append(S)
	V.append(S)
	while len(PQ)>0:
		#Loại bỏ node có f(n) thấp nhất ra khỏi hàng đợi ưu tiên
		n = PQ[0]
		n_idx = 0
		for idx, item in enumerate(PQ):
			if item.f < n.f:
				n = item
				n_idx = idx
		PQ.pop(n_idx)

		# Kiểm tra  n có phải là Goal State hay chưa
		if n.position[0] == goal[0] and n.position[1] == goal[1]:
			return n

		#Mở rộng node n
		for directon in vectorDirections:
			n_new_position =(n.position[0]+directon[0], n.position[1] + directon[1])

			#Kiểm tra vị trí có thuộc trong miền grid hay không
			if n_new_position[0] < 0 or n_new_position[0] > len(MAP) - 1 or n_new_position[1] < 0 or n_new_position[1] > len(MAP[0]) - 1:
				continue
			#Nếu là chướng ngại vật thì bỏ qua
			if MAP[n_new_position[0]][n_new_position[1]] == 1:
				continue
			n_new_node = Node(n_new_position)

			# Ta đặt
			g = n.g + 1
			f = g + sqrt((goal[0] - n_new_position[0])**2 + (goal[1] - n_new_position[1])**2)

			#Nếu Node n' chưa có trong PQ và V:
			if getNode(n_new_position,PQ) == None and getNode(n_new_position,V) == None:
				n_new_node.g = g
				n_new_node.f = f
				n_new_node.prev = n 
				PQ.append(n_new_node)
				V.append(n_new_node)
			#Ngược lại nếu Node n' có trong PQ:
			elif getNode(n_new_position,PQ) != None:
				p = getNode(n_new_position,PQ) 
				if p.f > f:
					# Update n'
					p.g = g
					p.f = f 
					p.prev = n 
			#Ngược lại nếu Node n' có trong V:
			elif getNode(n_new_position,V) != None:
				p = getNode(n_new_position,V)
				if p.f > f:
					# Update n'
					p.g = g 
					p.f = f 
					p.prev = n 
					PQ.append(p)
	return None


def getResolving(MAP,start,goal):
	p = astar(MAP,start,goal)
	return p 


MAP = [[0,0,0,0,0,0,0,0,0,0],
	   [0,0,0,0,0,1,0,0,0,0],
	   [0,1,0,0,0,1,1,1,1,0],
	   [0,1,0,0,0,1,0,0,0,0],
	   [0,1,1,1,1,1,0,0,0,0],
	   [0,0,0,1,0,0,0,0,0,0],
	   [0,0,0,1,0,0,0,0,0,0],
	   [0,0,0,1,0,0,0,1,0,0],
	   [0,0,0,0,0,0,0,1,0,0],
	   [0,0,0,0,0,0,0,1,0,0]]
start = (0,0)
goal = (8,9)

p = getResolving(MAP,start,goal)

while p.prev != None:
	print(p)
	p = p.prev




