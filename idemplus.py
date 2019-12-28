import numpy as np
from numbers import Number

class Idemplus:

    def __init__(self, element, zero, one, plus, size=None):
                    
        if isinstance(element, list):

            if all(
                (
                    isinstance(element[i], list)
                    and len(element[i])==len(element[0])
                )
                    
                for i in range(len(element))
            ):
                self.element = np.array(element).astype(np.float)
        
        elif isinstance(element, np.ndarray):

            if len(element.shape) == 1:

                self.element = np.array([element])
            
            elif len(element.shape) == 2:

                self.element = element

            else:

                raise ValueError('Forbidden shape: Use only (n,) and (n,m) arrays.') 

        elif isinstance(element, Number):

            self.element = np.float(element)
            
        elif element == 'identity':
            
            if size is not None:
        
                I = np.full((size,size), zero)
                np.fill_diagonal(I, one)
        
                self.element = I

            else: 

                self.element = one
                
        elif element == 'zero':
            
            if size is not None:
        
                self.element = np.full((size,size), zero)

            else: 

                self.element = zero

        else:

            raise ValueError('Wrong element type: use numbers, lists of lists, and numpy arrays only.')  
            
        
        self.zero = zero

        self.one = one

        self.plus = plus
        
        self.top = -zero
        
        self.bottom = zero
        
        self.own_class = getattr(self, '__class__')

    
    def __eq__(self, other):

        return all([
            #type(self) == type(other),
            self.element == other.element
            if self.isNumber() 
            else (self.element == other.element).all()
        ]) 

    def __le__(self, other):  

        return self + other == other
    
    def __add__(self, other):

        if sameType(self, other):
         
            if self.isNumber():
 
                return self.own_class(
                    element=self.plus(self.element, other.element)
                )
 
            else:
 
                if self.shape == other.shape:
 
                    return self.own_class(
                        element=elementwise(
                            operation=self.plus, 
                            A=self.element, 
                            B=other.element
                        )
                    )
                
                else:
 
                    raise ValueError('Matrices have different shapes.')
    
    def __mul__(self, other):
        
        if sameType(self, other):
            
            if self.isNumber():
                
                return self.own_class(
                    element=self.times(self.element, other.element)
                )

            else:
            
                m,n = self.shape
                p,q = other.shape

                if n == p:

                    M = np.empty(dtype=np.float, shape=(m,q))
                   
                    for i in range(m):

                        for j in range(q):

                            entry = self.own_class(
                                element=self.zero
                            )

                            for k in range(n):

                                c = self.own_class(
                                    element=self.times(
                                        a=self.element[i][k],
                                        b=other.element[k][j],
                                    )
                                )        

                                # checking if c >= entry
                                # according to the present order relation
                                # reminder : a <= b iff a+b=b 
                                # analogously to set inclusion and union

                                if entry + c == c:
                                    
                                    entry = c
                            
                                M[i][j] = entry.element        
                
                class_of_self = getattr(self, '__class__')
                return class_of_self(element=M)

           #else:

           #    raise ValueError(f'Can\'t multiply elements of shape {self.shape} and {other.shape}')
 
        elif any([self.isNumber(), other.isNumber()]):
        # needs a fix, it doesn't contemplate addition with infinities
           return self.own_class(
               element=self.element + other.element
           )

    def __pow__(self, other):
        
        if isinstance(other, Number):
            
            if self.isNumber():
                
                return self.own_class(
                    element=self.element * other
                )
            
            else:
                
                if isinstance(other, int):
                    
                    result = self.own_class(
                        element=self.element
                    )
                    
                    for i in range(1, other):
                        
                        result = result * self
                        
                    return result
                
                else:
                    
                    raise ValueError('Exponents of matrices need to be integers.')

        else:
            
            raise ValueError('Exponents need to be numbers.')
            
    def left_residual(self, X):
        
        if not (type(X) == type(self)):
            
            raise TypeError('You can only residuate by elements of the same algebra.')
        
        if self.isNumber() and X.isNumber():
            
            return self.own_class(
               element=number_residuation(
                   a=self.element, 
                   b=X.element,
                   bottom=self.bottom, 
                   top=self.top
               )
            )
        
        elif self.isMatrix() and X.isMatrix():
            
            return matrix_residuation(self, X, side='left')
        
        elif self.isMatrix() and X.isNumber():
            
            return scalar_residuation(self, X)
        
        else:
            
            class_of_self = getattr(self, '__class__')

            return matrix_residuation(
                A=class_of_self(
                    element=[[self.element]],
                ), 
                B=X, 
                side='left'
            )
    
    def right_residual(self, X):
        
        if not (type(X) == type(self)):
            
            raise TypeError('You can only residuate by elements of the same algebra.')
        
        if self.isNumber() and X.isNumber():
            
            return self.own_classs(
               element= number_residuation(
                   a=self.element, 
                   b=X.element,
                   bottom=self.bottom, 
                   top=self.top
               )
            )
        
        elif self.isMatrix() and X.isMatrix():
            
            return matrix_residuation(self, X, side='right')
        
        elif self.isMatrix() and X.isNumber():
            
            return scalar_residuation(self, X)
        
        else:
            
            class_of_self = getattr(self, '__class__')

            return matrix_residuation(
                A=class_of_self(
                    element=[[self.element]]
                ), 
                B=X, 
                side='right'
            )
            
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
                self.own_class(
                    element=el
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
            
    def kleene_star(self):
        
        if self.isSquared():
            
            if self.max_cycle_mean() < 0:

                result = I

                for i in range(0):
                    
                    pass
            

    def __repr__(self):

        return str(self.element)

class Maxplus(Idemplus):

    def __init__(self, element, size=None):

        super().__init__(
            element=element,
            zero=-np.inf,
            one=0,
            plus=lambda x,y:max(x,y),
            size=size
        )
        
        self.dual_class = Minplus
        
class Minplus(Idemplus):

    def __init__(self, element, size=None):

        super().__init__(
            element=element,
            zero=np.inf,
            one=0,
            plus=lambda x,y:min(x,y),
            size=size
        )
        
        self.dual_class = Maxplus

        
def sameType(a, b):

    return (a.isNumber()==b.isNumber()) or (a.isMatrix()==b.isMatrix())

def elementwise(operation, A, B):

    m,n = A.shape

    M = np.empty(shape=(m,n))

    for i in range(m):

        for j in range(n):

            M[i][j] = operation(A[i][j], B[i][j])

    return M         


def inverse(a, bottom, top):
    
    if a == bottom:
        
        return top
    
    elif a == top:
        
        return bottom
    else:
        
        return -a

#residuating a by b (a/b or b\a)
def number_residuation(a, b, bottom, top):
        
    if b == bottom:
        
        return top if a == bottom else bottom
    
    elif b == top:
        
        return top if a == top else bottom
    
    else:
        
        return a-b
    
def number_residuation_alternative(a, b, bottom, top):
    
    return a*inverse(b) # commutative...
    
#residuating A by B (A/B or B\A if side is 'right' or 'left', respectively)
def matrix_residuation(A, B, side='right'):
    
    x,y = B.shape
    m,n = A.shape
    
    
    
    if (side == 'left' and x == m) or (side =='right' and y == n):

        if isinstance(A, Maxplus):

            B_conj = Minplus(-B.element.transpose())

            doppelganger = Minplus(A.element)

        elif isinstance(A, Minplus):

            B_conj = Maxplus(-B.element.transpose())

            doppelganger = Maxplus(A.element)

        else: 

            raise TypeError("Don't know how to conjugate in this algebra.")
        
        element = (B_conj*doppelganger).element if side == 'left' else (doppelganger*B_conj).element
        class_of_A = getattr(A, '__class__')
        return class_of_A(element)
    
    else:
        
        axis = "rows" if side == 'left' else "columns"
        dim = A.shape[0] if side == 'left' else A.shape[1]
        
        raise ValueError(
            f"Wrongs dimensions. The {axis} index must be {dim}"
        )

    
def scalar_residuation(A, b):
    
    m,n = A.shape
    
    A_copy = np.array(A.element)
    b = b.element
    for i in range(m):
        for j in range(n):
            A_copy[i][j] = number_residuation(
                a=A_copy[i][j], 
                b=b,
                bottom=A.bottom,
                top=A.top
            )
        
    return A.own_classs(
        element=A_copy
    )
    
def semimodule_residuation(A, B):
    
    
    m,n = A.shape
    
    A_copy = np.array(A.element)
    b = b.element
    for i in range(m):
        for j in range(n):
            A_copy[i][j] = number_residuation(
                a=A_copy[i][j], 
                b=B.element[i][j],
                bottom=A.bottom,
                top=A.top
            )
        
    return A.own_class(
        element=A_copy
    )
    
    
    
    
    