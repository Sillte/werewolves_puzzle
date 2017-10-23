""" Player Class.
"""
from result import WhiteResult


class Player(object):
    """ Abstract class for players.
    The player is identified **index**. 
    Claims about other players are stored in  **result**. 
    All players impliticly claim that one's own color is white. 

    """
    def __init__(self, index):
        self.result = dict()
        self.index = index
        self.result[index] = WhiteResult.get_id()
    
    @classmethod
    def get_name(cls):
        return "player"
