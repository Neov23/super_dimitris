import pygame

class BigBurger:
    """A class to represent the final big burger"""

    def __init__(self, program):
        """Initialize burger and get its rect"""
        self.screen = program.screen
        self.settings = program.settings

        # Load dim's image and get its rect
        self.image = pygame.image.load('images/big_burger.png')
        self.rect = self.image.get_rect()

        self.initialize_position()

    def initialize_position(self):
        """Initialize big burger's position"""
        self.rect.x = self.settings.block_width * 5 + (
            self.settings.block_width * 177)
        self.rect.y = (self.settings.screen_height - 
            self.settings.ground_height - self.rect.height)
    
    def blitme(self):
        """Display dim in the specific position"""
        self.screen.blit(self.image, self.rect)