import pygame, sys, random, asyncio
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
life_font = pygame.font.Font(None, 40)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 25
number_of_cells = 20

OFFSET = 75

class Food:
	def __init__(self, snake_body):
		self.position = self.generate_random_pos(snake_body)

		self.speed = 1  
		
	
	def updatefood(self, snake_body):
		self.position.y += self.speed
		if self.position.y > number_of_cells:
			self.position = self.generate_random_pos(snake_body)
			snake_body.pop()
			
	
	def draw(self):
		food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
			cell_size, cell_size)
		screen.blit(food_surface, food_rect)

	

	def generate_random_cell(self):
		x = random.randint(0, number_of_cells-1)
		y = random.randint(0, number_of_cells-1)
		return Vector2(x, y)

	def generate_random_pos(self, snake_body):
		position = self.generate_random_cell()
		while position in snake_body:
			position = self.generate_random_cell()
		return position

class Snake:
	def __init__(self):
		self.body = [Vector2(6, 19), Vector2(5,19), Vector2(4,19),Vector2(3,19),Vector2(2,19)]
		self.direction = Vector2(1, 0)
		self.add_segment = False
		

	def draw(self):
		for segment in self.body[:-1]:
			segment_rect = (OFFSET + segment.x * cell_size, OFFSET+ segment.y * cell_size, cell_size, cell_size)
			pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if self.add_segment == True:
			self.add_segment = False
		else:
			self.body = self.body[:-1]

	def reset(self):
		self.body = [Vector2(6, 19), Vector2(5,19), Vector2(4,19),Vector2(3,19),Vector2(2,19)]
		self.direction = Vector2(1, 0)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.food_list = []  
		for i in range(3):    
			self.food_list.append(Food(self.snake.body))
		self.state = "RUNNING"
		self.life = 6

	def draw(self):
		for food in self.food_list:  
			food.draw()
		self.snake.draw()

	def update(self):
		if self.state == "RUNNING":
			self.snake.update()
			for food in self.food_list:  
				self.check_collision_with_food(food)
				food.updatefood(self.snake.body)
			
			self.check_collision_with_edges()
			self.check_collision_with_tail()
			self.lensnake()
			
			self.draw()



	def check_collision_with_food(self,food):
		if food.position in self.snake.body:        
			food.position = food.generate_random_pos(self.snake.body)
			self.snake.add_segment = True
			self.life += 1
		

		

		if food.position.y > -number_of_cells +39:

			self.life -= 1
			if self.life < 0:
				self.game_over()	

		
		


	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
			self.game_over()

	
	def lensnake(self):
		if len(self.snake.body) < 2:
			self.game_over()

	

	def game_over(self):
		self.snake.reset()
		self.food_list[0].position = self.food_list[0].generate_random_pos(self.snake.body)

		self.state = "STOPPED"
		self.life = 5
		

	def check_collision_with_tail(self):
		headless_body = self.snake.body[1:]
		

screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200) 	

async def main():
	while True:
		for event in pygame.event.get():
			if event.type == SNAKE_UPDATE:
				game.update()
			
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if game.state == "STOPPED":
					game.state = "RUNNING"
				if event.key == pygame.K_UP: 
					game.snake.direction = Vector2(0, -1)
				if event.key == pygame.K_DOWN: 
					game.snake.direction = Vector2(0, 1)
				if event.key == pygame.K_LEFT: 
					game.snake.direction = Vector2(-1, 0)
				if event.key == pygame.K_RIGHT: 
					game.snake.direction = Vector2(1, 0)

		#Drawing
		screen.fill(GREEN)
		pygame.draw.rect(screen, DARK_GREEN, 
			(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
		game.draw()
		title_surface = title_font.render("SNOW-SNAKE", True, DARK_GREEN)
		life_surface = life_font.render(str(game.life), True, DARK_GREEN)
		lifew_surface = life_font.render("LIFE: ", True, DARK_GREEN)
		move_surface = life_font.render("MOVE:  < ^ v >", True, DARK_GREEN)

		screen.blit(title_surface, (OFFSET-5, 20))
		screen.blit(life_surface, (OFFSET +70, OFFSET + cell_size*number_of_cells +10))
		screen.blit(lifew_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))
		screen.blit(move_surface, (OFFSET +300, OFFSET + cell_size*number_of_cells +10))
		pygame.display.update()
		clock.tick(60)
		await asyncio.sleep(0)

asyncio.run(main())		