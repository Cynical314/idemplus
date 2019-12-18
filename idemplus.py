import numpy as np
from numbers import Number


class Idemplus:

    def __init__(self, element, zero, one, plus):

        
        if isinstance(element, list):

            if all(
                (
                    isinstance(element[i], list)
                    and len(element[i])==len(element[0])
                )
                    
                for i in range(len(element))
            ):
                self.element = np.array(element)
        
        elif isinstance(element, np.ndarray):

            if len(element.shape) == 1:

                self.element = np.array([element])
            
            elif len(element.shape) == 2:

                self.element = element

            else:

                raise ValueError('Forbidden shape: Use only (n,) and (n,m) arrays.') 

        elif isinstance(element, Number):

            self.element = np.float(element)

        else:

            raise ValueError('Wrong element type: use numbers, lists of lists, and numpy arrays only.')  
            
        
        self.zero = zero

        self.one = one

        self.plus = plus
        
        self.minimum = lambda a,b: self.times(a,b)-self.plus(a,b)

    
    def __eq__(self, other):

        return all([
            type(self) == type(other),
            self.element == other.element, 
            self.shape == other.shape
        ]) 

    def __add__(self, other):

       if sameType(self, other):

           if self.isNumber():

               return Idemplus(
                   element=self.plus(self.element, other.element),
                   zero=self.zero,
                   one=self.one,
                   plus=self.plus
               )

           else:

               if self.shape == other.shape:

                   return Idemplus(
                       element=elementwise(
                           operation=self.plus, 
                           A=self.element, 
                           B=other.element
                       ),
                       zero=self.zero,
                       one=self.one,
                       plus=self.plus
                   )
               
               else:

                   raise ValueError('Matrices have different shapes.')
    
    def __mul__(self, other):
        
        if sameType(self, other):
            
            if self.isNumber():
                
                return Idemplus(
                    element=self.times(self.element, other.element),
                    zero=self.zero,
                    one=self.one,
                    plus=self.plus
                )

            else:
            
                m,n = self.shape
                p,q = other.shape

                if n == p:

                    M = np.empty(dtype=np.float, shape=(m,q))
                   
                    for i in range(m):

                        for j in range(q):

                            entry = Idemplus(
                                element=self.zero,
                                zero=self.zero,
                                one=self.one,
                                plus=self.plus
                            )

                            for k in range(n):

                                c = Idemplus(
                                    element=self.times(
                                        a=self.element[i][k],
                                        b=other.element[k][j],
                                    ),
                                    zero=self.zero,
                                    one=self.one,
                                    plus=self.plus
                                )        

                                # checking if c >= entry
                                # according to the present order relation
                                # reminder : a <= b iff a+b=b 
                                # analogously to set inclusion and union

                                if entry + c == c:
                                    
                                    entry = c
                            
                                M[i][j] = entry.element        
            
                return Idemplus(element=M, zero=self.zero, one=self.one, plus=self.plus)

           #else:

           #    raise ValueError(f'Can\'t multiply elements of shape {self.shape} and {other.shape}')
 
        elif any([self.isNumber(), other.isNumber()]):
        # needs a fix, it doesn't contemplate addition with infinities
           return Idemplus(
               element=self.element + other.element,
               zero=self.zero,
               one=self.one,
               plus=self.plus  
           )

    def __pow__(self, other):
        
        if isinstance(other, Number):
    
            return Idemplus(
                element=self.element * other,
                zero=self.zero,
                one=self.one,
                plus=self.plus  
            )

        else:
            
            raise ValueError('Exponents need to be numbers.')
            
    def left_residual(self, X):
        
        if not (type(X) == type(self)):
            
            raise TypeError('You can only residuate by elements of the same algebra.')
        
        
        x,y = X.shape
        m,n = self.shape
        if x == m:
            
            if isinstance(self, Maxplus):
                
                X_conj = Minplus(-X.element.transpose())

                doppelganger = Minplus(self.element)
                
            elif isinstance(self, Minplus):
                
                X_conj = Maxplus(-X.element.transpose())

                doppelganger = Maxplus(self.element)
                
            else: 
                
                raise TypeError("Don't know how to conjugate in this algebra.")
 
    
            return Idemplus(
               element= (X_conj*doppelganger).element,
               zero=self.zero,
               one=self.one,
               plus=self.plus
            )
        
        else:
            
            raise ValueError(f'Wrong dimensions. The row dimensione must be {self.shap[0]}.')       
            
            
    def isNumber(self):

        return isinstance(self.element, Number)

    def isMatrix(self):

        return isinstance(self.element, np.ndarray)

    def isSquared(self):

        return self.isMatrix() and (self.shape[0] == self.shape[1])

    def isValid(self):

        return self.isNumber() or self.isMatrix()

    @property
    def shape(self):

        return self.element.shape if self.isMatrix() else 0

    def times(self, a, b):

        if a == self.zero or b == self.zero:

            return self.zero
        
        else:

            return a+b

    def diagonal(self, to_obj=True):

        if self.isNumber() or not self.isSquared():
            
            raise TypeError('Numbers and rectangles don\'t have a diagonal.')

        else:

            dg = self.element.diagonal()

        if to_obj:

            return [
                Idemplus(
                    element=el,
                    zero=self.zero,
                    one=self.one,
                    plus=self.plus
                )

                for el in dg
            ]

        else:

            return dg
 


    def trace(self, to_obj=True):

        if self.isNumber() or not self.isSquared():
            
            raise TypeError('Numbers and rectangles don\'t have a trace.')

        else:
            
            dg = self.diagonal()

            tr = dg[0]
            for a in dg[1:]:
                tr = tr + a        

        if to_obj:
    
            return tr

        else:

            return tr.element

    def max_cycle_mean(self, to_obj=True):

        if self.isNumber():
            
            return self if to_obj else self.element 

        elif not self.isSquared():
            
            raise TypeError('Rectangles don\'t have a maximum cycle mean, as they aren\'t adjacency matrices of graphs.')

        else:

            n = self.shape[0]

            maxcm = self.trace()
            for k in range(2,n+1):
                maxcm = maxcm + ((self**k).trace())**(1/k)

            if to_obj:
                
                return maxcm

            else:

                return maxcm.element
            

    def __repr__(self):

        return str(self.element)

class Maxplus(Idemplus):

    def __init__(self, element):

        super().__init__(
            element=element,
            zero=-np.inf,
            one=0,
            plus=lambda x,y:max(x,y)
        )         

class Minplus(Idemplus):

    def __init__(self, element):

        super().__init__(
            element=element,
            zero=np.inf,
            one=0,
            plus=lambda x,y:min(x,y)
        )         



def sameType(a, b):

    return (a.isNumber()==b.isNumber()) or (a.isMatrix()==b.isMatrix())

def elementwise(operation, A, B):

    m,n = A.shape

    M = np.empty(shape=(m,n))

    for i in range(m):

        for j in range(n):

            M[i][j] = operation(A[i][j], B[i][j])

    return M         


