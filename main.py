'''Nguyễn Hoàng Thịnh - 17110372'''

'''Package tạo giao diện mô phỏng thuật toán'''

from tkinter import Tk, Menu, BOTH, LEFT
from tkinter.ttk import Frame, Button
from tkinter import *

from tkinter.filedialog import Open
import tkinter.messagebox as mbox 

from queue import LifoQueue

import astaralgorithm as helper
import time
'''Lớp này sẽ đại diện cho một frame được gắn lên cửa sổ chương trình'''
class Form(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.tileList = [] #Thuộc tính này sẽ chứa danh sách các button đại diện cho 1 ô trên grid
		self.path = LifoQueue() #Đại diện cho một lời giải
		self.MAP = None
		self.initUI()


	'''Hàm khởi tạo các widget trên cửa sổ'''
	def initUI(self):
		#Tạo tiêu đề cho cửa sổ
		self.parent.title('Resolving A Star')
		#Xác định layout của frame
		self.pack(fill = BOTH, expand = 1)

		#Tạo một menu trên frame
		menuBar = Menu(self)
		self.parent.config(menu = menuBar)

		fileMenu = Menu(menuBar)
		fileMenu.add_command(label = "Import grid", command = self.importGrid)
		fileMenu.add_command(label = "Exit", command = self.exit)
		menuBar.add_cascade(label = "File", menu = fileMenu)

		#Tạo một frame khác trên frame hiện tại. Frame này sẽ chứa bản đồ
		self.tileGrid = Frame(self, width = 400, height = 400)
		self.tileGrid.pack(side = LEFT, anchor = N, expand = 1)

		#Tạo một frame khác trên frame hiện tại. Frame này sẽ chứa widget dùng để sử dụng các tính năng của chương trình
		self.frameWidget = Frame(self)
		self.frameWidget.pack(fill = BOTH, side = LEFT, anchor = N, expand = 0)

		#Hai phương thức columnconfigure() và rowconfigure() quy định khoảng cách giữa các widget.
		self.frameWidget.columnconfigure(0,pad=1)
		self.frameWidget.columnconfigure(1,pad=1)

		self.frameWidget.rowconfigure(0,pad=1)
		self.frameWidget.rowconfigure(1,pad=1)
		self.frameWidget.rowconfigure(2,pad=1)
		self.frameWidget.rowconfigure(3,pad=1)

		self.btnResolving = Button(self.frameWidget, text = "Resolving",command = self.resolving)
		self.btnResolving.grid(row = 0, column = 0)
		self.btnResolving["state"] = "disabled"

		self.btnSimulation = Button(self.frameWidget, text = "Simulation", command = self.simulation)
		self.btnSimulation.grid(row = 0, column = 1)
		self.btnSimulation["state"] = "disabled"

		self.frame3 = Frame(self.frameWidget)
		self.frame3.grid(row = 1, column = 0)

		self.labelStart = Label(self.frame3,text="Start")
		self.labelStart.pack(side = LEFT)
		self.entryStartx = Entry(self.frame3, width = 5)
		self.entryStartx.pack(side = LEFT)
		self.entryStarty = Entry(self.frame3, width = 5)
		self.entryStarty.pack(side = LEFT)

		self.frame4 = Frame(self.frameWidget)
		self.frame4.grid(row = 2, column = 0)

		self.labelGoal = Label(self.frame4,text="Goal")
		self.labelGoal.pack(side = LEFT)
		self.entryGoalx = Entry(self.frame4, width = 5)
		self.entryGoalx.pack(side = LEFT)
		self.entryGoaly = Entry(self.frame4, width = 5)
		self.entryGoaly.pack(side = LEFT)

		self.listboxResult = Listbox(self.frameWidget)
		self.listboxResult.grid(row = 3, columnspan = 2)


	#Hàm lấy dữ liệu grid từ file txt
	def importGrid(self):
		#List lưu các định dạng file khác nhau để đọc file
		ftypes = [('All files','*')]
		#Hiển thị file dialog chúng ta cần gọi hàm Open(). Hàm này trả về đường dẫn file
		dlg = Open(self,filetypes = ftypes)
		fl = dlg.show()

		with open(fl) as textFile:
			lines = [line.split() for line in textFile]

		self.gridWidth = len(lines)
		self.gridHeight = len(lines[0])

		results = []
		for i in range(self.gridWidth):
			results.append([])
			for j in range(self.gridHeight):
				if lines[i][j] == "1":
					results[i].append(1)
				else:
					results[i].append(0)
		self.MAP = results
		# Đưa grid lên form
		self.updateUI()

	#Sau khi import được grid từ file txt, ta tiến hành đưa file lên giao diện
	def updateUI(self):
		c = self.tileGrid.winfo_width()
		r = self.tileGrid.winfo_height()
		for k in range(self.gridHeight):
			self.tileGrid.columnconfigure(k,weight = int(c/10), pad=2)
		for l in range(self.gridWidth):
			self.tileGrid.rowconfigure(l,weight = int(r/10),pad=2)
			self.tileList = []
		for i in range(self.gridWidth):
			self.tileList.append([])
			for j in range(self.gridHeight):
				bgTile = "white"
				if self.MAP[i][j] == 1:
					bgTile = "black"
				btnTile =  Button(self.tileGrid, width = 5, height = 5, bg = bgTile)
				btnTile.grid(row = i, column = j)
				btnTile["state"] = "disabled"
				self.tileList[i].append(btnTile)
		self.btnResolving["state"] = "active"

	def resolving(self):
		xStart = int(self.entryStartx.get())
		yStart = int(self.entryStarty.get())
		xGoal = int(self.entryGoalx.get())
		yGoal = int(self.entryGoaly.get())
		self.start = (xStart,yStart)
		self.goal = (xGoal, yGoal)

		p = helper.getResolving(self.MAP,self.start,self.goal)
		self.listboxResult.delete(0,END)
		self.path = LifoQueue()
		while p.prev != None:
			self.path.put(p.position)
			self.listboxResult.insert(END,p.position)
			p = p.prev
		self.path.put(self.start)
		self.listboxResult.insert(END,self.start)
		self.btnSimulation["state"] = "active"

	def simulation(self):
		self.btnSimulation["state"] = "disabled"
		self.btnResolving["state"] = "disabled"
		while not self.path.empty():
			tile = self.path.get()
			self.tileList[tile[0]][tile[1]].configure(bg = "#4ad2f7")
			self.parent.update()
			time.sleep(0.1)
			self.tileList[tile[0]][tile[1]].configure(bg = "white")
			self.parent.update()
			time.sleep(0.1)
			self.tileList[tile[0]][tile[1]].configure(bg = "#4ad2f7")
			self.parent.update()
			time.sleep(0.1)
			self.tileList[tile[0]][tile[1]].configure(bg = "white")
			self.parent.update()
			time.sleep(0.1)
			self.tileList[tile[0]][tile[1]].configure(bg = "#4ad2f7")
			self.parent.update()
			time.sleep(0.1)
		self.btnResolving["state"] = "active"
		self.parent.update()

	def exit(self):
		self.quit()



root = Tk()
'''5 dòng lệnh bên dưới nhằm tạo ra kích thước của cửa sổ và vị trí mà cửa sổ chương trình sẽ hiển thị'''
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("700x400+{}+{}".format(positionRight - 350, positionDown - 200))

app = Form(root)


root.mainloop()


