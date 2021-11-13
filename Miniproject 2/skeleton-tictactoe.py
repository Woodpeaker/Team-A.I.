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

	def draw_board(self,n=3,file=None):
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

	def minimax(self, max=False,maxDepth=None,depth=0,e=None,count=0,depthArray={}):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
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
			count += 1
			return (value,x,y,count)
		elif  result != None and e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
			count += 1
			return (value, x, y, count)
		elif result == 'X':
			return (-1, x, y,0)
		elif result == 'O':
			return (1, x, y,0)
		elif result == '.':
			return (0, x, y,0)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								count += 1
						else:
							(v, _, _,c) = self.minimax(max=False,e=e,maxDepth=maxDepth,depth=depth+1)
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
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								count += 1
						else:
							(v, _, _, c) = self.minimax(max=True, e=e, maxDepth=maxDepth, depth=depth + 1)
							count += c
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y, count)

	def alphabeta(self, alpha=-2, beta=2, max=False,maxDepth=None,depth=0,e=None,count=0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
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
			count += 1
			return (value, x, y, count)
		elif result != None and e == self.COMPLICATED_HEURISTIC:
			value = self.complicated_heuristic()
			count += 1
			return (value, x, y, count)
		elif result == 'X':
			return (-1, x, y, 0)
		elif result == 'O':
			return (1, x, y, 0)
		elif result == '.':
			return (0, x, y, 0)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if depth == maxDepth:
							if e == self.SIMPLE_HEURISTIC:
								v = self.simple_heuristic()
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								count += 1
						else:
							(v, _, _, c) = self.alphabeta(max=False, e=e, maxDepth=maxDepth, depth=depth + 1)
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
								count += 1
							elif e == self.COMPLICATED_HEURISTIC:
								v = self.complicated_heuristic()
								count += 1
						else:
							(v, _, _, c) = self.alphabeta(max=True, e=e, maxDepth=maxDepth, depth=depth + 1)
							count += c
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y,count)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y,count)
						if value < beta:
							beta = value
		return (value, x, y,count)

	def play(self,algo=None,player_x=None,player_o=None,e1=None,e2=None,depth=None,n=3,b=0,s=3,t=2):
		fileStr=F'gameTrace-{n}{b}{s}{t}.txt'
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
		elif e1 == self.COMPLICATED_HEURISTIC:
			file.write(F'e1 = COMPLICATED_HEURISTIC\n')
		else:
			file.write(F'e1 = None\n')
		file.write('PLayer 2: ')
		if player_o == self.AI:
			file.write('AI ')
		else:
			file.write('Human ')
		file.write(F'd = {depth} ')
		if algo == self.MINIMAX:
			file.write(F'a = MINMAX ')
		else:
			file.write(F'a = ALPHABETA ')
		if e2 == self.SIMPLE_HEURISTIC:
			file.write(F'e2 = SIMPLE_HEURISTIC\n')
		elif e2 == self.COMPLICATED_HEURISTIC:
			file.write(F'e2 = COMPLICATED_HEURISTIC\n')
		else:
			file.write(F'e2 = None\n')
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		moveCounter = 0
		totalTime=0
		totalEval=0
		while True:
			moveCounter += 1
			self.draw_board(n=n,file=file)
			if self.check_end(file=file):
				file.write(F'6(b)i\tAverage evaluation time: {totalTime}s\n')
				file.write(F'6(b)ii\tTotal heuristic evaluations: {totalEval}\n')
				file.write(F'6(b)iii\tEvaluations by depth: {None}\n')
				file.write(F'6(b)iv\tAverage evaluation depth: {None}\n')
				file.write(F'6(b)v\tAverage recursion depth: {None}\n')
				file.write(F'6(b)vi\tTotal moves: {moveCounter}\n')
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y,nbEval) = self.minimax(max=False,e=e1,maxDepth=4)
				else:
					(_, x, y,nbEval) = self.minimax(max=True,e=e2,maxDepth=4)
				print(f'h(n) = {_}')
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y,nbEval) = self.alphabeta(max=False,e=e1,maxDepth=4)
				else:
					(m, x, y,nbEval) = self.alphabeta(max=True,e=e2,maxDepth=4)
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
			file.write(F'ii\tNumber of evaluated states {nbEval}: \n')
			file.write('TODO:Evaluation for (iii), (iv) and (v)\n\n')
			file.write(F'move {moveCounter}: \n')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI,
		   depth=5,e1=Game.COMPLICATED_HEURISTIC,e2=Game.COMPLICATED_HEURISTIC)
	g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI,
		   depth=5, e1=Game.SIMPLE_HEURISTIC,e2=Game.SIMPLE_HEURISTIC,n=5, b=6, s=4, t=2)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI,n=5,b=6,s=4,t=2)


if __name__ == "__main__":
	main()

