class Settings:
    """A class to store all settings of the main game"""

    def __init__(self):
        """Initialize all settings"""
        # Screen settings
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (240, 100, 10)

        # Ground settings
        self.ground_width = self.screen_width
        self.ground_height = self.screen_height // 5
        self.ground_color = (120, 230, 30)

        # Dim's settings
        self.dim_speed = 7
        self.dim_jump = 12
        self.dim_gravity = 7

        # Block settings
        self.block_width = 100
        self.block_height = self.block_width
        self.block_color = (0, 255, 0)

        # Bean settings
        self.bean_speed = 2