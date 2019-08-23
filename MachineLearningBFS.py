import tkinter as tk
import time
import queue

#Create Grid
def create_grid(event=None):
    w = Frame.winfo_width() # Get current width of canvas
    h = Frame.winfo_height() # Get current height of canvas
    Frame.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, N):
        Frame.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, N):
        Frame.create_line([(0, i), (w, i)], tag='grid_line')
#Create Shape
def CreateShape(x,y,Time,color):
	time.sleep(Time)
	distx = N*x;disty = N*y
	Frame.create_rectangle(5+distx, 5+disty, N-5 +distx, N-5 +disty, outline='white', fill=color)
	Frame.update()
#Create Sys Shape
def CreateSysShape(x,y,Time,color):
	time.sleep(Time)
	distx = N*x;disty = N*y
	Frame.create_rectangle(distx, disty, N +distx, N +disty, outline='black', fill=color)
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
      elif(x < SystemCell[0] and y < SystemCell[1]):
      	return 0
      else:
      	Block[x][y] = 1
      	CreateShape(x,y,0,"pink")
#startBFS
def getorigin(eventorigin):
	x = eventorigin.x
	y = eventorigin.y
	x = int(x/N)
	y = int(y/N)

	if(Start[0]!= -1):
		if(End[0]!=-1):
			if(x == RunCell[0] and y == RunCell[1]):
				flag = BFS()
				print(flag)
				if(flag == True):
					traceBack()
					print(dist[End[0]][End[1]])
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
	N = 30
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
			CreateSysShape(i,j,0,"Black")
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
			CreateShape(x,y,0,"Purple")
		x = a
		y = b
		a = path[x][y][0]
		b = path[x][y][1]

#BFS
def BFS():
	BaseTime = 0
	global path,dist
	path = [[([]) for i in range(sizeX+10)] for i in range(sizeY+10)]
	dist = [[0 for i in range(sizeX+10)] for i in range(sizeY+10)]
	#direct up, right, down, left
	dx = [0,1,0,-1]
	dy = [-1,0,1,0]
	#Used init 2d array all zero
	used = [[0 for i in range(sizeX+10)] for i in range(sizeY+10)]
	#Queue
	q = queue.Queue(maxsize = sizeX*sizeY+10)
	path[Start[0]][Start[1]] = ([-1,-1])
	q.put([Start[0],Start[1]])
	while(q.empty() == False):
		Front = q.get()
		#Avoid going to System cells
		if(Front[0]<SystemCell[0] and Front[1]<SystemCell[1]):
			continue
		#Avoid going to used vertice
		if(used[Front[0]][Front[1]] == 1):
			continue
		#Process end when vertice go to End point
		if(Front[0] == End[0] and Front[1] == End[1]):
			CreateShape(Start[0],Start[1],BaseTime,"Red")
			CreateShape(End[0],End[1],BaseTime,"Green2")
			return True
		if(Front != Start):
			CreateShape(Front[0],Front[1],BaseTime,"yellow")
			CreateShape(Front[0],Front[1],BaseTime,"blue")
		#Mark this vertice used
		used[Front[0]][Front[1]] = 1
		for i in range(4):
			X = Front[0]+dx[i]
			Y = Front[1]+dy[i]
			if(used[X][Y] == 0 and Block[X][Y] == 0):
				if(X>=0 and X <= sizeX and Y>=0 and Y<=sizeY):
					#print('Co',X,Y,used[X][Y])
					#CreateShape(X,Y,"blue")
					dist[X][Y] = dist[Front[0]][Front[1]]+1
					path[X][Y] = ([Front[0],Front[1]])
					q.put([X,Y])
	return False		
#Main
InitMatrix()
#loop
root.mainloop()