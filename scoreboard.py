import pygame.font

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, program):
        """Initialize scorekeeping attributes"""
        self.program = program
        self.screen = program.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = program.settings
        self.stats = program.stats

        # Font settings for scoring information
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 38)

        # Prepare the initial score images.
        self._set_score()
        self._set_secret_score()
        self._set_high_score()

    def _set_score(self):
        """Turn the score into a rendered image"""
        score_str = str(f"{self.stats.score}/50")
        self.score_image = self.font.render(score_str, True,
            self.text_color, self.settings.bg_color)
        
        # Display the score at the top left of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = (self.screen_rect.left + 10 + 
            self.settings.block_width)
        self.score_rect.top = (self.screen_rect.top + 
            self.settings.block_width // 2 -
            self.score_rect.height // 2)

    def _set_secret_score(self):
        """Turn the score of secret burgers into a rendered image"""
        secret_score_str = str(f"Secret:  {self.stats.secret_score}/1")
        self.secret_score_image = self.font.render(secret_score_str, True,
            self.text_color, self.settings.bg_color)
        
        # Display the score between score and highscore
        self.secret_score_rect = self.secret_score_image.get_rect()
        self.secret_score_rect.left = self.score_rect.right + 100
        self.secret_score_rect.top = (self.screen_rect.top + 
            self.settings.block_width // 2 -
            self.score_rect.height // 2)
        
    def _set_high_score(self):
        """Turn the high score into a rendered image."""
        high_score_str = str(f"High Score: {self.stats.high_score}/50")
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = (self.screen_rect.top +
            self.settings.block_width // 2 -
            self.score_rect.height // 2)
    
    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._set_high_score()
    
    def show_score(self):
        """Draw scores, level and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.secret_score_image, self.secret_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)