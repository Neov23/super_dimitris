import pygame

class Sun:
    """Initialize the sun"""

    def __init__(self, program):
        self.screen = program.screen
        self.screen_rect = self.screen.get_rect()

        # Get image and create rect
        self.image = pygame.image.load('images/sun.png')
        self.rect = self.image.get_rect()

        # Set its static position
        self.rect.top = self.screen_rect.top + 30
        self.rect.right = self.screen_rect.right - 30
    
    def blitme(self):
        """Display sun in specific position"""
        self.screen.blit(self.image, self.rect)