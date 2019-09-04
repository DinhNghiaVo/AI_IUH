import tkinter as tk
import time
import queue

#Create Grid
def create_grid(event=None):
    w = Frame.winfo_width() # Get current width of canvas
    h = Frame.winfo_height() # Get current height of canvas


    # Creates all vertical lines at intevals of 100
    for i in range(0, w, N):
        Frame.create_line([(i, 0), (i, h)], fill="gray")

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, N):
        Frame.create_line([(0, i), (w, i)], fill="gray")
#Create Shape
def CreateShape(x,y,Time,color):
	time.sleep(Time)
	distx = N*x;disty = N*y
	Frame.create_rectangle(5+distx, 5+disty, N-5 +distx, N-5 +disty, outline='white', fill=color)
	Frame.update()
#Clear Grid
def ClearGrid():
	for i in range(0,50):
		for j in range(0,50):
			if(not(i<SystemCell[0] and j<SystemCell[1]) and not(i==Start[0] and j==Start[1]) and not(i==End[0] and j==End[1])):
				Block[i][j] = 0
				CreateShape(i,j,0,"white")
#Event Origin
def dragOrigin(eventorigin):
      x = eventorigin.x
      y = eventorigin.y
      x = int(x/N)
      y = int(y/N)
      if(x == RunCell[0] and y == RunCell[1]):
      	return 0
      elif(x == Start[0] and y == Start[1]):
      	return 0
      elif(x == End[0] and y == End[1]):
      	return 0
      else:
      	Block[x][y] = 1
      	CreateShape(x,y,0,"Black")
#startBFS
def getorigin(eventorigin):
	x = eventorigin.x
	y = eventorigin.y
	x = int(x/N)
	y = int(y/N)

	if(Start[0]!= -1):
		if(End[0]!=-1):
			if(x == RunCell[0] and y == RunCell[1]):
				start_time = time.time()
				flag = a_star_search(Start,End)
				end_time = time.time()
				print(flag)
				print (str((end_time - start_time))+ str("  s"))
				if(flag == True):
					traceBack()
					#print(dist[End[0]][End[1]])
			elif(x == ClearCell[0] and y == ClearCell[1]):
				ClearGrid()
			elif(x == Start[0] and y == Start[1]):
				CreateShape(Start[0],Start[1],0,"white")
				Start[0] = -1
				Start[1] = -1
			elif(x == End[0] and y == End[1]):
				CreateShape(End[0],End[1],0,"white")
				End[0] = -1
				End[1] = -1
		elif(x != Start[0] or y != Start[1]):
			End[0] = x
			End[1] = y
			CreateShape(x,y,0,"Orange")
	elif(x != End[0] or y != End[1]):
		Start[0] = x
		Start[1] = y
		CreateShape(x,y,0,"Red")	

#Init Grid
def InitMatrix():
	#Gobal varaiable
	global Frame,N,root,Start,End,sizeX,sizeY,Block
	root = tk.Tk()
	sizeX = 50
	sizeY = 50
	Block = [ [0 for i in range(sizeX+10)] for i in range(sizeY+10)]
	N = 30 # kích thước của 
	Frame = tk.Canvas(root, height=1500, width=1500, bg='white')
	Frame.pack(fill=tk.BOTH, expand=True)
	Frame.bind('<Configure>', create_grid)
	# Frame.bind("<Button 1>",getorigin)
	Frame.bind("<Button 1>",getorigin)
	Frame.bind("<B1-Motion>",dragOrigin)
	#Start Cell: color Red
	Start = ([5,6])
	CreateShape(Start[0],Start[1],0,"Red")
	#End Cell: color Orange
	End = ([30,20])
	CreateShape(End[0],End[1],0,"Orange")

	#System Cell: color Black
	global SystemCell
	SystemCell = ([3,2])
	for i in range(0,SystemCell[0]):
		for j in range(0,SystemCell[1]):
			CreateShape(i,j,0,"Black")
	#Run Cell: color Green
	global RunCell
	RunCell = ([0,0])
	CreateShape(RunCell[0],RunCell[1],0,"Green")
	#Clear Cell: color Blue
	global ClearCell
	ClearCell = ([1,0])
	CreateShape(ClearCell[0],ClearCell[1],0,"Blue")
#printTrack
def traceBack():
	x = End[0]
	y = End[1]
	a = path[x][y][0]
	b = path[x][y][1]
	while(a!=-1 and b!=-1):
		if(x != End[0] or y != End[1]):
			CreateShape(x,y,0,"Red")
		x = a
		y = b
		a = path[x][y][0]
		b = path[x][y][1]
#A Start Search
def heuristic(a,b): # G(x)
	(x1,y1) = a
	(x2,y2) = b
	return abs(x1-x2)+abs(y1-y2)
def Astar_ValidNode(Node):
	if(Node[0]>=0 and Node[0]<=sizeX and Node[1]>=0 and Node[1]<=sizeY and Block[Node[0]][Node[1]] == 0):
		return True
	return False
def a_star_search(start,goal):
	global path,dist
	path = [[([]) for i in range(sizeX+10)] for i in range(sizeY+10)]
	start = (start[0],start[1])
	goal = (goal[0],goal[1])
	path[Start[0]][Start[1]] = ([-1,-1])
	#Base Time
	BaseTime = 0
	#Direction
	dx = [0,1,0,-1]
	dy = [-1,0,1,0]
	#Queue
	frontier = queue.PriorityQueue()
	Cell = (0,start)
	frontier.put((0,start))
	cost_so_far = {start: 0}
	while not frontier.empty():
		current = frontier.get()[1]
		#Reach Goal
		if(current == goal):
			CreateShape(Start[0],Start[1],BaseTime,"Green2")# khởi tạo điểm bắt đầu 
			CreateShape(End[0],End[1],BaseTime,"Green2")# Khởi tạo điểm kết thúc
			return True
		#Draw Blue spot
		if(current != start):
			CreateShape(current[0],current[1],BaseTime,"yellow")
			CreateShape(current[0],current[1],BaseTime,"aquamarine")
		#Scout 4 directions
		for i in range(4):
			Next = (current[0]+dx[i],current[1]+dy[i])
			if(not Astar_ValidNode(Next)):
				continue
			new_cost = cost_so_far[current]+1
			if(Next not in cost_so_far or new_cost < cost_so_far[Next]):#Min-Heap: ở đây giá trị của nút gốc là nhỏ hơn hoặc bằng các giá trị của các nút con
				cost_so_far[Next] = new_cost
				priority = new_cost+heuristic(goal,Next) # hàm  heuristis được gọi truyền vào  điểm kết thúc và điểm tiếp theo để duyệt và trả về khoảng cách giữa 2 điểm
				frontier.put((priority,Next))
				path[Next[0]][Next[1]] = ([current[0],current[1]])
	return False		
#Main
InitMatrix()
#loop
root.mainloop()