class Player:
    
    def __init__(self, full_name=None, first_name=None, last_name=None):
        """
        A base class for a sports player.

        Attributes:
        full_name (str) representing the full name of the player
        first_name (str) representing the the first name of the player
        last_name (str) representing the last name of the player
        """
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name