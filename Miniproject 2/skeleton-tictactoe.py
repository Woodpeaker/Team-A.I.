# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
import string
import time
import pyfiglet

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	SIMPLE_HEURISTIC = 4
	COMPLICATED_HEURISTIC = 5
	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend

	def initialize_game(self):
		self.current_state = [['.','.','.'],
							  ['.','.','.'],
							  ['.','.','.']]
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self, n=3, blocks=[], file=None):
		letters = list(string.ascii_uppercase)
		print()
		print('\n  ', end="")
		for i in range(0, n):
			print(letters[i], end="")
		print('\n +', end="")
		for i in range(0, n):
			print('-', end="")
		print('\n')
		for i in range(0, n):
			print(str(i) + '|', end="")
			for j in range(0, n):
				if (j, i) in blocks:
					print(F'=', end="")
				else:
					print(F'{self.current_state[j][i]}', end="")
			print('\n')
		if not file.closed:
			file.write('\n  ')
			for i in range(0, n):
				file.write(letters[i])
			file.write('\n +')
			for i in range(0, n):
				file.write('-')
			file.write('\n')
			for i in range(0, n):
				file.write(str(i)+'|')
				for j in range(0, n):
					if (j, i) in blocks:
						file.write(F'=')
					else:
						file.write(F'{self.current_state[j][i]}')
				file.write('\n')
			file.write('\n')

	def is_valid(self, px, py):
		if px < 0 or px > 2 or py < 0 or py > 2:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		for i in range(0, 3):
			if (self.current_state[0][i] != '.' and
				self.current_state[0][i] == self.current_state[1][i] and
				self.current_state[1][i] == self.current_state[2][i]):
				return self.current_state[0][i]
		# Horizontal win
		for i in range(0, 3):
			if (self.current_state[i] == ['X', 'X', 'X']):
				return 'X'
			elif (self.current_state[i] == ['O', 'O', 'O']):
				return 'O'
		# Main diagonal win
		if (self.current_state[0][0] != '.' and
			self.current_state[0][0] == self.current_state[1][1] and
			self.current_state[0][0] == self.current_state[2][2]):
			return self.current_state[0][0]
		# Second diagonal win
		if (self.current_state[0][2] != '.' and
			self.current_state[0][2] == self.current_state[1][1] and
			self.current_state[0][2] == self.current_state[2][0]):
			return self.current_state[0][2]
		# Is whole board full?
		for i in range(0, 3):
			for j in range(0, 3):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self, file=None):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
				file.write('The winner is X!\n')
			elif self.result == 'O':
				print('The winner is O!')
				file.write('The winner is O!\n')
			elif self.result == '.':
				print("It's a tie!")
				file.write("It's a tie!\n\n")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def simple_heuristic(self):
		hScore = 0
		for col in range(0, 3):
			for row in range(0, 3):
				if self.current_state[row][col] == 'X':
					hScore += 1
				if row < 2:
					if self.current_state[row + 1][col] == 'O':
						hScore += 2
				if col < 2:
					if self.current_state[row][col + 1] == 'O':
						hScore += 2
				if row > 0:
					if self.current_state[row - 1][col] == 'O':
						hScore += 2
				if col > 0:
					if self.current_state[row][col - 1] == 'O':
						hScore += 2
				if col > 0 and row > 0:
					if self.current_state[row - 1][col - 1] == 'O':
						hScore += 2
				if col > 0 and row < 2:
					if self.current_state[row + 1][col - 1] == 'O':
						hScore += 2
				if col < 2 and row > 0:
					if self.current_state[row - 1][col + 1] == 'O':
						hScore += 2
				if col < 2 and row < 2:
					if self.current_state[row + 1][col + 1] == 'O':
						hScore += 2
		return hScore

	def complicated_heuristic(self):
		hScore = 0
		# Vertical win
		for i in range(0, 3):
			if (self.current_state[0][i] != 'O' and
					self.current_state[1][i] != 'O' and
					self.current_state[2][i] != 'O'):
				hScore += 100
			else:
				hScore -= 50
		# Horizontal win
		for i in range(0, 3):
			if (self.current_state[i][0] != 'O' and
					self.current_state[i][1] != 'O' and
					self.current_state[i][2] != 'O'):
				hScore += 100
			else:
				hScore -= 50
		# Main diagonal win
		if (self.current_state[0][0] != 'O' and
				self.current_state[1][1] != 'O' and
				self.current_state[2][2] != 'O'):
			hScore += 100
		else:
			hScore -= 50
		# Second diagonal win
		if (self.current_state[0][2] != 'O' and
				self.current_state[1][1] == 'O' and
				self.current_state[2][0] == 'O'):
			hScore += 100
		else:
			hScore -= 50
		return hScore

	def minimax(self, max=False,maxDepth=None,depth=0,e=None,count=0,depthArray={},recursionCount=0,totalRecDepth=0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		if depth != 0:
			recursionCount += 1
			totalRecDepth += depth
		value = 2
		if max:
			value = -2
		if e == self.SIMPLE_HEURISTIC:
			value = self.simple_heuristic()
		elif e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
		x = None
		y = None
		result = self.is_end()
		if result != None and e == self.SIMPLE_HEURISTIC:
			value = self.simple_heuristic()
			if depth in depthArray:
				depthArray[depth] += 1
			else:
				depthArray[depth] = 1
			count = 1
			return (value,x,y,count,depthArray,recursionCount,totalRecDepth)
		elif  result != None and e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
			if depth in depthArray:
				depthArray[depth] += 1
			else:
				depthArray[depth] = 1
			count = 1
			return (value, x, y, count,depthArray,recursionCount,totalRecDepth)
		elif result == 'X':
			return (-1, x, y,count,depthArray,recursionCount,totalRecDepth)
		elif result == 'O':
			return (1, x, y,count,depthArray,recursionCount,totalRecDepth)
		elif result == '.':
			return (0, x, y,count,depthArray,recursionCount,totalRecDepth)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
						else:
							(v, _, _,c,d,rc,trd) = self.minimax(max=False,e=e,maxDepth=maxDepth,depth=depth+1)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
						else:
							(v, _, _, c,d,rc,trd) = self.minimax(max=True, e=e, maxDepth=maxDepth, depth=depth + 1)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y, count,depthArray,recursionCount,totalRecDepth)

	def alphabeta(self, alpha=-2, beta=2, max=False,maxDepth=None,depth=0,e=None,count=0,depthArray={},recursionCount=0,totalRecDepth=0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		if depth != 0:
			recursionCount += 1
			totalRecDepth += depth
		value = 2
		if max:
			value = -2
		if e == self.SIMPLE_HEURISTIC:
			value = self.simple_heuristic()
		elif e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
		x = None
		y = None
		result = self.is_end()
		if result != None and e == self.SIMPLE_HEURISTIC:
			value = self.simple_heuristic()
			if depth in depthArray:
				depthArray[depth] += 1
			else:
				depthArray[depth] = 1
			count = 1
			return (value, x, y, count, depthArray, recursionCount, totalRecDepth)
		elif result != None and e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
			if depth in depthArray:
				depthArray[depth] += 1
			else:
				depthArray[depth] = 1
			count = 1
			return (value, x, y, count, depthArray, recursionCount, totalRecDepth)
		elif result == 'X':
			return (-1, x, y, count, depthArray, recursionCount, totalRecDepth)
		elif result == 'O':
			return (1, x, y, count, depthArray, recursionCount, totalRecDepth)
		elif result == '.':
			return (0, x, y, count, depthArray, recursionCount, totalRecDepth)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
						else:
							(v, _, _, c, d, rc, trd) = self.alphabeta(max=False, e=e, maxDepth=maxDepth, depth=depth + 1)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								if depth in depthArray:
									depthArray[depth] += 1
								else:
									depthArray[depth] = 1
								count += 1
						else:
							(v, _, _, c, d, rc, trd) = self.alphabeta(max=True, e=e, maxDepth=maxDepth, depth=depth + 1)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max:
						if value >= beta:
							return (value, x, y, count,depthArray,recursionCount,totalRecDepth)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y, count,depthArray,recursionCount,totalRecDepth)
						if value < beta:
							beta = value
		return (value, x, y, count,depthArray,recursionCount,totalRecDepth)

	def game_input(self):
		# WELCOMING THE PLAYER
		welcome_message = pyfiglet.figlet_format("Let's Line' Em Up!")
		print(welcome_message)

		# SETTING GAME PARAMETERS

		# n is the size of the board
		n = int(input("What board size would you like? \nnote: must be a number between 3 and 10"))

		while n < 3 or n > 10:
			print("Invalid number. Please try again")
			n = int(input("\nWhat board size would you like? \n note: must be a number between 3 and 10"))
		else:
			print("\nThe board will be of size: " + str(n) + "\n")

		# Show the board to the player
		letters = list(string.ascii_uppercase)
		print('\n  ', end="")
		for i in range(0, n):
			print(letters[i], end="")
		print('\n +', end="")
		for i in range(0, n):
			print('-', end="")
		print('\n')
		for i in range(0, n):
			print(str(i) + '|', end="")
			for j in range(0, n):
				print(F'.', end="")
			print('\n')

		# b is the number of blocks
		b = int(input("How many blocks would you like? \n note: must be a number between 0 and " + str(2*n)))
		while b < 0 or b > 2 * n:
			print("Invalid number. Please try again")
			b = int(input("\nHow many blocks would you like? \n note: must be a number between 0 and " + str(2*n)))
		else:
			print("\nThere will be " + str(b) + " block(s) \n")

		# Initializing block positions
		print("Please choose coordinates for each of the blocks:\n")
		blocks = []
		for i in range(0, b):
			valid = False
			while not valid:
				row = int(input("Which row would you like block " + str(i) + " to be on?"))
				if row < 0 or row >= n:
					print("Invalid row choice. Please try again")
					row = int(input("\nWhich row would you like block " + str(i) + " to be on?"))
				column = int(input("Which column would you like your block to be on?"))
				if column < 0 or column >= n:
					print("Invalid column choice. Please try again")
					column = int(input("\nWhich column would you like your block to be on?"))
				if (row, column) not in blocks:
					valid = True
				else:
					print("\nInvalid coordinates. Please try again\n")
			blocks += [(row, column)]
			print("\nYour block will be at coordinate " + "(" + str(row) + ", " + letters[column] + ")\n")

		# Show the board with the blocks to the player
		print('\n  ', end="")
		for i in range(0, n):
			print(letters[i], end="")
		print('\n +', end="")
		for i in range(0, n):
			print('-', end="")
		print('\n')
		for i in range(0, n):
			print(str(i) + '|', end="")
			for j in range(0, n):
				if (j, i) in blocks:
					print(F'=', end="")
				else:
					print(F'.', end="")
			print('\n')

		# s is the winning line-up size
		s = int(input("What size would you like for the winning line-up? \n note: must be a number between 3 and " + str(n)))
		while s < 3 or s > n:
			print("Invalid number. Please try again")
			s = int(input(
				"\nWhat size would you like for the winning line-up? \n note: must be a number between 3 and " + str(n)))
		else:
			print("\nThe winning line-up will be of size " + str(s) + "\n")

		# d1 and d2 are the maximum depth of the adversarial search for player 1 and player 2
		d1 = int(input("What would you like the maximum depth of the adversarial search to be for Player 1?"))
		print("\nThe maximum depth of the adversarial search for Player 1 will be: " + str(d1) + "\n")

		d2 = int(input("What would you like the maximum depth of the adversarial search to be for Player 2?"))
		print("\nThe maximum depth of the adversarial search for Player 2 will be: " + str(d2) + "\n")

		# t is the maximum allowed time for the program to return a move, in seconds
		t = int(input("What would you like to set as the maximum allowed time (in seconds) for the AI to make a move?"))
		while t <= 0:
			print("Invalid input. Please try again")
			t = int(input("\nWhat would you like to set as the maximum allowed time (in seconds) for the AI to make a move?"))
		else:
			print("\nThe maximum allowed time has been set to " + str(t) + " seconds\n")

		# a1 and a2 are booleans values 0 or 1, used to force the use of either minimax (FALSE) or alphabeta (TRUE)
		# for player 1 and player 2
		a1 = int(input("For Player 1:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		while a1 < 0 or a1 > 1:
			print("Invalid choice. Please try again")
			a1 = int(input("\nFor Player 1:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		if not a1:
			print("\nPlayer 1 will use minimax\n")
			bool(a1)
		else:
			print("\nPlayer 1 will use alphabeta\n")

		a2 = int(input("For Player 2:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		while a2 < 0 or a2 > 1:
			print("Invalid choice. Please try again")
			a2 = int(input("\nFor Player 2:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		if not a2:
			print("\nPlayer 2 will use minimax\n")
		else:
			print("\nPlayer 2 will use alphabeta\n")

		# m1 and m2 are booleans values 0 or 1, used to select whether the player will be HUMAN or AI, for both player 1
		# and player 2
		m1 = int(input("For Player 1:\nType 0 to select human.\nType 1 if you would like to select AI"))
		while m1 < 0 or m1 > 1:
			print("Invalid choice. Please try again")
			m1 = int(input("\nFor Player 1:\nType 0 if you would like to select human.\nType 1 if you would like to to select AI"))
		if not m1:
			print("\nPlayer 1 will be human\n")
		else:
			print("\nPlayer 1 will be AI\n")

		m2 = int(input("For Player 2:\nType 0 to select human.\nType 1 if you would like to select AI"))
		while m2 < 0 or m2 > 1:
			print("Invalid choice. Please try again")
			m2 = int(input("\nFor Player 2:\nType 0 if you would like to select human.\nType 1 if you would like to to select AI"))
		if not m2:
			print("\nPlayer 2 will be human")
		else:
			print("\nPlayer 2 will be AI")

		# Returning all the parameters
		return n, b, blocks, s, d1, d2, t, a1, a2, m1, m2

	def play(self,player_x=None,player_o=None,a1=False,a2=False,e1=None,e2=None,d1=None,d2=None,n=None,b=None,s=None,t=None, blocks=[]):
		fileStr=F'gameTrace-{n}{b}{s}{t}.txt'
		file = open(fileStr, 'w')
		file.write(F'n = {n}, b = {b}, s = {s}, t = {t}\n')
		file.write(F'Position of the blocks: {blocks}\n')
		file.write('PLayer 1: ')
		if player_x == self.AI:
			file.write('AI ')
		else:
			file.write('Human ')
		file.write(F'd1 = {d1} ')
		if a1:
			file.write(F'a1 = ALPHABETA ')
		else:
			file.write(F'a1 = MINMAX ')
		if e1 == self.SIMPLE_HEURISTIC:
			file.write(F'e1 = SIMPLE_HEURISTIC\n')
		elif e1 == self.COMPLICATED_HEURISTIC:
			file.write(F'e1 = COMPLICATED_HEURISTIC\n')
		else:
			file.write(F'e1 = None\n')
		file.write('PLayer 2: ')
		if player_o == self.AI:
			file.write('AI ')
		else:
			file.write('Human ')
		file.write(F'd2 = {d2} ')
		if a2:
			file.write(F'a2 = ALPHABETA ')
		else:
			file.write(F'a2 = MINMAX ')
		if e2 == self.SIMPLE_HEURISTIC:
			file.write(F'e2 = SIMPLE_HEURISTIC\n')
		elif e2 == self.COMPLICATED_HEURISTIC:
			file.write(F'e2 = COMPLICATED_HEURISTIC\n')
		else:
			file.write(F'e2 = None\n')
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		moveCounter = 0
		totalTime=0
		totalEval=0
		totalDepthArray={}
		avgTotaldepth=0
		totalAvgRecDepth = 0
		while True:
			moveCounter += 1
			self.draw_board(n=n, blocks=blocks, file=file)
			if self.check_end(file=file):
				for key in totalDepthArray.keys():
					avgTotaldepth += key * totalDepthArray[key]
				avgTotaldepth /= totalEval
				totalAvgRecDepth /=moveCounter
				file.write(F'6(b)i\tAverage evaluation time: {totalTime}s\n')
				file.write(F'6(b)ii\tTotal heuristic evaluations: {totalEval}\n')
				file.write(F'6(b)iii\tEvaluations by depth: {totalDepthArray}\n')
				file.write(F'6(b)iv\tAverage evaluation depth: {round(avgTotaldepth,1)}\n')
				file.write(F'6(b)v\tAverage recursion depth: {round(totalAvgRecDepth,1)}\n')
				file.write(F'6(b)vi\tTotal moves: {moveCounter}\n')
				return
			avgDepth = 0
			start = time.time()
			if self.player_turn == 'X':
				if a1:
					(_, x, y,nbEval,depthArray,recCount,TotalRecDepth)  = self.alphabeta(max=False,e=e1,maxDepth=d1)
				else:
					(_, x, y,nbEval,depthArray,recCount,TotalRecDepth) = self.minimax(max=False,e=e1,maxDepth=d1)
				print(f'h(n) = {_}')
			else:
				if a2:
					(m, x, y,nbEval,depthArray,recCount,TotalRecDepth)  = self.alphabeta(max=False,e=e2,maxDepth=d2)
				else:
					(m, x, y,nbEval,depthArray,recCount,TotalRecDepth) = self.minimax(max=True,e=e2,maxDepth=d2)
				print(f'h(n) = {m}')
			if x == None or y == None:
				for i in range(0, 3):
					for j in range(0, 3):
						if self.current_state[i][j] == '.':
							x = i
							y = j
			end = time.time()
			totalTime += round(end - start, 7)
			totalTime = round(totalTime, 7)
			totalEval += nbEval
			for key in depthArray.keys():
				avgDepth += key* depthArray[key]
				if key in totalDepthArray:
					totalDepthArray[key] += depthArray[key]
				else:
					totalDepthArray[key] = depthArray[key]
			avgDepth /= nbEval
			avgRecDepth = TotalRecDepth/recCount
			totalAvgRecDepth += avgRecDepth
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			file.write(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}\n\n')
			file.write(F'i\tEvaluation time: {round(end - start, 7)}s\n')
			file.write(F'ii\tNumber of evaluated states: {nbEval}\n')
			file.write(F'iii\tEvaluations by depth: {depthArray}\n')
			file.write(F'iv\tAverage evaluation depth: {round(avgDepth,1)}\n')
			file.write(F'iv\tAverage recursion depth: {round(avgRecDepth,1)}\n\n')
			file.write(F'move {moveCounter}: \n')
			depthArray.clear()
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	n, b, blocks, s, d1, d2, t, a1, a2, m1, m2 = g.game_input()
	# This was for testing reason (It use default settings of a Tic-Tac-Toe game):
	g.play(player_x=Game.AI, player_o=Game.AI, a1=a1,  a2=a2, d1=d1, d2=d2, e1=Game.COMPLICATED_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=n, b=b, s=s, t=t, blocks=blocks)
	# 2.6 Experiments and Analysis (Uncomment when Input part is done)
	# 1
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=False, a2=False, d1=6, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=4, b=4, s=3, t=5)
	# # 2
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=6, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=4, b=4, s=3, t=1)
	# # 3
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=2, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=5, b=4, s=4, t=1)
	# # 4
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=6, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=5, b=4, s=4, t=5)
	# # 5
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=2, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=8, b=5, s=5, t=1)
	# # 6
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=2, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=8, b=5, s=5, t=5)
	# # 7
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=6, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=8, b=6, s=5, t=1)
	# # 8
	# g.play(player_x=Game.AI, player_o=Game.AI, a1=True, a2=True, d1=6, d2=6,
	# 	   e1=Game.SIMPLE_HEURISTIC, e2=Game.COMPLICATED_HEURISTIC, n=8, b=6, s=5, t=5)



if __name__ == "__main__":
	main()

