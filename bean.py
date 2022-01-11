import pygame
from pygame.sprite import Sprite

class Bean(Sprite):
    """A class to represent a bean"""

    def __init__(self, program):
        """Initialize bean and get its rect"""
        super().__init__()
        self.screen = program.screen
        self.settings = program.settings

        # Load dim's image and get its rect
        self.image = pygame.image.load('images/bean.png')
        self.rect = self.image.get_rect()

        # Variable to change bean's movement direction
        self.direction = 1

    def update(self):
        """Move bean left or right"""
        self.rect.x += self.settings.bean_speed * self.direction
    
    def blitme(self):
        """Display dim in the specific position"""
        self.screen.blit(self.image, self.rect)