class Temperature(object):

    def __init__(self, value=None, unit='K', k=None, c=None, f=None):
        if  value != None:
            if unit == 'K': self.setk( value )
            if unit == 'C': self.setc( value )
            if unit == 'F': self.setf( value )            
            self.unit = unit
        elif k != None:
            self.setk( k ) 
            self.unit = 'K'
        elif c != None:
            self.setc( c ) 
            self.unit = 'C'
        elif f != None:
            self.setf( f )
            self.unit = 'F'
        else:
            self.__init__( 0.0 ) 
    
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
    def setvalue(self, value):
        if      self.unit == 'K': self.setk(value)
        elif    self.unit == 'C': self.setc(value)
        elif    self.unit == 'F': self.setf(value)

    def getk(self): return self._k
    def getc(self): return self._c
    def getf(self): return self._f    
    def getvalue(self):
        if self.unit == 'K': return self.getk()
        if self.unit == 'C': return self.getc()
        if self.unit == 'F': return self.getf() 

    k       = property( getk,       setk        )  
    c       = property( getc,       setc        )
    f       = property( getf,       setf        )
    value   = property( getvalue,   setvalue    )





