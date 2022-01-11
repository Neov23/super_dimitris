import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    """A class to represent a block"""

    def __init__(self, program):
        """Initialize the block's rect and set its position"""
        super().__init__()
        self.screen = program.screen
        self.settings = program.settings
        self.color = self.settings.block_color

        # Create block's rect
        self.rect = pygame.Rect(0, 0, self.settings.block_width,
            self.settings.block_height)
    
    def display_block(self):
        """Display the block in specific position"""
        pygame.draw.rect(self.screen, self.color, self.rect)