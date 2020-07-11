import pytest
from extra.game_environment.menu_files.menu import Menu 
from extra.game_environment.score_files.score import Score 
from gamemodes.classic_mode import ClassicModeGameManager
from gamemodes.survival_mode import SurvivalModeGameManager
from gamemodes.battle_mode import BattleModeGameManager


class TestClassicGamemodeClass:

	def setup(self):
		menu_inst = Menu()
		score_inst = Score('TestName')
		self.gamemode = ClassicModeGameManager(score_inst, menu_inst)
		self.gamemode.settings_storage['width'] = 40
		self.gamemode.settings_storage['height'] = 20

		walls = "can crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.settings_storage['speed'] = 0.08
		self.gamemode.settings_storage['length'] = 3
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_player()

	def test_initialize_new_player_method_classic_mode(self):
		self.setup()
		assert len(self.gamemode.snake_segments_coord_x) != 0
		assert len(self.gamemode.snake_segments_coord_y) != 0 
		assert self.gamemode.adding_points in [20, 30, 40]

	def test_snake_and_walls_logic_classic_mode(self):

		self.gamemode.head_x_coord = 41
		self.gamemode.process_hook_logic()
		assert self.gamemode.head_x_coord == 1
		assert self.gamemode.game_over == False 

		self.gamemode.head_x_coord = 0
		self.gamemode.process_hook_logic()
		assert self.gamemode.head_x_coord == self.gamemode.width - 1
		assert self.gamemode.game_over == False 

		self.gamemode.head_y_coord = 22
		self.gamemode.process_hook_logic()
		assert self.gamemode.head_y_coord == 0
		assert self.gamemode.game_over == False 

		self.gamemode.head_y_coord = -1 
		self.gamemode.process_hook_logic()
		assert self.gamemode.head_y_coord == self.gamemode.height
		assert self.gamemode.game_over == False 

		walls = "can't crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_player()

		self.gamemode.head_x_coord = 40
		self.gamemode.process_hook_logic()
		assert self.gamemode.game_over == True 

		self.gamemode.head_x_coord = 0
		self.gamemode.process_hook_logic()
		assert self.gamemode.game_over == True

		self.gamemode.head_y_coord = 21
		self.gamemode.process_hook_logic()
		assert self.gamemode.game_over == True

		self.gamemode.head_y_coord = -1
		self.gamemode.process_hook_logic()
		assert self.gamemode.game_over == True 

	def test_snake_eats_fruit_logic_classic_mode(self):
		self.gamemode.head_x_coord = 20 
		self.gamemode.head_y_coord = 11
		self.gamemode.x_coord_of_fruit = 20 
		self.gamemode.y_coord_of_fruit = 10
		self.gamemode.process_hook_logic()
		assert self.gamemode.num_of_snake_segments == 4

	def test_snake_eats_itself_logic_classic_mode(self):
		self.gamemode.head_x_coord = 20 
		self.gamemode.head_y_coord = 13
		self.gamemode.process_hook_logic()
		assert self.gamemode.game_over == True


class TestSurvivalGamemodeClass:

	def setup(self):
		menu_inst = Menu()
		score_inst = Score('TestName')
		self.gamemode = SurvivalModeGameManager(score_inst, menu_inst)
		self.gamemode.settings_storage['width'] = 40
		self.gamemode.settings_storage['height'] = 20

		walls = "can crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.settings_storage['speed'] = 0.08
		self.gamemode.settings_storage['length'] = 3
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_players()

	def test_initialize_new_players_method_survival_mode(self):
		self.setup()
		assert len(self.gamemode.snake_segments_coord_x_1) != 0
		assert len(self.gamemode.snake_segments_coord_y_1) != 0 
		assert len(self.gamemode.snake_segments_coord_x_2) != 0
		assert len(self.gamemode.snake_segments_coord_y_2) != 0
		assert self.gamemode.adding_points in [20, 30, 40]

	def test_snake_and_walls_logic_survival_mode(self):
		# Snake 1
		self.gamemode.head_x_coord_1 = 41
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_x_coord_1 == 1
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_x_coord_1 = 0
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_x_coord_1 == self.gamemode.width - 1
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_y_coord_1 = 22
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_y_coord_1 == 0
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_y_coord_1 = -1 
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_y_coord_1 == self.gamemode.height
		assert self.gamemode.game_over_1 == False

		# Snake 2 
		self.gamemode.head_x_coord_2 = 41
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_x_coord_2 == 1
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_x_coord_2 = 0
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_x_coord_2 == self.gamemode.width - 1
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_y_coord_2 = 22
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_y_coord_2 == 0
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_y_coord_2 = -1 
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_y_coord_2 == self.gamemode.height
		assert self.gamemode.game_over_2 == False

		walls = "can't crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_players()

		# Snake 1
		self.gamemode.head_x_coord_1 = 40
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True 

		self.gamemode.head_x_coord_1 = 0
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		self.gamemode.head_y_coord_1 = 21
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		self.gamemode.head_y_coord_1 = -1
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		# Snake 2
		self.gamemode.head_x_coord_2 = 40
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True 

		self.gamemode.head_x_coord_2 = 0
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True

		self.gamemode.head_y_coord_2 = 21
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True

		self.gamemode.head_y_coord_2 = -1
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True

	def test_snake_eats_fruit_logic_survival_mode(self):
		# Snake 1
		self.gamemode.head_x_coord_1 = 20 
		self.gamemode.head_y_coord_1 = 11
		self.gamemode.x_coord_of_fruit = 20 
		self.gamemode.y_coord_of_fruit = 10
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.num_of_snake_segments_1 == 4

		# Snake 2
		self.gamemode.head_x_coord_2 = 20 
		self.gamemode.head_y_coord_2 = 11
		self.gamemode.x_coord_of_fruit = 20 
		self.gamemode.y_coord_of_fruit = 10
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.num_of_snake_segments_2 == 4

	def test_snake_eats_itself_logic_classic_mode(self):
		# Snake 1 
		self.gamemode.head_x_coord_1 = 15 
		self.gamemode.head_y_coord_1 = 13
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		# Snake 2
		self.gamemode.head_x_coord_2 = 25 
		self.gamemode.head_y_coord_2 = 13
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True

	def test_common_logic_of_2_snakes(self):
		self.gamemode.head_x_coord_1 = 20
		self.gamemode.head_y_coord_1 = 20 
		self.gamemode.head_x_coord_2 = 20
		self.gamemode.head_y_coord_2 = 20

		self.gamemode.process_common_logic_of_2_snakes()
		assert self.gamemode.game_over_1 == True
		assert self.gamemode.game_over_2 == True

		# Snake 1
		self.gamemode.game_over_1 = False  
		self.gamemode.head_x_coord_1 = 25
		self.gamemode.head_y_coord_1 = 13
		self.gamemode.process_common_logic_of_2_snakes()
		assert self.gamemode.game_over_1 == True
		self.gamemode.game_over_1 = False 

		# Snake 2
		self.gamemode.game_over_2 = False
		self.gamemode.head_x_coord_2 = 15
		self.gamemode.head_y_coord_2 = 13
		self.gamemode.process_common_logic_of_2_snakes()
		assert self.gamemode.game_over_2 == True


class TestBattleGamemodeClass:

	def setup(self):
		menu_inst = Menu()
		score_inst = Score('TestName')
		self.gamemode = BattleModeGameManager(score_inst, menu_inst)

		walls = "can crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.settings_storage['speed'] = 0.08
		self.gamemode.settings_storage['game_time'] = 1000
		self.gamemode.settings_storage['length'] = 3
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_players()

	def test_initialize_new_players_method_battle_mode(self):
		self.setup()
		assert len(self.gamemode.snake_segments_coord_x_1) != 0
		assert len(self.gamemode.snake_segments_coord_y_1) != 0 
		assert len(self.gamemode.snake_segments_coord_x_2) != 0
		assert len(self.gamemode.snake_segments_coord_y_2) != 0
		assert self.gamemode.adding_points in [20, 30, 40]

	def test_snake_and_walls_logic_battle_mode(self):
		# Snake 1
		self.gamemode.head_x_coord_1 = 20
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_x_coord_1 == 1
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_x_coord_1 = 0
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_x_coord_1 == 19
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_y_coord_1 = 22
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_y_coord_1 == 0
		assert self.gamemode.game_over_1 == False 

		self.gamemode.head_y_coord_1 = -1 
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.head_y_coord_1 == 20
		assert self.gamemode.game_over_1 == False

		# Snake 2 
		self.gamemode.head_x_coord_2 = 60
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_x_coord_2 == 41
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_x_coord_2 = 40
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_x_coord_2 == 59
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_y_coord_2 = 22
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_y_coord_2 == 0
		assert self.gamemode.game_over_2 == False 

		self.gamemode.head_y_coord_2 = -1 
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.head_y_coord_2 == 20
		assert self.gamemode.game_over_2 == False

		walls = "can't crawl through the walls"
		self.gamemode.settings_storage['walls'] = walls
		self.gamemode.set_default_settings()
		self.gamemode.initialize_new_players()

		# Snake 1
		self.gamemode.head_x_coord_1 = 20
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True 

		self.gamemode.head_x_coord_1 = 0
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True 

		self.gamemode.head_y_coord_1 = 21
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True 

		self.gamemode.head_y_coord_1 = -1 
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		# Snake 2 
		self.gamemode.head_x_coord_2 = 60
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True 

		self.gamemode.head_x_coord_2 = 40
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True 

		self.gamemode.head_y_coord_2 = 21
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True 

		self.gamemode.head_y_coord_2 = -1 
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True

	def test_snake_eats_fruit_logic_battle_mode(self):
		# Snake 1
		self.gamemode.head_x_coord_1 = 10 
		self.gamemode.head_y_coord_1 = 11
		self.gamemode.x_coord_of_fruit_1 = 10 
		self.gamemode.y_coord_of_fruit_1 = 10
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.num_of_snake_segments_2 == 4

		# Snake 2
		self.gamemode.head_x_coord_2 = 55 
		self.gamemode.head_y_coord_2 = 11
		self.gamemode.x_coord_of_fruit_2 = 55 
		self.gamemode.y_coord_of_fruit_2 = 10
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.num_of_snake_segments_1 == 4

	def test_snake_eats_itself_logic_battle_mode(self):
		# Snake 1 
		self.gamemode.head_x_coord_1 = 10 
		self.gamemode.head_y_coord_1 = 13
		self.gamemode.process_hook_logic_for_player_1()
		assert self.gamemode.game_over_1 == True

		# Snake 2
		self.gamemode.head_x_coord_2 = 50 
		self.gamemode.head_y_coord_2 = 13
		self.gamemode.process_hook_logic_for_player_2()
		assert self.gamemode.game_over_2 == True
