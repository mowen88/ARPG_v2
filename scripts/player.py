import math
from settings import *
from state_machine import Idle
from timer import Timer
from objects import Object

class Player(Object):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.game = game
		self.zone = zone

		self.acc = pygame.math.Vector2()
		self.friction = -0.5
		self.max_speed = 2
		self.vel = pygame.math.Vector2()
		self.edge = ''
		self.dashing = False

		self.import_imgs()

		self.state = Idle(self, 'up')
		self.animation_type = 'loop'
		self.frame_index = 0

		self.image = self.animations['down_idle'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.75)

		self.moving_right, self.moving_left = False, False
		self.moving_down, self.moving_up = False, False

	def animate(self, state, animation_speed, anmimation_type):
		self.frame_index += animation_speed
		if anmimation_type == 'end' and self.frame_index >= len(self.animations[state])-1:
			self.frame_index = len(self.animations[state])-1
		else:
			self.frame_index = self.frame_index % len(self.animations[state])
		self.image = self.animations[state][int(self.frame_index)]



	def object_collisions(self, direction):
		
		for sprite in self.zone.collidable_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					
					if direction == 'x':
						if self.vel.x > 0:
							self.hitbox.right = sprite.hitbox.left
							self.acc.x = 0
							
						if self.vel.x < 0:
							self.hitbox.left = sprite.hitbox.right
							self.acc.x = 0

						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx
				
					if direction == 'y':			
						if self.vel.y > 0:
							self.hitbox.bottom = sprite.hitbox.top	
							self.acc.y = 0	
							
						if self.vel.y < 0:
							self.hitbox.top = sprite.hitbox.bottom
							self.acc.y = 0
						
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def stair_collisions(self, dt):

		# all stairs
		for sprite in self.zone.stair_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):

					if sprite.col == '0':
						self.vel *= 0.99
						
					elif sprite.col == '1':
						self.acc.y += self.vel.x
						if self.moving_up:
							self.vel.y -= abs(self.vel.x) * dt
						elif self.moving_down:
							self.vel.y += abs(self.vel.x) * dt

					elif sprite.col == '2':
						self.acc.y -= self.vel.x
						if self.moving_up:
							self.vel.y -= abs(self.vel.x) * dt
						elif self.moving_down:
							self.vel.y += abs(self.vel.x) * dt

	def wall_collisions(self, direction):
		# all walls
		for sprite in self.zone.wall_sprites:
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					rel_x = sprite.hitbox.x - self.hitbox.x
					rel_y = sprite.hitbox.y - self.hitbox.y

					if sprite.col == '5' or sprite.col == '15':
						
						# normal square block collisions....

						if direction == 'x':
							if self.vel.x > 0:
								self.hitbox.right = sprite.hitbox.left
								self.acc = pygame.math.Vector2()
								if sprite.col == '15': self.edge = 'right'
								
							if self.vel.x < 0  and self.vel.magnitude():
								self.hitbox.left = sprite.hitbox.right
								self.acc = pygame.math.Vector2()
								if sprite.col == '15': self.edge = 'left'
							
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx

						if direction == 'y':	
							if self.vel.y > 0:
								self.hitbox.bottom = sprite.hitbox.top
								self.acc = pygame.math.Vector2()
								if sprite.col == '15': self.edge = 'down'
								
							if self.vel.y < 0:
								self.hitbox.top = sprite.hitbox.bottom
								self.acc = pygame.math.Vector2()
								if sprite.col == '15': self.edge = 'up'

							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery
							

					elif sprite.col == '6' or sprite.col == '16':
						# moving right and diagonal up
						
						target_y = sprite.hitbox.top + rel_x
						target_x = sprite.hitbox.left + rel_y

						print(target_x, target_y)

						if self.hitbox.bottom > target_y:
							self.hitbox.bottom = target_y
							self.hitbox.centerx = target_x
							if sprite.col == '16': self.edge = 'right_down'
							self.acc = pygame.math.Vector2()
							
							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx

					elif sprite.col == '7' or sprite.col == '17':
						# moving left and diagonal up
						
						target_y = sprite.hitbox.top - rel_x
						target_x = sprite.hitbox.right - rel_y

						if self.hitbox.bottom > target_y:
							self.hitbox.bottom = target_y
							self.hitbox.centerx = target_x
							if sprite.col == '17': self.edge = 'left_down'
							self.acc = pygame.math.Vector2()
							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx


					elif sprite.col == '8' or sprite.col == '18':
						# moving right and diagonal down
						
						target_y = sprite.hitbox.bottom - rel_x
						target_x = sprite.hitbox.left - rel_y

						if self.hitbox.top < target_y:
							self.hitbox.top = target_y
							self.hitbox.right = target_x
							if sprite.col == '18': self.edge = 'right_up'
							self.acc = pygame.math.Vector2()
							
							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx


					elif sprite.col == '9' or sprite.col == '19':
						# moving left and diagonal down
						
						target_y = sprite.hitbox.bottom + rel_x
						target_x = sprite.hitbox.right + rel_y

						if self.hitbox.top < target_y:
							self.hitbox.top = target_y 
							self.hitbox.left = target_x
							if sprite.col == '19': self.edge = 'left_up'
							self.acc = pygame.math.Vector2()
							
							self.rect.centery = self.hitbox.centery
							self.pos.y = self.hitbox.centery
							self.rect.centerx = self.hitbox.centerx
							self.pos.x = self.hitbox.centerx

		
	def physics(self, dt):
		
		self.stair_collisions(dt)
		
		# x direction
		self.acc.x += self.vel.x * self.friction
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
		self.vel.x = max(-self.max_speed, min(self.vel.x, self.max_speed))
		if abs(self.vel.x) < 0.05: self.vel.x = 0 
		self.hitbox.centerx = round(self.pos.x)
	
		self.wall_collisions('x')
		self.object_collisions('x')
		self.rect.centerx = self.hitbox.centerx
		
		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y * dt) * dt
		self.vel.y = max(-self.max_speed, min(self.vel.y, self.max_speed))
		if abs(self.vel.y) < 0.05: self.vel.y = 0 
		self.hitbox.centery = round(self.pos.y)

		self.wall_collisions('y')
		self.object_collisions('y')
		self.rect.centery = self.hitbox.centery
		
		if self.vel.magnitude() > self.max_speed:
			self.vel = self.vel.normalize() * self.max_speed

		if self.acc.magnitude() < 0.1:
			self.acc = pygame.math.Vector2()

	def state_logic(self):
		new_state = self.state.state_logic(self)
		if new_state != None:
			self.state = new_state
		else: 
			self.state
		
	def import_imgs(self):
		self.animations = {'down_attack':[], 'up_attack':[], 'right_attack':[], 'left_attack':[], 'up':[], 'down':[], 'left':[], 'right':[], 'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[]}

		for animation in self.animations.keys():
			full_path = '../assets/player/' + animation
			self.animations[animation] = self.game.import_folder(full_path)

	def update(self, dt):
		self.state.update(dt, self)
		self.state_logic()

	def render(self, screen):
		pass

