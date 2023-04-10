import math
from settings import *
from state_machine import IdleState
from timer import Timer

class Object(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.image = pygame.transform.scale_by(self.image, SCALE)
		self.rect = self.image.get_rect(topleft = pos)

class Entity(Object):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.game = game
		self.zone = zone

		self.image = pygame.Surface((25, 25))
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(self.image.get_width() * 0.2, self.image.get_height() * 0.2)
		self.pos = pygame.math.Vector2(self.hitbox.center)
		self.vel = pygame.math.Vector2()
		
		self.acc = 0.25
		self.friction = 0.25
		self.max_speed = 2

	def switch_layer(self):
		for group in self.zone.layers:
			if self in group:
				new_group = self.zone.layers.index(group)-1
				group.remove(self)
				self.zone.layers[new_group].add(self)

	def animate(self):
		self.frame_index += 0.2
		if self.frame_index >= len(self.animations[self.state]):
			self.frame_index = 0
		self.image = self.animations[self.state][int(self.frame_index)]

	def update(self):
		pass


	def render(self, screen):
		pass

class Player(Entity):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.acc = 0.3
		self.friction = 0.3
		self.max_speed = 3

		self.import_imgs()
		self.state = IdleState()
		self.animation_type = 'loop'
		self.frame_index = 0

		#self.image = self.animations[self.state][self.frame_index]
		self.image = self.animations['down_idle'][self.frame_index]

		self.moving_right, self.moving_left = False, False
		self.moving_down, self.moving_up = False, False
		self.cardinal_directions = ['down', 'up', 'right', 'left']


		self.attacking = Timer(300)

	def state_logic(self):
		new_state = self.state.state_logic(self)
		self.state = new_state if new_state is not None else self.state
		
	def import_imgs(self):
		self.animations = {'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}

		for animation in self.animations.keys():
			full_path = '../assets/player/' + animation
			self.animations[animation] = self.game.import_folder(full_path)


	def input(self):
		keys = pygame.key.get_pressed()

		if ACTIONS['space']:
			print('yes')
			self.attacking.start()

		if keys[pygame.K_RIGHT]:
			self.moving_right = True
		else:
			self.moving_right = False
			
		if keys[pygame.K_LEFT]:
			self.moving_left = True	
		else:
			self.moving_left = False
			
		if keys[pygame.K_DOWN]:
			self.moving_down = True
		else:
			self.moving_down = False

		if keys[pygame.K_UP]:
			self.moving_up = True
		else:
			self.moving_up = False


	def move_logic(self):
		# y direction
		if self.moving_down:
			self.state = 'down'
			self.vel.y += self.acc
		elif self.moving_up:
			self.state = 'up'
			self.vel.y -= self.acc
		elif self.vel.y > 0:
			self.vel.y -= self.friction
		else:
			self.vel.y += self.friction

		# x direction
		if self.moving_right:
			self.state = 'right'
			self.vel.x += self.acc
		elif self.moving_left:
			self.state = 'left'
			self.vel.x -= self.acc
		elif self.vel.x > 0:
			self.vel.x -= self.friction
		else:
			self.vel.x += self.friction

		# normalize speed for diagonal, max speed may be lower depending on acc and friction values (might resolve to a lower value than the max speed as friction builds up)
		if self.vel.magnitude() >= self.max_speed:
			self.vel = self.vel.normalize() * self.max_speed
	
		# move the entity
		self.hitbox.center += self.vel
		self.rect.center = self.hitbox.center

	def change_state(self, new_state, new_frame_rate, new_animation_type):
		if self.state != new_state:
			self.frame_index = 0
			self.state = new_state
			self.frame_rate = new_frame_rate
			self.animation_type = new_animation_type

	def set_state(self):
		pass
		# initialize states in order of priority...
		

		# # loop to control state switching from general moving and idling
		# elif self.state in self.cardinal_directions:
		# 	for state in self.cardinal_directions:	
		# 		if self.vel.magnitude() < 0.5 and self.state == state:
		# 			state = state.split('_')[0] + '_idle'
		# 			self.change_state(state, 0.2, 'loop')

		# 		elif self.state == state:
		# 			self.change_state(state, 0.2, 'loop')

	def update(self):
		#self.input()
		self.state_logic()
		self.state.update(self)

		#self.animate()
		self.move_logic()


	def render(self, screen):
		pass

