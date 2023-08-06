from .Operations import Operations

class Add(Operations):
    '''
    This class inherit the features from Operations class.
    The goal od this class is to add 2 numbers.
    '''

    '''
    Initializing the variable in memory
    '''
    def __init__(self, n1, n2):
        Operations.__init__(self, n1, n2)

    '''
    This method add 2 numbers
    '''
    def soma (n1, n2):
        return n1+n2