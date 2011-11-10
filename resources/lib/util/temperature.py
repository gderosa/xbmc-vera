class Temperature(object):

    def __init__(self, value=None, unit=None, k=None, c=None, f=None):
        if  value != None:
            if unit.lower() == 'k': self.setk( value )
            if unit.lower() == 'c': self.setc( value )
            if unit.lower() == 'f': self.setf( value )             
        elif k != None:
            self.setk( k ) 
        elif c != None:
            self.setc( c ) 
        elif f != None:
            self.setf( f )
        else:
            self.setk( 0.0 )
    
    def setk(self, value):
        self._k = float(value)
        self._c = self._k - 273.15
        self._f = (self._k * 1.8) - 459.57
    def setc(self, value):
        self._c = float(value)
        self._k = self._c + 273.15
        self._f = self._c * ( 9.0 / 5.0 ) + 32.0
    def setf(self, value):
        self._f = float(value)
        self._k = ( self._f + 459.57 ) / 1.8
        self._c = ( self._f - 32.0 ) * ( 5.0 / 9.0 )  

    def getk(self): return self._k
    def getc(self): return self._c
    def getf(self): return self._f

    k = property(getk, setk) 
    c = property(getc, setc)
    f = property(getf, setf)





