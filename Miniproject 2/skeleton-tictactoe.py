# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
import string
import time

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

	def draw_board(self,n=3,file=open("gameTraceJunk.txt",'w')):
		letters = list(string.ascii_uppercase)
		print()
		for y in range(0, 3):
			for x in range(0, 3):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		if not file.closed:
			file.write('\n  ')
			for i in range(0, 3):
				file.write(letters[i])
			file.write('\n +')
			for i in range(0, 3):
				file.write('-')
			file.write('\n')
			for i in range(0, 3):
				file.write(str(i)+'|')
				for j in range(0, 3):
					file.write(F'{self.current_state[i][j]}')
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

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
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
		for row in range(0, 3):
			for col in range(0, 3):
				if self.current_state[row][col] == '0':
					hScore += 1
				if row < 2:
					if self.current_state[row + 1][col] == 'X':
						hScore += 2
				if col < 2:
					if self.current_state[row][col + 1] == 'X':
						hScore += 2
				if row > 0:
					if self.current_state[row - 1][col] == 'X':
						hScore += 2
				if col > 0:
					if self.current_state[row][col - 1] == 'X':
						hScore += 2
		return hScore

	def complicated_heuristic(self):
		hScore = 0
		for row in range(0, 3):
			for col in range(0, 3):
				if self.current_state[row][col] == '0':
					hScore += 1
				if row < 2:
					if self.current_state[row + 1][col] == 'X':
						hScore += 2
				if col < 2:
					if self.current_state[row][col + 1] == 'X':
						hScore += 2
				if row > 0:
					if self.current_state[row - 1][col] == 'X':
						hScore += 2
				if col > 0:
					if self.current_state[row][col - 1] == 'X':
						hScore += 2
		return hScore

	def minimax(self, max=False,maxDepth=4,depth=0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 100
		if max:
			value = 0
		x = None
		y = None
		if depth == maxDepth:
			value = self.simple_heuristic()
		else:
			result = self.is_end()
			if result == 'X':
				return (-1, x, y)
			elif result == 'O':
				return (1, x, y)
			elif result == '.':
				return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth:
							value = self.simple_heuristic()
							x = i
							y = j
							self.current_state[i][j] = '.'
							return (value, x, y)
						else:
							(v, _, _) = self.minimax(max=False,depth=depth+1)
							if v > value:
								value = v
								x = i
								y = j
					else:
						self.current_state[i][j] = 'X'
						if depth == maxDepth:
							value = self.simple_heuristic()
							x = i
							y = j
							self.current_state[i][j] = '.'
							return (value, x, y)
						else:
							(v, _, _) = self.minimax(max=True,depth=depth+1)
							if v < value:
								value = v
								x = i
								y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None,e1=None,e2=None,depth=None,n=3,b=0,s=3,t=2):
		fileStr=F'gameTrace-{n}{b}{s}{t}.txt'
		letters = list(string.ascii_uppercase)
		file = open(fileStr, 'w')
		file.write(F'n = {n}, b = {b}, s = {s}, t = {t}\n')
		file.write(F'TODO: Position of the blocks (Show array of coordinate)\n')
		file.write('PLayer 1: ')
		if player_x == self.AI:
			file.write('AI ')
		else:
			file.write('Human ')
		file.write(F'd = {depth} ')
		if algo == self.MINIMAX:
			file.write(F'a = MINMAX ')
		else:
			file.write(F'a = ALPHABETA ')
		if e1 == self.SIMPLE_HEURISTIC:
			file.write(F'e1 = SIMPLE_HEURISTIC\n')
		else:
			file.write(F'e1 = COMPLICATED_HEURISTIC\n')
		file.write('PLayer 2: ')
		if player_o == self.AI:
			file.write('AI ')
		else:
			file.write('Human ')
		file.write(F'(TODO: d = depth of search) ')
		file.write(F'(TODO: a = algo?) ')
		file.write(F'(TODO: e2 = heuristic?)\n')
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		moveCounter = 0
		while True:
			moveCounter += 1
			self.draw_board(n=n,file=file)
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
				print(f'h(n) = {_}')
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			if x == None or y == None:
				for i in range(0, 3):
					for j in range(0, 3):
						if self.current_state[i][j] == '.':
							x = i
							y = j
			end = time.time()
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
			file.write('TODO:Evaluation for (ii), (iii), (iv) and (v)\n\n')
			file.write(F'move {moveCounter}: \n')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI,depth=5,e1=Game.SIMPLE_HEURISTIC)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI,n=5,b=6,s=4,t=2)

if __name__ == "__main__":
	main()

