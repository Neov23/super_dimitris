import pygame.font

class Button:

    def __init__(self, program, msg, width=400, height=100, textsize=48):
        """Initialize button attributes"""
        self.screen = program.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties for the button
        self.width, self.height = width, height
        self.button_color = (60, 60, 60)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, textsize)

        # Build the button's rect and position it in the center of the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._set_msg(msg)

    def _set_msg(self, msg):
        """Render the text in msg into an image and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw the button with the message in it"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)