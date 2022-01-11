import pygame

class Dim:
    """A class to represent the character 'dim'."""

    def __init__(self, program):
        """Initialize dim and get its rect"""
        self.screen = program.screen
        self.settings = program.settings
        self.screen_rect = program.screen.get_rect()
        self.ground_rect = program.ground.rect

        # Load dim's image and get its rect
        self.image = pygame.image.load('images/dim.png')
        self.rect = self.image.get_rect()

        # Get rect's width and height
        self.rect_width, self.rect_height = self.rect.size

        # Movement flags
        self.allow_jump = True
        self.allow_gravity = True
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False

        # Set moving_up as False when this variable becomes 0
        self.levitation = self.settings.dim_jump * 4
        
        self.initialize_position()

    def initialize_position(self):
        """Set dim's initial position"""
        self.rect.x = 200
        self.rect.y = (self.ground_rect.top - self.rect_height)
        
    def update(self):
        """Move dim and set it's positional limits"""
        self._left_right_movement()
        self._jump()
        self._stop_jumping()
        self._gravity()

        # Set allow_gravity always to True. Can be set False only in main
        self.allow_gravity = True
        # Set allow_jump always to False. Can be set True only in main
        self.allow_jump = False
    
    def _left_right_movement(self):
        """Move dim left and right"""
        if self.moving_right and self.rect.right < self.screen_rect.right - 599:
            self.rect.x += self.settings.dim_speed
        if self.moving_left and self.rect.left > 149:
            self.rect.x -= self.settings.dim_speed
        
        # I use 298 and 18, to be in condition's range in _check_edges().

    def _jump(self):
        """Simulate dim's jump"""
        if self.moving_up and (self.allow_jump or 
        self.levitation < self.settings.dim_jump * 4):
            self.rect.y -= self.settings.dim_jump
            self.levitation -= 1

    def _gravity(self):
        """Simulate gravity for dim"""
        if self.rect.bottom < self.ground_rect.top and self.allow_gravity:
            self.rect.y += self.settings.dim_gravity
        if self.rect.bottom >= self.ground_rect.top:
            self.rect.y = self.ground_rect.top - self.rect_height

    def _stop_jumping(self, command=False):
        """End levitation"""
        # If method called with argument=True, dim stops instantly jumping
        if command:
            self.levitation = 0
        # Check if levitation is 0, stop moving up and reset lev. value to 200
        if self.levitation == 0:
            self.moving_up = False
            self.levitation = self.settings.dim_jump * 4
    
    def check_left_edge(self):
        """Sense when dim reaches left movement limits and pull all objects"""
        # Create variables to use as conditions for clean coding
        con_1 = self.rect.left <= 150
        con_2 = self.rect.left >= 149 - self.settings.dim_speed

        if con_1 and con_2:
            return True
        else:
            return False
    
    def check_right_edge(self):
        """Sense when dim reaches right movement limits and pull all objects"""
        con_1 = self.rect.right >= self.settings.screen_width - 600
        con_2 = (self.rect.right <= self.settings.screen_width - 599 +
        self.settings.dim_speed)

        if con_1 and con_2:
            return True
        else:
            return False

    def blitme(self):
        """Display dim in the specific position"""
        self.screen.blit(self.image, self.rect)