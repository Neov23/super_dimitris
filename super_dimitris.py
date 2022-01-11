import sys
from time import sleep

import pygame

from settings import Settings
from dim import Dim
from ground import Ground
from sun import Sun
from block import Block
from burger import Burger
from bean import Bean
from button import Button
from stats import Stats
from scoreboard import Scoreboard
from big_burger import BigBurger

class SuperDimitris:
    """Overall class to manage the game"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # Initialize Screen
        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Super Dimitris")
        pygame.display.set_icon(pygame.image.load('images/icon.png'))

        self.stats = Stats(self)
        self.scoreboard = Scoreboard(self)
        self.burger_score = Burger(self)

        self.ground = Ground(self)
        self.blocks = pygame.sprite.Group()
        self.burgers = pygame.sprite.Group()
        self.secret_burgers = pygame.sprite.Group()
        self.beans = pygame.sprite.Group()
        self.dim = Dim(self)
        self.bigburger = BigBurger(self)
        self.sun = Sun(self)

        self.play = Button(self, "PLAY")
        self.game_over = Button(self, "GAME OVER", self.settings.screen_width, 
            self.settings.screen_height, 300)
        self.well_done = Button(self, "WELL DONE", self.settings.screen_width,
            self.settings.screen_height, 250)

        # Get clock to set static fps
        self.clock = pygame.time.Clock()

        # Calculate available rows. Create list with col.num. for each row
        # Create list representing a row, and set column number for block
        self.block_row_1 = [14, 43, 54, 55, 56, 57, 58, 85, 92, 105, 106, 107,
        108, 109, 110, 111, 112, 137, 139, 141, 148, 150]
        self.block_row_2 = [1, 2, 14, 30, 31, 34, 35, 36, 55, 56, 57, 58, 85,
            86, 87, 88, 89, 90, 91, 92, 106, 107, 112, 137, 139, 141,
            148, 150]
        self.block_row_3 = [5, 6, 56, 57, 58, 62, 63, 76, 77, 106, 107, 112,
            113, 150]
        self.block_row_4 = [57, 58, 66, 67, 89, 107, 113, 150]
        self.block_row_5 = [58, 70, 71, 107, 108, 109, 110, 113]

        # Create list representing a row, and set column number for burger
        self.burger_row_1 = [9, 20, 21, 22, 84, 138, 140, 142, 143, 144, 145,
            146, 147, 149, 169]
        self.burger_row_2 = [43, 54, 83, 108, 109, 110]
        self.burger_row_3 = [1, 2, 14, 55, 82, 108, 109, 110, 144, 145]
        self.burger_row_4 = [5, 6, 56, 62, 77, 81, 108, 109, 110]
        self.burger_row_5 = [57, 66, 78, 80, 89, 150]
        self.burger_row_6 = [33, 70, 79, 119]

        # Create list representing a row, and set column number for beans
        self.bean_row_1 = [44, 93, 113, 142]

        self.initialize_blocks()
        self.initialize_burgers()
        self.initialize_beans()

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self._move_dim()
                self.dim.update()
                self.blocks.update()
                self.beans.update()
                self._check_bean_direction()
                self._check_dim_burger_collisions()
                self._check_dim_bean_collisions()
                self._check_dim_bigburger_collision()
                self._limit_movement()

            self._update_screen()
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_play_button(self, mouse_pos):
        """Start the game only when the player clicks on the PLAY button"""
        button_clicked = self.play.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Set game active
            self.stats.game_active = True

            # Reset all stats
            self.stats.reset_stats()
            self.scoreboard.set_score()
            self.scoreboard.set_secret_score()

            # Initialize objects position
            self.blocks.empty()
            self.burgers.empty()
            self.beans.empty()

            self.initialize_blocks()
            self.initialize_burgers()
            self.initialize_beans()

            self.dim.initialize_position()
            self.bigburger.initialize_position()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.dim.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.dim.moving_left = True
        if event.key == pygame.K_UP and self.dim.allow_jump:
            self.dim.moving_up = True
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.dim.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.dim.moving_left = False
    
    def initialize_blocks(self):
        """Initialize all blocks and their static position"""
        # Create first row
        for number in self.block_row_1:
            self._create_block(number, 1)
        
        # Create second row
        for number in self.block_row_2:
            self._create_block(number, 2)

        # Create third row
        for number in self.block_row_3:
            self._create_block(number, 3)

        # Create fourth row
        for number in self.block_row_4:
            self._create_block(number, 4)

        # Create fifth row
        for number in self.block_row_5:
            self._create_block(number, 5)

    def _create_block(self, block_number, row_number):
        """Create block and add to sprite group"""
        block = Block(self)
        block_width, block_height = block.rect.size
        block.rect.x = block_width * 5 + (block_width * block_number)
        block.rect.y = ((self.settings.screen_height -
            self.settings.ground_height) - block_height * row_number)
        self.blocks.add(block)
    
    def initialize_burgers(self):
        """Initialize all burgers and their static position"""
        # Create first row
        for number in self.burger_row_1:
            self._create_burger(number, 1)
        
        # Create second row
        for number in self.burger_row_2:
            self._create_burger(number, 2)

        # Create third row
        for number in self.burger_row_3:
            self._create_burger(number, 3)

        # Create fourth row
        for number in self.burger_row_4:
            self._create_burger(number, 4)

        # Create fifth row
        for number in self.burger_row_5:
            self._create_burger(number, 5)
        
        # Create sixth row
        for number in self.burger_row_6:
            self._create_burger(number, 6)
        
        # Create secret burger
        self._create_secret_burger()
    
    def _create_burger(self, burger_number, row_number):
        """Create burger and add to sprite group"""
        burger = Burger(self)
        burger_width, burger_height = burger.rect.size
        burger.rect.x = burger_width * 5 + (burger_width * burger_number)
        burger.rect.y = (self.settings.screen_height -
            self.settings.ground_height - burger_height * row_number)
        self.burgers.add(burger)
    
    def _create_secret_burger(self):
        """Create a secret burger"""
        secret_burger = Burger(self)
        burger_width, burger_height = secret_burger.rect.size
        secret_burger.rect.x = burger_width * 5 + (burger_width * 89)
        secret_burger.rect.y -= burger_height
        self.secret_burgers.add(secret_burger)
    
    def initialize_beans(self):
        """Initialize all beans and their static position"""
        for number in self.bean_row_1:
            self._create_bean(number)
    
    def _create_bean(self, bean_number):
        """Create a bean and add to sprite group"""
        bean = Bean(self)
        bean_width, bean_height = bean.rect.size
        bean.rect.x = bean_width * 5 + (bean_width * bean_number)
        bean.rect.y = (self.settings.screen_height -
            self.settings.ground_height - bean_height)
        self.beans.add(bean)

    def _check_bean_direction(self):
        """If bean collides with block, change direction"""
        for block in self.blocks.sprites():
            for bean in self.beans.sprites():
                if pygame.Rect.colliderect(bean.rect, block.rect):
                    bean.direction *= -1
    
    def _check_dim_burger_collisions(self):
        """Check if dim collides with burger and if so, remove burger"""
        for burger in self.burgers.sprites():
            if pygame.Rect.colliderect(self.dim.rect, burger.rect):
                self.burgers.remove(burger)
                self.stats.score += 1
                self.scoreboard.set_score()
                self.scoreboard.check_high_score()
        if pygame.sprite.spritecollideany(self.dim, self.secret_burgers):
            self.secret_burgers.empty()
            self.stats.secret_score += 1
            self.scoreboard.set_secret_score()

    def _check_dim_bean_collisions(self):
        """Check if dim collides with a bean and if so, simulate GAME OVER"""
        for bean in self.beans.sprites():
            if pygame.Rect.colliderect(self.dim.rect, bean.rect):
                self.stats.save_stats()
                sleep(1.5)
                self.game_over.draw_button()
                pygame.display.flip()
                sleep(3)
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
        
    def _check_dim_bigburger_collision(self):
        """Check if dim collides with final big burger and simulate winning"""
        if pygame.Rect.colliderect(self.dim.rect, self.bigburger.rect):
            self.stats.save_stats()
            sleep(1.5)
            self.well_done.draw_button()
            pygame.display.flip()
            sleep(3)
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _limit_moving_right(self, block):
        """Stop dim walking to the right if there is a block"""
        # Create variables to use as conditions for clean coding
        # In con_2 i set "-1" to make this condition False when on top of block
        con_1 = self.dim.rect.x + self.dim.rect_width == block.rect.x
        con_2 = self.dim.rect.y -1 in range(block.rect.y -
        self.dim.rect_height, block.rect.y + self.settings.block_height)
        con_3 = self.dim.rect.x + self.dim.rect_width > block.rect.x
        con_4 = (self.dim.rect.x + self.dim.rect_width <= block.rect.x +
        self.settings.dim_speed)
        con_5 = self.dim.moving_left

        if (con_1 and con_2) or (con_2 and con_3 and con_4 and not con_5):
            self.dim.rect.x -= self.settings.dim_speed

    def _limit_moving_left(self, block):
        """Stop dim walking to the left if there is a block"""
        # Create variables to use as conditions for clean coding
        con_1 = self.dim.rect.x == block.rect.x + self.settings.block_width
        con_2 = self.dim.rect.y - 1 in range(block.rect.y -
        self.dim.rect_height, block.rect.y + self.settings.block_height)
        con_3 = self.dim.rect.x < block.rect.x + self.settings.block_width
        con_4 = (self.dim.rect.x >= block.rect.x + self.settings.block_width -
        self.settings.dim_speed)
        con_5 = self.dim.moving_right

        if (con_1 and con_2) or (con_2 and con_3 and con_4 and not con_5):
            self.dim.rect.x += self.settings.dim_speed
    
    def _limit_moving_up(self, block):
        """Stop dim jumping through a block"""
        # Create variables to use as conditions for clean coding
        con_1 = self.dim.rect.y == block.rect.y + self.settings.block_height
        con_2 = self.dim.rect.x + self.dim.rect_width in range(block.rect.x,
        block.rect.x + self.settings.block_width + self.dim.rect_width)
        con_3 = self.dim.rect.y < block.rect.y + self.settings.block_height
        con_4 = (self.dim.rect.y >= block.rect.y + self.settings.block_height -
        self.settings.dim_jump)

        if con_1 and con_2:
            self.dim._stop_jumping(True)
        if con_2 and con_3 and con_4:
            self.dim._stop_jumping(True)
            self.dim.rect.y += self.settings.dim_jump

    def _limit_moving_down(self, block):
        """Stop dim falling through a block"""
        # Create variables to use as conditions for clean coding
        con_1 = self.dim.rect.y + self.dim.rect_height == block.rect.y
        con_2 = self.dim.rect.x + self.dim.rect_width in range(block.rect.x,
        block.rect.x + self.settings.block_width + self.dim.rect_width)
        con_3 = self.dim.rect.y + self.dim.rect_height > block.rect.y
        con_4 = (self.dim.rect.y + self.dim.rect_height <= block.rect.y +
        self.settings.dim_gravity)
        if con_1 and con_2:
            self.dim.allow_gravity = False
        if con_2 and con_3 and con_4:
            self.dim.rect.y = block.rect.y - self.dim.rect_height

    def _grounded(self, block):
        """In Dim() instance, set allow_jump to True"""
        con_1 = self.dim.rect.bottom == self.ground.rect.top
        con_2 = self.dim.rect.y + self.dim.rect_height == block.rect.y
        con_3 = self.dim.rect.x + self.dim.rect_width in range(block.rect.x,
        block.rect.x + self.settings.block_width + self.dim.rect_width)
        if con_1 or (con_2 and con_3):
            self.dim.allow_jump = True

    def _limit_movement(self):
        """Set limits to dim's movement"""
        for block in self.blocks.sprites():
            self._limit_moving_right(block)
            self._limit_moving_left(block)
            self._limit_moving_up(block)
            self._limit_moving_down(block)
            self._grounded(block)
    
    def _move_dim(self):
        """If dim reaches the edge, pull all objects to look like dim walking"""
        if self.dim.check_left_edge() and self.dim.moving_left:
            for block in self.blocks.sprites():
                block.rect.x += self.settings.dim_speed
            for burger in self.burgers.sprites():
                burger.rect.x += self.settings.dim_speed
            for bean in self.beans.sprites():
                bean.rect.x += self.settings.dim_speed
            for secret_burger in self.secret_burgers.sprites():
                secret_burger.rect.x += self.settings.dim_speed

            self.bigburger.rect.x += self.settings.dim_speed

        if self.dim.check_right_edge() and self.dim.moving_right:
            for block in self.blocks.sprites():
                block.rect.x -= self.settings.dim_speed
            for burger in self.burgers.sprites():
                burger.rect.x -= self.settings.dim_speed
            for bean in self.beans.sprites():
                bean.rect.x -= self.settings.dim_speed
            for secret_burger in self.secret_burgers.sprites():
                secret_burger.rect.x -= self.settings.dim_speed
            
            self.bigburger.rect.x -= self.settings.dim_speed

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.dim.blitme()
        self.sun.blitme()
        self.bigburger.blitme()
        for block in self.blocks.sprites():
            block.display_block()
        self.burgers.draw(self.screen)
        self.secret_burgers.draw(self.screen)
        self.beans.draw(self.screen)
        self.ground.display_ground()
        self.scoreboard.show_score()
        self.burger_score.blitme()
        self.clock.tick(100)

        if not self.stats.game_active:
            self.play.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    main_program = SuperDimitris()
    main_program.run_game()