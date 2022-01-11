class Stats:
    """Track statistics for the game."""

    def __init__(self, program):
        """Initalize statistics"""
        self.settings = program.settings
        self._reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
        self._load_stats()

    def _reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.score = 0
        self.secret_score = 0

    def save_stats(self):
        filename = 'high_score.json'

        with open(filename, 'w') as f:
            f.write(str(self.high_score))
    
    def _load_stats(self):
        try:
            filename = 'high_score.json'

            with open(filename) as f:
                loaded_score = f.read()
                self.high_score = int(loaded_score)
        except FileNotFoundError:
            pass