import os
import sys
import threading
import random
import time
from msvcrt import *
from extra.tools.asker import complex_ask


class BattleModeGameManager:
	"""This class provides methods for implementing the Battle mode"""

	def __init__(self, player_score_instance, game_menu_instance):
		'''Setting the keys on the keyboard to control the snakes,
		setting self.menu and self.player_score'''
		
		self.UP_1 = [119, 87]  # w W
		self.DOWN_1 = [115, 83]  # s S
		self.LEFT_1 = [97, 65]  # a A
		self.RIGHT_1 = [100, 68]  # d D

		self.UP_2 = 72 
		self.DOWN_2 = 80
		self.LEFT_2 = 75
		self.RIGHT_2 = 77
		self.keys_player_2 = [72, 80, 75, 77]

		self.settings_storage = {}
		self.player_score = player_score_instance
		self.menu = game_menu_instance
		
	def run(self):
		"""Method starting the mode automatically"""
		player_wants_to_change_gamemode = False 
		plays_current_game_in_current_gamemode = True

		while plays_current_game_in_current_gamemode:

			wanna_continue_the_current_game = True
			repeat_the_game = False

			# Survey of the player about the game settings
			self.settings_storage = complex_ask(self.menu, 3)

			# Setting default settings according to the choice of the player
			self.set_default_settings() 

			while wanna_continue_the_current_game:
				self.initialize_new_players()
			
				while (not self.get_game_over_status_player_1() and
					not self.get_game_over_status_player_2()):
					self.draw_whole_field() # ?

					threads = self.create_new_threads()

					for t in threads:
						t.start()

					self.process_hook_logic_for_player_1()
					self.process_hook_logic_for_player_2()

					# If player1 or player2 lose 
					if (self.get_game_over_status_player_1() or 
						self.get_game_over_status_player_2() or
						self.is_the_time_over()):

						winner = self.determine_who_won()
						if winner == 1:
							print("Player 1 won the game!")
						elif winner == 2:
							print("Player 2 won the game!")
						else:
							print('Draw!')

						print("P1: " + self.get_score_of_players()[0])
						print("P2: " + self.get_score_of_players()[1])  
						print('~' * 40)

						player_resp = self.menu.ask_player_for_further_actions()
						if player_resp == 1:
							self.set_default_settings()
							self.set_game_over_false()
							break
						elif player_resp == 2: 
							wanna_continue_the_current_game = False
							self.set_game_over_false()
							break
						elif player_resp == 3:
							wanna_continue_the_current_game = False 
							plays_current_game_in_current_gamemode = False
							self.set_game_over_false()
							break					
						else:
							exit()

	def initialize_new_players(self):
		"""Method sets the initial length of snakes and sets the adding 
		bonus for extra speed of the game"""
		
		# Setting the default length of the 1-st snake
		self.snake_segments_coord_x_1 = [self.head_x_coord_1
		for i in range(self.num_of_snake_segments_1 + 1)] # List generator 

		offsets_of_the_snake_segment_y_1 = 1
		for i in range(self.num_of_snake_segments_1  + 1):
			self.snake_segments_coord_y_1.append(self.head_y_coord_1 + 
			offsets_of_the_snake_segment_y_1) 

			offsets_of_the_snake_segment_y_1 += 1

		# Setting the default length of the 2-d snake
		self.snake_segments_coord_x_2 = [self.head_x_coord_2
		for i in range(self.num_of_snake_segments_2 + 1)] # List generator 

		offsets_of_the_snake_segment_y_2 = 1
		for i in range(self.num_of_snake_segments_2  + 1):
			self.snake_segments_coord_y_2.append(self.head_y_coord_2 + 
			offsets_of_the_snake_segment_y_2) 

			offsets_of_the_snake_segment_y_2 += 1

		# Setting points for one fruit
		if self.game_speed == 0.08:
			self.adding_points = 20
		elif self.game_speed == 0.06:
			self.adding_points = 30
		else:
			self.adding_points = 40

	def draw_whole_field(self):
		"""Method constantly redraws the playing fields, snakes, fruits and 
		score&time indicator"""

		for i in range(self.width + 1):
			# Drawing the space between two fields (TOP)
			if i > 20 and i < 40:
				print(' ',end = '')
			else:
				# Drawing the upper edges
				print("█", end = '')

		print(" ")
		# Drawing snakes' head, fruit, side edges, snakes' tails, and a void
		for i in range(self.height + 1):
				
		 	for j in range(self.width + 1):
		 		# Drawing 1-st snake's head
		 		if i == self.head_y_coord_1 and j == self.head_x_coord_1:
		 			print("0" , end = "")

		 		# Drawing 2-nd snake's head
		 		elif i == self.head_y_coord_2 and j == self.head_x_coord_2:
		 			print("0" , end = "")

		 		# Drawing fruit in different game fields
		 		elif (i == self.y_coord_of_fruit_1	and
		 			j == self.x_coord_of_fruit_1 or 
		 			i == self.y_coord_of_fruit_2 and
		 			j == self.x_coord_of_fruit_2):
		 			print("*" , end = "")

		 		# Drawing the side edges of two fields
		 		elif j == 0 or j == 20  or j == 40 or j == self.width:
		 			# Drawing the side borders of the 1-st field
		 			if j == 0:
		 				print("█", end = "")
		 			elif j == 20 :
		 			 	print("█", end = "")
		 			 # Drawing the side borders of the 2-nd field
		 			elif j == 40:
		 				print("█", end = "")
		 			else:
		 				print("█")
									
		 		else:
		 			# Drawing tail of the 1-st snake
		 			print_tail_1 = False
		 			for k in range(self.num_of_snake_segments_1):
		 			  	if (self.snake_segments_coord_x_1[k] == j and 
		 			  		self.snake_segments_coord_y_1[k] == i): 
		 			  		print_tail_1 = True
		 			  		print("o", end = "")
					
					# Drawing tail of the 2-nd snake
		 			print_tail_2 = False
		 			for t in range(self.num_of_snake_segments_2):
		 				if (self.snake_segments_coord_x_2[t] == j and 
		 			  		self.snake_segments_coord_y_2[t] == i): 
		 			  		print_tail_2 = True
		 			  		print("o", end = "")
								 
		 			if not print_tail_1 and not print_tail_2:
		 				print(" ", end = "")
		
		# Drawing the space between two fields (Bottom)
		for i in range(self.width + 1):
			if i > 20 and i < 40:
				print(' ',end = '')
			else:
				# Drawing the bottom borders of 2 fields
				print("█", end = '') 

		print(' ')
		print(self.centralize_score_n_time + "P1: " + str(self.score_1) + 
			' | ' + 'Time: ' + str(self.time - self.countdown) + ' | ' + 
		 	'P2: ' + str(self.score_2)) 

		self.countdown += 1
		time.sleep(self.game_speed)
		os.system('cls')

	def process_players_input(self):
		'''Handles pressing keyboard keys. Changes the 
		direction of the snakes (depends on the keys that players press)'''
	  		
		time.sleep(0.085)
		if kbhit():
		 	key = ord(getch())
		 	if key not in self.keys_player_2:
			 	if key in self.UP_1:
		  		 	self.direction_1 = 'UP'
			 	elif key in self.DOWN_1:		
		  		 	self.direction_1  = 'DOWN'

			 	elif key in self.LEFT_1:			
		  		 	self.direction_1 = 'LEFT'
			 	elif key in self.RIGHT_1:
		  		 	self.direction_1 = 'RIGHT'
		 	else:
		 		if key == self.UP_2:
		 			self.direction_2 = 'UP'
		 		elif key == self.DOWN_2:		
	  		 		self.direction_2  = 'DOWN'

		 		elif key == self.LEFT_2:			
	  		 		self.direction_2 = 'LEFT'
		 		elif key == self.RIGHT_2:
	  		 		self.direction_2 = 'RIGHT'

	def process_hook_logic_for_player_1(self):
		'''Handles logic related to the tail of the snake1, direction of 
		the	snake1, logic for eating fruits(snake1), cases in which 
		self.game_over_1 = True for snake1'''

		# Snake1's tail logic
		self.snake_segments_coord_x_1.append(0)
		self.snake_segments_coord_y_1.append(0)

		prev_coord_x_1 = self.snake_segments_coord_x_1[0]
		prev_coord_y_1 = self.snake_segments_coord_y_1[0]	

		prev_coord2_x_1 = 0
		prev_coord2_y_1 = 0 

		self.snake_segments_coord_x_1[0] = self.head_x_coord_1
		self.snake_segments_coord_y_1[0] = self.head_y_coord_1

		for i in range(1, self.num_of_snake_segments_1):
			
			prev_coord2_x_1 = self.snake_segments_coord_x_1[i]
			prev_coord2_y_1 = self.snake_segments_coord_y_1[i]

			self.snake_segments_coord_x_1[i] =  prev_coord_x_1
			self.snake_segments_coord_y_1[i] = prev_coord_y_1

			prev_coord_x_1 = prev_coord2_x_1
			prev_coord_y_1 = prev_coord2_y_1

		# The logic related to the direction of the snake1
		if self.direction_1 == 'LEFT':
			self.head_x_coord_1 -= 1
		elif self.direction_1 == 'RIGHT':
			self.head_x_coord_1 += 1

		elif self.direction_1 == 'UP':
			self.head_y_coord_1 -= 1
		elif self.direction_1 == 'DOWN':
			self.head_y_coord_1 += 1
		
		# Snake1 and walls logic 
		if self.snake_and_walls == 'can crawl through the walls':
			if self.head_x_coord_1 > 19:
				self.head_x_coord_1 = 1
			elif self.head_x_coord_1 == 0:
				self.head_x_coord_1 = 19
		
			if self.head_y_coord_1 > self.height:
				self.head_y_coord_1 = 0
			elif self.head_y_coord_1 < 0:
				self.head_y_coord_1 = self.height

		else:
			if (self.head_x_coord_1 > 19 or 
				self.head_x_coord_1 == 0):
				self.game_over_1 = True 
				
			elif (self.head_y_coord_1 > self.height or 
				self.head_y_coord_1 < 0):
				self.game_over_1 = True 
		
		# Cases for self.game_over_1 = True (snake1)
		for i in range(self.num_of_snake_segments_1):
			if (self.snake_segments_coord_x_1[i] == self.head_x_coord_1 and
				self.snake_segments_coord_y_1[i] == self.head_y_coord_1):
				self.game_over_1 = True 	

		# Eating fruit logic (snake1)		
		if (self.head_x_coord_1 == self.x_coord_of_fruit_1 and
			self.head_y_coord_1 == self.y_coord_of_fruit_1):

			self.x_coord_of_fruit_1 = random.randint(1, 19)
			self.y_coord_of_fruit_1 = random.randint(1, 19)

			self.x_coord_of_fruit_2 = self.x_coord_of_fruit_1 + 40
			self.y_coord_of_fruit_2 = self.y_coord_of_fruit_1

			self.num_of_snake_segments_2 += 1
			self.score_1 += self.adding_points

	def process_hook_logic_for_player_2(self):
		'''Handles logic related to the tail of the snake2, direction of 
		the	snake2, logic for eating fruits(snake2), cases in which 
		self.game_over_2 = True for snake2'''

		# Snake2's tail logic
		self.snake_segments_coord_x_2.append(0)
		self.snake_segments_coord_y_2.append(0)

		prev_coord_x_2 = self.snake_segments_coord_x_2[0]
		prev_coord_y_2 = self.snake_segments_coord_y_2[0]	

		prev_coord2_x_2 = 0 
		prev_coord2_y_2 = 0 

		self.snake_segments_coord_x_2[0] = self.head_x_coord_2
		self.snake_segments_coord_y_2[0] = self.head_y_coord_2

		for i in range(1, self.num_of_snake_segments_2):
			prev_coord2_x_2 = self.snake_segments_coord_x_2[i]
			prev_coord2_y_2 = self.snake_segments_coord_y_2[i]

			self.snake_segments_coord_x_2[i] =  prev_coord_x_2
			self.snake_segments_coord_y_2[i] = prev_coord_y_2

			prev_coord_x_2 = prev_coord2_x_2
			prev_coord_y_2 = prev_coord2_y_2

		# The logic related to the direction of the snake2
		if self.direction_2 == 'LEFT':
			self.head_x_coord_2 -= 1
		elif self.direction_2 == 'RIGHT':
			self.head_x_coord_2 += 1

		elif self.direction_2 == 'UP':
			self.head_y_coord_2 -= 1
		elif self.direction_2 == 'DOWN':
			self.head_y_coord_2 += 1

		# Snake2 and walls logic 
		if self.snake_and_walls == 'can crawl through the walls':
			if self.head_x_coord_2 > self.width - 1:
				self.head_x_coord_2 = 41
			elif self.head_x_coord_2 == 40:
				self.head_x_coord_2 = self.width - 1

			if self.head_y_coord_2 > self.height:
				self.head_y_coord_2 = 0
			elif self.head_y_coord_2 < 0:
				self.head_y_coord_2 = self.height

		else:
			if (self.head_x_coord_2 > self.width - 1 or 
				self.head_x_coord_2 == 0):
				self.game_over_2 = True 
			elif (self.head_y_coord_2 > self.height or
				self.head_y_coord_2 < 0):
				self.game_over_2 = True

		# Cases for self.game_over_2 = True (snake2)
		for i in range(self.num_of_snake_segments_2):
		 	if (self.snake_segments_coord_x_2[i] == self.head_x_coord_2 and
		 		self.snake_segments_coord_y_2[i] == self.head_y_coord_2):
		 		self.game_over_2 = True  

		# Eating fruit logic (snake2)
		if (self.head_x_coord_2 == self.x_coord_of_fruit_2 and
			self.head_y_coord_2 == self.y_coord_of_fruit_2):

			self.x_coord_of_fruit_2 = random.randint(41, self.width - 1)
			self.y_coord_of_fruit_2 = random.randint(1, self.height - 1)

			self.x_coord_of_fruit_1 = self.x_coord_of_fruit_2 - 40
			self.y_coord_of_fruit_1 = self.y_coord_of_fruit_2

			self.num_of_snake_segments_1 += 1
			self.score_2 += self.adding_points

	def get_game_over_status_player_1(self) -> bool:
	 	return self.game_over_1

	def get_game_over_status_player_2(self) -> bool:
		return self.game_over_2
		
	def set_game_mode_false(self):
		self.gamemode = False

	def set_default_settings(self):
		'''Sets attribute settings before the beginning of the game itself'''

		# Basic settings
		self.width = 60
		self.height = 20
		self.snake_and_walls = self.settings_storage['walls']
		self.centralize_score_n_time = " " * (int(self.width / 2) - 12)
		self.game_speed = self.settings_storage['speed']
		self.time = self.settings_storage['game_time']
		self.countdown = 0

		# Snake1's settings
		self.game_over_1 = False
		self.score_1 = 0
		self.head_x_coord_1 = 10
		self.head_y_coord_1 = 10
		self.direction_1 = 'UP'
		self.x_coord_of_fruit_1 = random.randint(1, 19)
		self.y_coord_of_fruit_1 = random.randint(1, self.height - 1)
		self.num_of_snake_segments_1 = self.settings_storage['length']
		self.snake_segments_coord_x_1 = [] 
		self.snake_segments_coord_y_1 = [] 

		# Snake2's settings
		self.game_over_2 = False
		self.score_2 = 0
		self.head_x_coord_2 = 50
		self.head_y_coord_2 = 10
		self.direction_2 = 'UP'
		self.x_coord_of_fruit_2 = self.x_coord_of_fruit_1 + 40
		self.y_coord_of_fruit_2 = self.y_coord_of_fruit_1
		self.num_of_snake_segments_2 = self.settings_storage['length']
		self.snake_segments_coord_x_2 = [] 
		self.snake_segments_coord_y_2 = []

	def get_score(self) -> int:
		return self.score

	def is_the_time_over(self) -> bool:
		time = self.time - self.countdown
		if time == 0:
			return True
		return False 

	def set_game_over_false(self):
		self.game_over_1 = False
		self.game_over_2 = False

	def determine_who_won(self) -> int:
		if self.score_1 > self.score_2: 
			if (not self.game_over_1 and self.game_over_2 or not
				self.game_over_1 and not self.game_over_2):
				return 1
			else:
				return 2 
		elif self.score_1 < self.score_2:
			if (self.game_over_1 and not self.game_over_2 or not
				self.game_over_1 and not self.game_over_2):
				return 2
			else:
				return 1
		elif self.score_1 == self.score_2:
			if not self.game_over_1 and self.game_over_2:
				return 1
			elif self.game_over_1 and not self.game_over_2:
				return 2
			else:
				return 3

	def get_score_of_players(self) -> list:
		return [str(self.score_1), str(self.score_2)]

	def get_status_about_snake_and_fruit(self):
		return self.another_player_gets_longer_status

	def create_new_threads(self) -> list:
		threading_list = []
		t1 = threading.Thread(target= lambda: self.process_players_input())
		threading_list.extend([t1])
		return threading_list   
