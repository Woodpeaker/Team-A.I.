# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
import random
import string
import time
# import pyfiglet


def game_input():
	# WELCOMING THE PLAYER
	# welcome_message = pyfiglet.figlet_format("Let's Line' Em Up!")
	# print(welcome_message)

	# SETTING GAME PARAMETERS

	# n is the size of the board
	while True:
		try:
			n = int(input("What board size would you like? \nnote: must be a number between 3 and 10"))
			while n < 3 or n > 10:
				print("Invalid number. Please try again")
				n = int(input("\nWhat board size would you like? \n note: must be a number between 3 and 10"))
		except ValueError:
			print("Invalid. Please try again\n")
			continue
		else:
			print("\nThe board will be of size: " + str(n) + "\n")
			break

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
	while True:
		try:
			b = int(input("How many blocks would you like? \n note: must be a number between 0 and " + str(2*n)))
			while b < 0 or b > 2 * n:
				print("Invalid number. Please try again")
				b = int(input("\nHow many blocks would you like? \n note: must be a number between 0 and " + str(2*n)))
		except ValueError:
			print("Invalid. Please try again\n")
			continue
		else:
			print("\nThere will be " + str(b) + " block(s) \n")
			break

	# Initializing block positions
	print("Please choose coordinates for each of the blocks:\n")
	blocks = []
	while True:
		try:
			if b == 0:
				break
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
		except ValueError:
			print("Invalid. Please try again.\n")
			continue
		else:
			blocks += [(row, column)]
			print("\nYour block will be at coordinate " + "(" + str(row) + ", " + letters[column] + ")\n")
			break

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
	while True:
		try:
			s = int(input("What size would you like for the winning line-up? \n note: must be a number between 3 and " + str(n)))
			while s < 3 or s > n:
				print("Invalid number. Please try again")
				s = int(input(
					"\nWhat size would you like for the winning line-up? \n note: must be a number between 3 and " + str(n)))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			print("\nThe winning line-up will be of size " + str(s) + "\n")
			break

	# d1 and d2 are the maximum depth of the adversarial search for player 1 and player 2
	while True:
		try:
			d1 = int(input("What would you like the maximum depth of the adversarial search to be for Player 1?"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			print("\nThe maximum depth of the adversarial search for Player 1 will be: " + str(d1) + "\n")
			break

	while True:
		try:
			d2 = int(input("What would you like the maximum depth of the adversarial search to be for Player 2?"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			print("\nThe maximum depth of the adversarial search for Player 2 will be: " + str(d2) + "\n")
			break

	# t is the maximum allowed time for the program to return a move, in seconds
	while True:
		try:
			t = int(input("What would you like to set as the maximum allowed time (in seconds) for the AI to make a move?"))
			while t <= 0:
				print("Invalid input. Please try again")
				t = int(input("\nWhat would you like to set as the maximum allowed time (in seconds) for the AI to make a move?"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			print("\nThe maximum allowed time has been set to " + str(t) + " seconds\n")
			break

	# a1 and a2 are booleans values 0 or 1, used to force the use of either minimax (FALSE) or alphabeta (TRUE)
	# for player 1 and player 2
	while True:
		try:
			a1 = int(input("For Player 1:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
			while a1 < 0 or a1 > 1:
				print("Invalid choice. Please try again")
				a1 = int(input("\nFor Player 1:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			if not a1:
				print("\nPlayer 1 will use minimax\n")
				bool(a1)
			else:
				print("\nPlayer 1 will use alphabeta\n")
			break

	while True:
		try:
			a2 = int(input("For Player 2:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
			while a2 < 0 or a2 > 1:
				print("Invalid choice. Please try again")
				a2 = int(input("\nFor Player 2:\nType 0 if you would like to use minimax.\nType 1 if you would like to use alphabeta"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			if not a2:
				print("\nPlayer 1 will use minimax\n")
				bool(a2)
			else:
				print("\nPlayer 2 will use alphabeta\n")
			break

	# m1 and m2 are booleans values 0 or 1, used to select whether the player will be HUMAN or AI, for both player 1
	# and player 2
	while True:
		try:
			m1 = int(input("For Player 1:\nType 0 to select human.\nType 1 if you would like to select AI"))
			while m1 < 0 or m1 > 1:
				print("Invalid choice. Please try again")
				m1 = int(input("\nFor Player 1:\nType 0 if you would like to select human.\nType 1 if you would like to to select AI"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			if not m1:
				print("\nPlayer 1 will be human\n")
			else:
				print("\nPlayer 1 will be AI\n")
			break

	while True:
		try:
			m2 = int(input("For Player 2:\nType 0 to select human.\nType 1 if you would like to select AI"))
			while m2 < 0 or m2 > 1:
				print("Invalid choice. Please try again")
				m2 = int(input("\nFor Player 2:\nType 0 if you would like to select human.\nType 1 if you would like to to select AI"))
		except ValueError:
			print("Invalid. Please try again\n")
		else:
			if not m2:
				print("\nPlayer 2 will be human")
			else:
				print("\nPlayer 2 will be AI")
			break

	# Returning all the parameters
	return n, b, blocks, s, d1, d2, t, a1, a2, m1, m2

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	SIMPLE_HEURISTIC = 4
	COMPLICATED_HEURISTIC = 5
	def __init__(self, recommend = True, blocks=[], n=3):
		self.initialize_game(blocks=blocks, n=n)
		self.recommend = recommend

	def initialize_game(self, n=3, blocks=[]):
		self.current_state = [[0 for x in range(n)] for y in range(n)]
		for i in range(0, n):
			for j in range(0, n):
				if (j, i) in blocks:
					self.current_state[j][i] = "="
				else:
					self.current_state[j][i] = "."
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

	def is_valid(self, px, py, n=3):
		if px < 0 or px > n-1 or py < 0 or py > n-1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self, n=3, s=3):
		# Vertical win
		for i in range(0, n):
			for j in range(0, n-s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					winner = True
					for k in range(1, s):
						if self.current_state[j+k][i] != self.current_state[j][i]:
							winner = False
							break
					if winner:
						return self.current_state[j][i]
		# Horizontal win
		for i in range(0, n-s):
			for j in range(0, n):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					winner = True
					for k in range(1, s):
						if self.current_state[j][i+k] != self.current_state[j][i]:
							winner = False
							break
					if winner:
						return self.current_state[j][i]
		winner = True
		# Main diagonal win
		for i in range(0, n-s):
			for j in range(0, n-s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					for k in range(1, s):
						if self.current_state[j+k][i+k] != self.current_state[j][i]:
							winner = False
							break
					if winner:
						return self.current_state[j][i]
		# Second diagonal win
		for i in range(s, n):
			for j in range(0, n-s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					winner = True
					for k in range(1, s):
						if self.current_state[j+k][i-k] != self.current_state[j][i]:
							winner = False
							break
					if winner:
						return self.current_state[j][i]

		# Is whole board full?
		for i in range(0, n):
			for j in range(0, n):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self, file=None, n=3, s=3):
		self.result = self.is_end(n=n, s=s)
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

	def input_move(self, n=3):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py, n=n):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def simple_heuristic(self, n=3):
		hScore = 0
		for col in range(0, n):
			for row in range(0, n):
				if self.current_state[row][col] == 'X':
					hScore -= 8
				if row < n-1:
					if self.current_state[row + 1][col] == 'O' or self.current_state[row + 1][col] == '=':
						hScore += 1
				if col < n-1:
					if self.current_state[row][col + 1] == 'O' or self.current_state[row][col+1] == '=':
						hScore += 1
				if row > 0:
					if self.current_state[row - 1][col] == 'O' or self.current_state[row - 1][col] == '=':
						hScore += 1
				if col > 0:
					if self.current_state[row][col - 1] == 'O' or self.current_state[row][col-1] == '=':
						hScore += 1
				if col > 0 and row > 0:
					if self.current_state[row - 1][col - 1] == 'O' or self.current_state[row - 1][col-1] == '=':
						hScore += 1
				if col > 0 and row < n-1:
					if self.current_state[row + 1][col - 1] == 'O' or self.current_state[row + 1][col-1] == '=':
						hScore += 1
				if col < n-1 and row > 0:
					if self.current_state[row - 1][col + 1] == 'O' or self.current_state[row - 1][col+1] == '=':
						hScore += 1
				if col < n-1 and row < n-1:
					if self.current_state[row + 1][col + 1] == 'O' or self.current_state[row + 1][col+1] == '=':
						hScore += 1
		return hScore

	def complicated_heuristic(self, n=3, s=3):
		hScore = 0
		player=''
		# Vertical win
		for i in range(0, n):
			for j in range(0, n - s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					player = self.current_state[j][i]
					winner = True
					for k in range(1, s):
						if self.current_state[j + k][i] != self.current_state[j][i] and self.current_state[j + k][i] != '.':
							winner = False
							if player == 'X':
								hScore += 100
							else:
								hScore -= 10
							break
					if winner:
						if player == 'X':
							hScore -= 100
						else:
							hScore += 1000
		# Horizontal win
		for i in range(0, n - s):
			for j in range(0, n):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					player = self.current_state[j][i]
					winner = True
					for k in range(1, s):
						if self.current_state[j][i + k] != self.current_state[j][i] and self.current_state[j][i + k] != '.':
							winner = False
							if player == 'X':
								hScore += 100
							else:
								hScore -= 10
							break
					if winner:
						if player == 'X':
							hScore -= 100
						else:
							hScore += 1000
		winner = True
		# Main diagonal win
		for i in range(0, n - s):
			for j in range(0, n - s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					player = self.current_state[j][i]
					for k in range(1, s):
						if self.current_state[j + k][i + k] != self.current_state[j][i] and self.current_state[j + k][i + k] != '.':
							winner = False
							if player == 'X':
								hScore += 100
							else:
								hScore -= 10
							break
					if winner:
						if player == 'X':
							hScore -= 100
						else:
							hScore += 1000
		# Second diagonal win
		for i in range(s, n):
			for j in range(0, n - s):
				if self.current_state[j][i] != '.' and self.current_state[j][i] != "=":
					player = self.current_state[j][i]
					winner = True
					for k in range(1, s):
						if self.current_state[j + k][i - k] != self.current_state[j][i] and self.current_state[j + k][i - k] != '.':
							winner = False
							if player == 'X':
								hScore += 100
							else:
								hScore -= 10
							break
					if winner:
						if player == 'X':
							hScore -= 100
						else:
							hScore += 1000
		return hScore

	def minimax(self, max=False, maxDepth=None, depth=0, e=None, count=0,depthArray={}, recursionCount=0, totalRecDepth=0, n=3, s=3, start=0, t=None):
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
		# if e == self.SIMPLE_HEURISTIC:
		# 	value = self.simple_heuristic()
		# elif e == self.COMPLICATED_HEURISTIC:
		# 	value = self.complicated_heuristic()
		x = None
		y = None
		result = self.is_end(n=n, s=s)
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
		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth or time.time() - start >= t:
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
							(v, _, _,c,d,rc,trd) = self.minimax(max=False, e=e, maxDepth=maxDepth, depth=depth+1, n=n, start=start, t=t)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == maxDepth or time.time() - start >= t:
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
							(v, _, _, c,d,rc,trd) = self.minimax(max=True, e=e, maxDepth=maxDepth, depth=depth + 1, n=n, start=start, t=t)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y, count,depthArray,recursionCount,totalRecDepth)

	def alphabeta(self, alpha=0, beta=100, max=False, maxDepth=None, depth=0, e=None, count=0, depthArray={}, recursionCount=0, totalRecDepth=0, n=3, s=3, start=0, t=None):
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
		result = self.is_end(n=n, s=s)
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
		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth or time.time() - start >= t:
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
							(v, _, _, c, d, rc, trd) = self.alphabeta(max=False, e=e, maxDepth=maxDepth, depth=depth + 1, n=n, start=start, t=t)
							recursionCount += rc
							totalRecDepth += trd
							count += c
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == maxDepth or time.time() - start >= t:
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
							(v, _, _, c, d, rc, trd) = self.alphabeta(max=True, e=e, maxDepth=maxDepth, depth=depth + 1, n=n, start=start, t=t)
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

	def play(self,player_x=None,player_o=None,a1=False,a2=False,e1=None,e2=None,d1=None,d2=None,n=None,b=None,s=None,t=None, blocks=[]):
		self.initialize_game(n=n,blocks=blocks)
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
			winner = self.check_end(file=file, n=n, s=s)

			if winner:
				for key in totalDepthArray.keys():
					avgTotaldepth += key * totalDepthArray[key]
				if totalEval == 0:
					totalEval = 1
				avgTotaldepth /= totalEval
				totalAvgRecDepth /=moveCounter
				file.write(F'6(b)i\tAverage evaluation time: {totalTime}s\n')
				file.write(F'6(b)ii\tTotal heuristic evaluations: {totalEval}\n')
				file.write(F'6(b)iii\tEvaluations by depth: {totalDepthArray}\n')
				file.write(F'6(b)iv\tAverage evaluation depth: {round(avgTotaldepth,1)}\n')
				file.write(F'6(b)v\tAverage recursion depth: {round(totalAvgRecDepth,1)}\n')
				file.write(F'6(b)vi\tTotal moves: {moveCounter}\n')
				return (winner, totalTime, totalEval, totalDepthArray, avgTotaldepth, totalAvgRecDepth, moveCounter)
			avgDepth = 0
			start = time.time()
			if self.player_turn == 'X':
				if a1:
					(_, x, y,nbEval,depthArray,recCount,TotalRecDepth)  = self.alphabeta(max=False,e=e1,maxDepth=d1, n=n, s=s, start=start, t=t)
				else:
					(_, x, y,nbEval,depthArray,recCount,TotalRecDepth) = self.minimax(max=False,e=e1,maxDepth=d1, n=n, s=s, start=start, t=t)
				print(f'h(n) = {_}')
			else:
				if a2:
					(m, x, y,nbEval,depthArray,recCount,TotalRecDepth)  = self.alphabeta(max=False,e=e2,maxDepth=d2, n=n, s=s, start=start, t=t)
				else:
					(m, x, y,nbEval,depthArray,recCount,TotalRecDepth) = self.minimax(max=True,e=e2,maxDepth=d2, n=n, s=s, start=start, t=t)
				print(f'h(n) = {m}')
			if x == None or y == None:
				x=0
				y=0
				for i in range(0, n):
					for j in range(0, n):
						if self.current_state[i][j] == '.':
							x = i
							y = j
							break
					if self.current_state[x][y] == '.':
						break
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
					(x,y) = self.input_move(n=n)
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

	def scoreboard(self, r =4,a1=False,a2=False,d1=4,d2=4,n=3,b=0,s=3,t=2,blocks=[]):
		g = Game(recommend=True, blocks=blocks, n=n)
		fileStr=F'scoreboard.txt'
		file = open(fileStr, 'a')
		file.write(F'n = {n}, b = {b}, s = {s}, t = {t}\n')
		file.write(F'PLayer 1: d= {d1} a={a1}\n')
		file.write(F'PLayer 2: d= {d2} a={a2}\n')
		totalgames= 2*r
		file.write('\n')
		file.write(F'{totalgames} games\n')
		file.write('\n')
		e1Wins=0
		e2Wins=0

		totalTimeLoop= 0
		totalEvalLoop= 0
		totalDepthArrayLoop = {}
		avgTotalDepthLoop = 0
		totalAvgRecDepthLoop =0
		moveCounterLoop= 0


		for x in range (0,r):
			(winner, totalTime, totalEval, totalDepthArray, avgTotaldepth, totalAvgRecDepth, moveCounter) = self.play(player_x=Game.AI,player_o=Game.AI,a1=a1,a2=a2,e1=g.SIMPLE_HEURISTIC,e2=g.COMPLICATED_HEURISTIC, blocks=blocks, d1=d1,d2=d2,n=n,b=b,s=s,t=t)
			if winner == 'X':
				e1Wins+=1
			elif winner== 'O':
				e2Wins+=1
			totalTimeLoop+=totalTime
			totalEvalLoop+=totalEval

			for key in totalDepthArray.keys():
				if key in totalDepthArrayLoop:
					totalDepthArrayLoop[key] += totalDepthArray[key]
				else:
					totalDepthArrayLoop[key] = totalDepthArray[key]

			totalDepthArray.clear()
			avgTotalDepthLoop+=avgTotaldepth
			totalAvgRecDepthLoop+=totalAvgRecDepth
			moveCounterLoop+=moveCounter


		for x in range (0,r):
			(winner, totalTime, totalEval, totalDepthArray, avgTotaldepth, totalAvgRecDepth, moveCounter) = self.play(player_x=Game.AI,player_o=Game.AI,a1=a2,a2=a1,e1=g.COMPLICATED_HEURISTIC,e2=g.SIMPLE_HEURISTIC,blocks=blocks, d1=d2,d2=d1,n=n,b=b,s=s,t=t)
			if winner == 'X':
				e2Wins+=1
			elif winner== 'O':
				e1Wins+=1
			totalTimeLoop += totalTime
			totalEvalLoop += totalEval

			for key in totalDepthArray.keys():
				if key in totalDepthArrayLoop:
					totalDepthArrayLoop[key] += totalDepthArray[key]
				else:
					totalDepthArrayLoop[key] = totalDepthArray[key]
			totalDepthArray.clear()
			avgTotalDepthLoop += avgTotaldepth
			totalAvgRecDepthLoop += totalAvgRecDepth
			moveCounterLoop += moveCounter

		percentageE1= e1Wins/totalgames
		percentageE2= e2Wins/totalgames

		file.write('\n')
		file.write(F'Total wins for heuristic e1: {e1Wins} ({percentageE1*100}%) (Simple Heuristic)\n')
		file.write(F'Total wins for heuristic e2: {e2Wins} ({percentageE2*100}%) (Complicated Heuristic)\n')
		file.write('\n')

		file.write(F'i   Average evaluation time: {totalTimeLoop/totalgames}\n')
		file.write(F'ii  Total heuristic evaluations: {totalEvalLoop/totalgames}\n')
		file.write(F'iii Evaluations by depth: {totalDepthArrayLoop}\n')
		file.write(F'iv Average evaluation depth: {avgTotalDepthLoop/totalgames}\n')
		file.write(F'v  Average recursion depth: {totalAvgRecDepthLoop/totalgames}\n')
		file.write(F'vi   Average moves per game: {moveCounterLoop/totalgames}\n')
		file.write(F'------------------------------------------------------------------------------------\n')

def blockGenerator(b=3,n=3):
	blocks =[]
	for i in range(0,b):
		valid = False
		while not valid:
			coord=[(random.randint(0,n-1),random.randint(0,n-1))]
			if coord not in blocks:
				blocks += coord
				valid = True
	return blocks


def main():
	n, b, blocks, s, d1, d2, t, a1, a2, m1, m2 = game_input()
	if m1:
		p1 = Game.AI
	else:
		p1 = Game.HUMAN
	if m2:
		p2 = Game.AI
	else:
		p2 = Game.HUMAN
	g = Game(recommend=True, blocks=blocks, n=n)
	g.play(player_x=p1, player_o=p2, a1=a1,  a2=a2, d1=d1, d2=d2, e1=Game.SIMPLE_HEURISTIC, e2=Game.SIMPLE_HEURISTIC, n=n, b=b, s=s, t=t, blocks=blocks)
	# g.scoreboard(r =7,a1=True,a2=False,d1=4,d2=4,n=3,b=0,s=3,t=2)

	# 2.6 Experiments and Analysis
	# 1
	g = Game(recommend=True, blocks=[(0, 0), (0, 3), (3, 0), (3, 3)], n=4)
	g.scoreboard(r=10,a1=False, a2=False,blocks=[(0,0),(0,3),(3,0),(3,3)], d1=6, d2=6,  n=4, b=4, s=3, t=5)
	# 2
	g = Game(recommend=True, blocks=[(0,0),(0,3),(3,0),(3,3)], n=4)
	g.scoreboard(r=10, blocks=[(0,0),(0,3),(3,0),(3,3)], a1=True, a2=True, d1=6, d2=6, n=4, b=4, s=3, t=1)
	# 3
	blocks=blockGenerator(b=4,n=5)
	g = Game(recommend=True, blocks=blocks, n=5)
	g.scoreboard(r=10, blocks=blocks, a1=True, a2=True, d1=2, d2=6,  n=5, b=4, s=4, t=1)
	# 4
	blocks = blockGenerator(b=4, n=5)
	g = Game(recommend=True,blocks=blocks, n=5)
	g.scoreboard(r=10, blocks=blocks, a1=True, a2=True, d1=6, d2=6, n=5, b=4, s=4, t=5)
	# 5
	blocks = blockGenerator(b=5, n=8)
	g = Game(recommend=True, blocks=blocks, n=8)
	g.scoreboard(r=10,blocks=blocks, a1=True, a2=True, d1=2, d2=6,n=8, b=5, s=5, t=1)
	# 6
	blocks = blockGenerator(b=5, n=8)
	g = Game(recommend=True, blocks=blocks, n=8)
	g.scoreboard(r=10,blocks=blocks,a1=True, a2=True, d1=2, d2=6, n=8, b=5, s=5, t=5)
	# 7
	blocks = blockGenerator(b=6, n=8)
	g = Game(recommend=True, blocks=blocks, n=8)
	g.scoreboard(r=10, blocks=blocks, a1=True, a2=True, d1=6, d2=6, n=8, b=6, s=5, t=1)
	# 8
	blocks = blockGenerator(b=6, n=8)
	g = Game(recommend=True, blocks=blocks, n=8)
	g.scoreboard(r=10, blocks=blocks,a1=True, a2=True, d1=6, d2=6,  n=8, b=6, s=5, t=5)



if __name__ == "__main__":
	main()

