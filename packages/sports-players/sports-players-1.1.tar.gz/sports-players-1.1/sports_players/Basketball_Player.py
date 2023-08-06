from .General_Player import Player
import pandas
class BasketballPlayer(Player):
    """
    Basketball player class that tracks all information
    regrading a basketball player.

    Attributes:
        full_name (str) representing the full name of the player
        first_name (str) representing the the first name of the player
        last_name (str) representing the last name of the player
    """
    def __init__(self, full_name=None, first_name=None, last_name=None):
        super().__init__(full_name=full_name, first_name=first_name, last_name=last_name)
        self._games = None

    @property
    def games(self):
        """       
        Return the games of the player 
        """
        return self._games

    @games.setter
    def games(self, value):
        """ 
        The games of the player represented as a pandas dataframe.
        
        games (pandas.Dataframe) representing the games of the player in form of
        {'points': [], 'rebounds': [], assists: []},
        points: int
        rebounds: int
        assists: int
        Example:
        {'points': [20, 15], 'rebounds': [5, 9], assists: [3, 4]}
        
        """
        if isinstance(value, pandas.DataFrame):
            if 'points' not in value.columns: # if there isn't a points column
                raise ValueError("Missing 'points' column")
            elif 'rebounds' not in value.columns: # if there isn't a rebounds column
                raise ValueError("Missing 'rebounds' column")
            elif 'assists' not in value.columns: # if there isn't a assist column
                raise ValueError("Missing 'assists' column")
            else:
                self._games = value
        elif value is None:
            self._games = None
        else:
            raise TypeError("games must be a dataframe")

    def ppg(self):
        """
        Return points per game average
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['points'].mean()
    
    def apg(self):
        """ 
        Return assist per game average 
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['assists'].mean()

    def rpg(self):
        """
        Return rebounds per game average
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['rebounds'].mean()

    def points_max(self):
        """ 
        Return game with highest points sby player
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['points'].max()

    def assists_max(self):
        """ 
        Return game with highest assist by player
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['assists'].max()

    def rebounds_max(self):
        """ 
        Return game with highest rebounds by player
        """
        if self._games is None:
            raise TypeError('games has not been set')
        return self._games['rebounds'].max()

    def avg_through(self, start, end):
        """ 
        Return averages by player through number of games
        in the form of a pandas Series
        """
        if self._games is None:
            raise TypeError('games has not been set')
        if start is None or end is None:
            raise ValueError('start and end must be provided')
        if not isinstance(start, int):
            raise TypeError('start must be an integer')
        if not isinstance(end, int):
            raise TypeError('end must be an interger')
        if start < 0 or end > len(self._games):
            raise  ValueError('Index out of range')
        if start >= end:
            raise ValueError('start must be less than end')
        return self._games.loc[start:end].mean()
