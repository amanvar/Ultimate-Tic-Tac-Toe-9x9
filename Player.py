'''
	TEAM 77
	Aman Varshney (201402188)
	Vinay Kumar Singh (201402035)
	IIIT-Hyderabad
'''
import random
import copy
import sys

class Player():

	def __init__(self):
		self.APPROXIMATE_WIN_SCORE = 7
		self.BIG_BOARD_WEIGHT = 23
		self.WIN_SCORE = 10**6
		self.ALPHA_BETA_DEPTH = 7
		self.POSSIBLE_WIN_SEQUENCES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		self.stored_score = [0]*8
		self.first = 0
		self.maxxx = 9223372036854775807

	MAXX = 9223372036854775807


	def move(self, state, temp_block, old_move, flag):
		#print flag
		self.first = 0
		if(old_move[0] == -1 and old_move[1] == -1):
			return (4,4)
		acts_res = []
		final_choices = []
		cells = []
		cells = self.get_legal_actions(state,temp_block,old_move,flag)

		if type(cells) == tuple:
			y = []
			y.append(cells)
			cells = y

		if(len(cells) == 1):
			return (cells[0][0], cells[0][1])

		if (len(cells) >= 2):
			self.ALPHA_BETA_DEPTH = 2
		elif (len(cells) >= 3):
			self.ALPHA_BETA_DEPTH = 3
		elif (len(cell) >= 4):
			self.ALPHA_BETA_DEPTH = 4
		elif (len(cell) >= 5):
			self.ALPHA_BETA_DEPTH = 5
		elif (len(cell) >= 6):
			self.ALPHA_BETA_DEPTH = 6
		else:
			self.ALPHA_BETA_DEPTH = 7

		for act in cells:
			successor_state = self.generate_successor(state, act, flag)
			acts_res.append((act, self.__min_val_ab(successor_state, self.ALPHA_BETA_DEPTH, temp_block, flag, old_move)))
		_, best_val = max(acts_res, key=lambda x: x[1])
		#return random.choice([best_action for best_action, val in acts_res if val == best_val])
		final_choices = [best_action for best_action, val in acts_res if val == best_val]
		i = final_choices[0]
		x = i[0] - (i[0]%3)
		y = i[1] - (i[1]%3)
		arr = []
		for j in [x,x+1,x+2]:
			for k in [y,y+1,y+2]:
				if state[j][k] == flag:
					arr.append(1)
				elif state[j][k] == self.op(flag):
					arr.append(-1)
				else:
					arr.append(0)
		loc = []
		for i in xrange(len(arr)):
			if arr[i] == 1:
				self.rtup(i,arr,x,y,loc)
		final_choices = list(set(loc).intersection(set(final_choices)))
		if len(final_choices) == 0:
			return random.choice([best_action for best_action, val in acts_res if val == best_val])
		return random.choice(final_choices)

	def rtup(self, i, arr, sx, sy, x):
		for j in self.POSSIBLE_WIN_SEQUENCES:
			if i in j:
				var = j.index(i)
				for k in xrange(len(j)):
					if k != var:
						if arr[k] == -1:
							break
						elif k == 2:
							for s in xrange(len(j)):
								if s != var:
									v1 = sx + (s/3)
									v2 = sy + (s%3)
									x.append((v1,v2))
		return

	def filter(self, temp_block, flag):
		for i in xrange(9):
			if temp_block[i] == flag:
				self.stored_score[i/3] += 1
				self.stored_score[(i%3) + 3] += 1
				if i == 0:
					self.stored_score[6] += 1
				elif i == 2:
					self.stored_score[7] += 1
				elif i == 4:
					self.stored_score[6] += 1
					self.stored_score[7] += 1
				elif i == 6:
					self.stored_score[7] += 1
				elif i == 8:
					self.stored_score[6] += 1
			elif temp_block[i] != '-':
				self.stored_score[i/3] = 0
				self.stored_score[(i%3) + 3] = 0
				if i == 0:
					self.stored_score[6] = 0
				elif i == 2:
					self.stored_score[7] = 0
				elif i == 4:
					self.stored_score[6] = 0
					self.stored_score[7] = 0
				elif i == 6:
					self.stored_score[7] = 0
				elif i == 8:
					self.stored_score[6] = 0


	def func(self, index, temp_block):

		if index == 6:
			for j in [0,4,8]:
				if temp_block[j] == '-':
					return j

		elif index == 7:
			for j in [6,0,2]:
				if temp_block[j] == '-':
					return j

		elif index == 1:
			for j in [4,5,3]:
				if temp_block[j] == '-':
					return j

		elif index == 4:
			for j in [4,7,1]:
				if temp_block[j] == '-':
					return j

		elif index == 0:
			for j in [0,1,2]:
				if temp_block[j] == '-':
					return j

		elif index == 2:
			for j in [8,7,6]:
				if temp_block[j] == '-':
					return j

		elif index == 3:
			for j in [6,3,0]:
				if temp_block[j] == '-':
					return j

		elif index == 5:
			for j in [2,5,8]:
				if temp_block[j] == '-':
					return j


	def select(self, blocks_allowed, temp_block):
		if len(blocks_allowed) == 0:
			check = [0, 1, 2, 3, 4, 5, 6, 7]
			check = list(reversed([x for (y,x) in sorted(zip(self.stored_score,check))]))
			for i in check:
				ret = self.func(i, temp_block)
				if ret != None:
					return ret

		elif len(blocks_allowed) == 1:
			return blocks_allowed[0]

		else:
			max_value = 0
			block = []
			for i in blocks_allowed:
				block.append(i/3)
				block.append((i%3)+3)
				if i == 0:
					block.append(6)
				elif i == 2:
					block.append(7)
				elif i == 4:
					block.append(6)
					block.append(7)
				elif i == 6:
					block.append(7)
				elif i == 8:
					block.append(6)

			index = block[0]
			block = list(set(block))
			for i in block:
				if self.stored_score[i] >= max_value:
					index = i
					max_value = self.stored_score[i]

			if index == 0:
				for j in list(set([1,0,2]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 1:
				for j in list(set([4,3,5]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 2:
				for j in list(set([7,6,8]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 3:
				for j in list(set([3,6,0]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 4:
				for j in list(set([4,1,7]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 5:
				for j in list(set([5,2,8]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 6:
				for j in list(set([4,8,0]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j

			elif index == 7:
				for j in list(set([4,2,6]).intersection(blocks_allowed)):
					if temp_block[j] == '-':
						return j


	def get_legal_actions(self,state,temp_block,old_move,flag):

		for_corner = [0,1,2,3,5,6,7,8]                                #*************Aman Start************
		blocks_allowed = []
		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [1,3]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
			blocks_allowed = [1,5]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
			blocks_allowed = [3,7]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
			blocks_allowed = [5,7]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
			blocks_allowed = [0,2]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
			blocks_allowed = [0,6]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
			blocks_allowed = [6,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
			blocks_allowed = [2,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
			blocks_allowed = [4]
		else:
			sys.exit(1)

		# blocks_allowed  = []
		#
		# if old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		# 		blocks_allowed = [4]
		# else:
		# 	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		# 		blocks_allowed = [1, 3]
		#
		# 	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		# 		blocks_allowed = [3, 7]
		#
		# 	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		# 		blocks_allowed = [0, 6]
		#
		# 	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		# 		blocks_allowed = [0, 2]
		#
		# 	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		# 		blocks_allowed = [1, 5]
		#
		# 	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		# 		blocks_allowed = [2, 8]
		#
 	# 		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		# 		blocks_allowed = [5, 7]
		#
		# 	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		# 		blocks_allowed = [6, 8]



		for i in reversed(blocks_allowed):
			if temp_block[i] != '-':
				blocks_allowed.remove(i)

		if self.first == 0:
			self.first = 1
			cells = []
			mv = []
			ball = copy.deepcopy(blocks_allowed)
			if len(ball) == 0:
				for i in xrange(9):
					if temp_block[i] == '-':
						ball.append(i)
			for i in ball:
				var = self.analyze(state,i,flag)
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in for_corner:
					return i
			if len(mv) != 0:
				return mv[0]
			mv = []
			for i in ball:
				var = self.analyze(state,i,self.op(flag))
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in for_corner:
					return i
			if len(mv) != 0:
				return mv[0]

		cells = []

		blocks_a = []
		self.stored_score = [0]*8
		self.filter(temp_block, flag)
		blocks_a.append(self.select(blocks_allowed, temp_block))
		cells = self.get_empty_of(state,blocks_a,temp_block)

		return cells

	def op(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def __min_val_ab(self,state, depth, temp_block, flag, old_move, alpha=-(MAXX), beta=(MAXX)):
		if self.terminal_test(state, depth, temp_block):
			return self.__eval_state(state, temp_block, flag)
		val = (self.maxxx)
		for act in self.get_legal_actions(state,temp_block,old_move,flag):
			successor_state = self.generate_successor(state, act, flag)
			val = min(val, self.__max_val_ab(successor_state,  depth - 1, temp_block, flag, old_move, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)
		return beta

	def __max_val_ab(self,state, depth, temp_block,flag, old_move, alpha=-(MAXX), beta=(MAXX)):
		if self.terminal_test(state, depth, temp_block):
			return self.__eval_state(state, temp_block, flag)
		val = -(self.maxxx)
		for act in self.get_legal_actions(state,temp_block,old_move,flag):
			successor_state = self.generate_successor(state, act, flag)
			val = max(val, self.__min_val_ab(successor_state, depth, temp_block, flag, old_move, alpha, beta))
			if val >= beta:
				return val
			alpha = max(alpha, val)
		return alpha

	def terminal_test(self,state, depth, temp_block):
		if depth==0:
			return True
		a,b =  self.terminal_state_reached(state, temp_block)
		return a

	def generate_successor(self, state, action, flag):
		brd = copy.deepcopy(state)
		brd[action[0]][action[1]] = flag
		return brd

	def __eval_state(self,state, temp_block, flag):
		uttt_board = copy.deepcopy(state)
		mini_board = copy.deepcopy(temp_block)

		if self.get_winner(temp_block) != False:
			free_cells = 0
			for i in xrange(9):
				for j in xrange(9):
					if uttt_board[i][j] == '-':
						free_cells += 1
			return self.WIN_SCORE + free_cells if self.get_winner(temp_block) == flag else -self.WIN_SCORE - free_cells

		if self.is_board_full(uttt_board):
			return 0

		board_as_mini = []
		for i in xrange(9):
			board_as_mini.append(temp_block[i])

		ret = self.__assess_miniB(board_as_mini, flag) * self.BIG_BOARD_WEIGHT
		for i in xrange(9):
			if temp_block[i] == '-':
				miniB = self.get_miniBoard(uttt_board,i)
				if '-' in miniB:
					ret += self.__assess_miniB(miniB, flag)
		return ret

	def __assess_miniB(self,miniB, flag):
		if '-' not in miniB:
			return 0
		player_counter = 0
		opponent_counter = 0
		player_str = flag
		opponent_str = self.op(flag)
		miniB_as_list = copy.deepcopy(miniB)
		for seq in self.POSSIBLE_WIN_SEQUENCES:
			filtered_seq = [miniB_as_list[index] for index in seq if miniB_as_list[index] != '-']
			if player_str in filtered_seq:
				if opponent_str in filtered_seq:
					continue
				if len(filtered_seq) > 1:
					player_counter += self.APPROXIMATE_WIN_SCORE
				player_counter += 1
			elif opponent_str in filtered_seq:
				if len(filtered_seq) > 1:
					opponent_counter += self.APPROXIMATE_WIN_SCORE
				opponent_counter += 1
		return player_counter - opponent_counter

	def get_winner(self, block):
		if block[0] == block[1] and block[1] == block[2] and block[1] != '-':
			return block[0]
		elif block[3] == block[4] and block[4] == block[5] and block[4] != '-':
			return block[3]
		elif block[6] == block[7] and block[7] == block[8] and block[7] != '-':
			return block[6]
		elif block[0] == block[3] and block[3] == block[6] and block[3] != '-':
			return block[0]
		elif block[1] == block[4] and block[4] == block[7] and block[4] != '-':
			return block[1]
		elif block[2] == block[5] and block[5] == block[8] and block[5] != '-':
			return block[2]
		elif block[0] == block[4] and block[4] == block[8] and block[4] != '-':
			return block[0]
		elif block[2] == block[4] and block[4] == block[6] and block[4] != '-':
			return block[2]
		else:
			return False

	def is_board_full(self,uttt_board):
		for i in xrange(9):
			if '-' in uttt_board[i]:
				return False
		return True

	def get_miniBoard(self,state,i):
		mini = []
		for x in xrange(3):
			for y in xrange(3):
				mini.append(state[i/3 + x][i%3 + y])
		return mini

	def get_empty_of(self, gameb, blal,block_stat):
		cells = []
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))
		return cells


	def terminal_state_reached(self,game_board, block_stat):

		bs = block_stat
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
			#print block_stat
			return True, 'W'

		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
			#print block_stat
			return True, 'W'

		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
			#print block_stat
			return True, 'W'

		else:
			smfl = 0
			for i in range(9):
				for j in range(9):
					if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
						smfl = 1
						break
			if smfl == 1:
				return False, 'Continue'

			else:
	                        point1 = 0
	                        point2 = 0
	                        for i in block_stat:
	                            if i == 'x':
	                                point1+=1
	                            elif i=='o':
	                                point2+=1
				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
				else:
	                                point1 = 0
	                                point2 = 0
	                                for i in range(len(game_board)):
	                                    for j in range(len(game_board[i])):
	                                        if i%3!=1 and j%3!=1:
	                                            if game_board[i][j] == 'x':
	                                                point1+=1
	                                            elif game_board[i][j]=='o':
	                                                point2+=1
				        if point1>point2:
					    return True, 'P1'
				        elif point2>point1:
					    return True, 'P2'
	                                else:
					    return True, 'D'

	def analyze(self, gameb, index, flag):
		id1 = index/3
		id2 = index%3
		tup = []
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return (i,(id2*3)+loc)
			tup = []
		for j in range(id2*3,id2*3+3):
			for i in range(id1*3,id1*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return ((id1*3)+loc,j)
			tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+loc)
		tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+2-i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+2-loc)
		return (-1,-1)

	def free(self, tup,flag):
		if tup[0] == tup[1] and tup[2] == '-' and tup[0] == flag:
			return 2
		elif tup[0] == tup[2] and tup[1] == '-' and tup[0] == flag:
			return 1
		elif tup[1] == tup[2] and tup[0] == '-' and tup[1] == flag:
			return 0
		else:
			return -1

'''

## Player77=O
## RandomPlayer=X

=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (3, 6) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 3) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (5, 1) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (6, 2) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - - -

- - o  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (5, 7) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- - o  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (6, 1) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (2, 0) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
x - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (8, 4) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
x - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  - - -  - - -
- - -  - - -  - - -
- - -  - o -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (8, 6) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
x - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  - - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (6, 3) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
x - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (1, 4) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - -
x - -  o - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (3, 4) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - -
x - -  o - -  - - -

- - -  - o -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (1, 8) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - x
x - -  o - -  - - -

- - -  - o -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 6) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - x
x - -  o - -  o - -

- - -  - o -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - -  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (6, 5) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - x
x - -  o - -  o - -

- - -  - o -  x - -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (3, 7) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - x -  - - x
x - -  o - -  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 0) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o - -  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 4) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o -  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - -
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (6, 8) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o -  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - x
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 5) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  - x -

- o o  o - x  - - x
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 1 made the move: (5, 6) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - - -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 2 made the move: (7, 4) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  - o -  x o -
- - -  - - -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - o -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 1 made the move: (4, 4) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  - o -  x o -
- - -  - x -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - o -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 2 made the move: (3, 3) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  o o -  x o -
- - -  - x -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - o -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 1 made the move: (4, 2) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - o -  - - -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 2 made the move: (7, 7) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  - - -  x x -

- o o  o - x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 1 made the move: (5, 3) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  x - -  x x -

- o o  o - x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- - -
==================================

Player 2 made the move: (6, 4) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x - -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  x - -  x x -

- o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- o -
==================================

Player 1 made the move: (2, 1) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  x - -  x x -

- o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
- o -
==================================

Player 2 made the move: (6, 0) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
- x -  x - -  x x -

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
o o -
==================================

Player 1 made the move: (5, 0) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
x x -  x - -  x x -

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
o o -
==================================

Player 2 made the move: (5, 2) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o -
- - x  - x -  - - -
x x o  x - -  x x -

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
o o -
==================================

Player 1 made the move: (3, 8) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o x
- - x  - x -  - - -
x x o  x - -  x x -

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
o o -
==================================

Player 2 made the move: (5, 8) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o x
- - x  - x -  - - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - -
o o -
==================================

Player 1 made the move: (4, 6) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x -  o o o  o - -

- - -  o o -  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - x
o o -
==================================

Player 2 made the move: (2, 2) with o
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  - - x
x x o  o o o  o - -

- - -  o o -  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - x
o o -
==================================

Player 1 made the move: (1, 6) with x
=========== Game Board ===========
x - -  - - -  - - -
- - -  - x -  x - x
x x o  o o o  o - -

- - -  o o -  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - x
o o -
==================================

Player 2 made the move: (1, 0) with o
=========== Game Board ===========
x - -  - - -  - - -
o - -  - x -  x - x
x x o  o o o  o - -

- - -  o o -  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - x
o o -
==================================

Player 1 made the move: (1, 1) with x
=========== Game Board ===========
x - -  - - -  - - -
o x -  - x -  x - x
x x o  o o o  o - -

- - -  o o -  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- - x
o o -
==================================

Player 2 made the move: (3, 5) with o
=========== Game Board ===========
x - -  - - -  - - -
o x -  - x -  x - x
x x o  o o o  o - -

- - -  o o o  x o x
- - x  - x -  x - -
x x o  x - -  x x o

o o o  o o x  - - x
- - -  - o -  - o -
- - -  - o -  x - -
==================================
=========== Block Status =========
- o -
- o x
o o -
==================================

P2
COMPLETE
'''
