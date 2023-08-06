sports-players
===================================

This is project created by Frantz Paul.

``sports-players`` a fun way to represent sports players as objects.

# Installation

pip install sports_players

.. code:: python

    from sports_players import BasketballPlayer

    import pandas as pd

    player = BasketballPlayer(full_name="Lebron James")
    data = {'points': [20, 10, 10, 10], 'rebounds': [4, 3, 2, 10], 'assists': [2, 4, 7, 2]}

    games = pd.DataFrame(data=self.data)
    player.games = self.games

    print(player.ppg()) # returns player points per game
    print(player.apg()) # returns player assists per game

``sports-players`` requires the pandas library and is installed
when you install the package.