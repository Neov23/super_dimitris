import pygame

class Ground:
    """A class to represent the ground"""
    def __init__(self, program):
        """Create the rect and set his position"""
        self.screen = program.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = program.settings
        self.color = self.settings.ground_color

        # Create the ground and get its rect
        self.rect = pygame.Rect(0, 0, self.settings.ground_width,
            self.settings.ground_height)
        self.rect.bottom = self.screen_rect.bottom

    def display_ground(self):
        """Display ground in specific position"""
        pygame.draw.rect(self.screen, self.color, self.rect)