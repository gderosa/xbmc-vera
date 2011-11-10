class Ring:

    def __init__(self, l=[]): # should work with tuples too
        self.l = l
        self.i = 0

    def get(self): return self.l[ self.i ] 

    def next(self):
        self.i += 1
        if self.i < len( self.l ): pass
        else:
            self.i = 0

        return get()

    def previous(self):
        self.i -= 1
        if self.i < 0:
            self.i = len( self.l ) - 1

        return get()


