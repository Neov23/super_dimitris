import pygame
from pygame.sprite import Sprite

class Burger(Sprite):
    """A class to represent a burger"""

    def __init__(self, program):
        """Initialize burger and get its rect"""
        super().__init__()
        self.screen = program.screen

        # Load dim's image and get its rect
        self.image = pygame.image.load('images/burger.png')
        self.rect = self.image.get_rect()
    
    def blitme(self):
        """Display dim in the specific position"""
        self.screen.blit(self.image, self.rect)