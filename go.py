import copy
import random

######################################################################################################
class GoBoard(object):
	def __init__(self, n):
		self.n = n
		self.turn = 0

		a = []
		for i in range(0,n):
			a.append(" ")
		self.grid = []
		for i in range(0,n):
			self.grid.append(a[:])

	def display(self):
		a = ""
		for i in range(0,self.n):
			if (self.n - i) < 10:
				a = a + "\n "
			else:
				a = a + "\n"
			a = a + str(self.n - i) + " |"
			for j in range(0, self.n):
				a = a + str(self.grid[i][j]) + "|"
			

		a = a + "\n    "
		for i in range(0,self.n):
			a = a + chr(65+i) + " "

		if self.turn % 2 == 0:
			a = a + "\nTurn " + str(self.turn) + ": X to move\n"
		else:
			a = a + "\nTurn " + str(self.turn) + ": O to move\n"



		return a	
	


	def capture(self, X, i_check=None, j_check=None): 
		numgroups = 0
		safety = [] 
		groups = copy.deepcopy(self.grid)
		imembers = []
		jmembers = []

		if i_check == None:
			for i in range(0, self.n):
				for j in range(0, self.n):
					if groups[i][j] == X:
				
						imembers.append(i)
						jmembers.append(j)
						alive = False
				
						while len(imembers) > 0:
							I = imembers.pop()
							J = jmembers.pop()

							groups[I][J] = numgroups
							if I != 0 and groups[I-1][J] == X:
								imembers.append(I-1)
								jmembers.append(J)
							elif I != 0 and groups[I-1][J] == " ":
								alive = True
							if J != 0 and groups[I][J-1] == X:
								imembers.append(I)
								jmembers.append(J-1)
							elif J != 0 and groups[I][J-1] == " ":
								alive = True
							if I != self.n-1 and groups[I+1][J] == X:
								imembers.append(I+1)
								jmembers.append(J)
							elif I != self.n-1 and groups[I+1][J] == " ":
								alive = True
							if J != self.n-1 and groups[I][J+1] == X:
								imembers.append(I)
								jmembers.append(J+1)
							elif J != self.n-1 and groups[I][J+1] == " ":
								alive = True

						safety.append(alive)
						numgroups = numgroups + 1
		else:
			checklist_i = []
			checklist_j = []
			checklist_i.append(i_check)
			checklist_j.append(j_check)
			if i_check != 0:
				checklist_i.append(i_check-1)
				checklist_j.append(j_check)
			if i_check != self.n-1:
				checklist_i.append(i_check+1)
				checklist_j.append(j_check)
			if j_check != 0:
				checklist_i.append(i_check)
				checklist_j.append(j_check-1)
			if j_check != self.n-1:
				checklist_i.append(i_check)
				checklist_j.append(j_check+1)

			for i, j in zip(checklist_i, checklist_j):
					if groups[i][j] == X:
				
						imembers.append(i)		#add this X to the lists
						jmembers.append(j)
						alive = False
				
						while len(imembers) > 0:	#for each member:
							I = imembers.pop()
							J = jmembers.pop()

							groups[I][J] = numgroups 		#Label by group number
							if I != 0 and groups[I-1][J] == X:	#Check above
								imembers.append(I-1)
								jmembers.append(J)
							elif I != 0 and groups[I-1][J] == " ":
								alive = True
							if J != 0 and groups[I][J-1] == X:	#Check left
								imembers.append(I)
								jmembers.append(J-1)
							elif J != 0 and groups[I][J-1] == " ":
								alive = True
							if I != self.n-1 and groups[I+1][J] == X:	#Check below
								imembers.append(I+1)
								jmembers.append(J)
							elif I != self.n-1 and groups[I+1][J] == " ":
								alive = True
							if J != self.n-1 and groups[I][J+1] == X:	#Check right
								imembers.append(I)
								jmembers.append(J+1)
							elif J != self.n-1 and groups[I][J+1] == " ":
								alive = True

						safety.append(alive)
						numgroups = numgroups + 1	


		for i in range(0, self.n):
			for j in range(0, self.n):
				if isinstance(groups[i][j], int):
					if safety[groups[i][j]]:
						groups[i][j] = X
					else:
						groups[i][j] = " "
		self.grid = groups


	def makeMove(self, textcoord, X):
		Y = "X"
		if X == "X":
			Y = "O"

		try:
			letter = textcoord[0]
			number = textcoord[1:]

			j = ord(letter)

			if j > 64 and j < (65 + self.n):
				j = j - 65
			elif j > 96 and j < (97 + self.n):
				j = j - 97
			else:
				int("not and int lol")
	
		
			if j < 0:
				int("not an int lol")

			
			i = self.n - int(number)
			if i < 0 or i > (self.n - 1):
				int("not an int lol")

		except:
			return 1



		if self.grid[i][j] != " ":
			return 2
	
		

		testgrid = copy.deepcopy(self)
		testgrid.grid[i][j] = X
		testgrid.capture(Y, i, j)
		testgrid.capture(X, i, j)

		if testgrid.grid[i][j] == ' ':
			return 3

		else:
			self.grid = testgrid.grid
			self.turn = self.turn + 1
			return 0


######################################################################################################
class GoManager(object):
	def __init__(self):
		self.active = False
		self.passed = False
		self.game = None



	def tell(self, read, player):
		
		if str(read[:4]) == str("@go "):
			read = read[4:]

			if read[:4] == "help":
				self.out = "start N - begins NxN game\nf3 - Place a stone on intersection f3\npass- pass your turn\n"	
		
			elif not self.active:
					if read[:6] == "start ":
						try:
							self.game = GoBoard(int(read[6:]))
							self.active = True
							self.out = self.game.display()
							self.firstmove = random.randint(0,1)
							self.out = self.out + "Player " + str(self.firstmove + 1) + " to start."
						except:
							self.out = "Invalid input"
					else:
						self.out = "Invalid input"		
			

			else:
					if read == "pass":				# player passing go
						self.turnparity = self.game.turn % 2

						if (self.turnparity == 0 and player == self.firstmove) or (self.turnparity == 1 and player != self.firstmove):
							self.game.turn = self.game.turn + 1
							self.out = self.game.display()
							if self.passed == False:
								self.passed = True
							else:
								self.out = self.out + "gg"
								self.active = False
								self.passed = False
								self.game = None
						else:
							self.out = "Not your turn"


					else:						# player making move
						
						self.turnparity = self.game.turn % 2

						if self.turnparity == 0 and player == self.firstmove:
							self.error = self.game.makeMove(read, 'X')
						elif self.turnparity == 1 and player != self.firstmove:
							self.error = self.game.makeMove(read, 'O')
						else:
							self.error = 4



						if self.error == 0:
							self.out = self.game.display()
							self.passed = False
						elif self.error == 1:
							self.out = "Invalid input"
						elif self.error == 2:
							self.out = "Invalid move"
						elif self.error == 3:
							self.out = "Invalid move"
						elif self.error == 4:
							self.out = "Not your turn"

			return self.out






