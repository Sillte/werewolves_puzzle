""" Result classes.
"""


class AbstractResult(object):
    """ This class represents the claim of the other players.   
    """

    def __init__(self):
        pass

    @classmethod
    def get_id(cls):
        raise SyntaxError("Please Implement.")


class WhiteResult(AbstractResult):
    def __init__(self):
        pass

    @classmethod
    def get_id(cls):
        return "white"


class BlackResult(AbstractResult):
    def __init__(self):
        pass

    @classmethod
    def get_id(cls):
        return "black"
