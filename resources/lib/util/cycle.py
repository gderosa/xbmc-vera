class Cycle(object):

    def __init__(self, l=[]): # should work with tuples too
        self.l = l
        self.i = 0

    def get_current(self): return self.l[ self.i ] 

    def set_current(self, value):
        for i in range(len(self.l)):
            if self.l[i] == value:      
                self.i = i
                return True
        return False

    current = property(get_current, set_current)

    def cycle(self):
        self.i += 1
        if self.i < len( self.l ): pass
        else:
            self.i = 0

        return self.current

    def cycle_back(self):
        self.i -= 1
        if self.i < 0:
            self.i = len( self.l ) - 1

        return self.current


