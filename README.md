**idemplus** is a python module for computations in (linear) maxplus and minplus algebras, modelled by classes **Maxplus** and **Minplus**, respectively. They are coded as subclasses of class **Idemplus**, a general class for any algebra over an idempotent semifield over the reals and sum + as its product and any idempotent operation as its addition.
Regardless of dimensions, scalars and matrices are represented as instances of the same class.



```python
import idemplus
from idemplus import Idemplus, Maxplus, Minplus
import numpy as np

a = Maxplus(3)
B = Maxplus([
    [1,2],
    [3,-np.inf]
])
```

The class handles the product between elements of compatible dimensions


```python
a*B
```




    [[  4.   5.]
     [  6. -inf]]



and alerts you when something goes wrong.


```python
c = Maxplus([
    [1],
    [2]
])

c*B
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-4-ecee9e0fb6cf> in <module>
          4 ])
          5 
    ----> 6 c*B
    

    ~/idempotency/idemplus.py in __mul__(self, other)
        179                 else:
        180 
    --> 181                     raise ValueError(f'Can\'t multiply elements of shape {self.shape} and {other.shape}')
        182 
        183         elif any([self.isNumber(), other.isNumber()]):


    ValueError: Can't multiply elements of shape (2, 1) and (2, 2)



```python
c.transpose()*B
```




    [[5. 3.]]



Note that the only ways allowed to instantiate a matrix (including row and column vectors) is either passing a list of lists with appropriate dimensions or as a numpy.array.


```python
v1 = Maxplus([
    [1,0,0]
])

w3 = Maxplus([
    [0],
    [0],
    [3]
])

arr = np.array([
    [1,2],
    [-1,4]
])

v = Minplus(arr)

print(v)
print(type(v))
```

    [[ 1  2]
     [-1  4]]
    <class 'idemplus.Minplus'>


The canonical completions of the maxplus (minplus) semifield is correspond precisely to the completed maxplus (minplus) and minplus (maxplus) idempotent semifields. 


```python
A = Maxplus([
    [1,2],
    [3,4]
])

B = Maxplus([
    [0,4],
    [-3,9]
])
```

$A$ and $B$ can be multiplied as instances of $\textbf{Maxplus}$


```python
A*B
```




    [[ 1. 11.]
     [ 3. 13.]]



Any element of one algebra can thought of as an element of the other or as having a doppelganger in it.


```python
print(A.doppelganger())
print(type(A.doppelganger()))
```

    [[1. 2.]
     [3. 4.]]
    <class 'idemplus.Minplus'>



```python
A.doppelganger()*B.doppelganger()
```




    [[-1.  5.]
     [ 1.  7.]]



The class **Idemplus** provides generalised support for residuation to the left (B\A)


```python
A.left_residual(B)
```




    [[ 1.  2.]
     [-6. -5.]]




```python
A.left_residual(B)
```




    [[ 1.  2.]
     [-6. -5.]]



and to the right (A/B)


```python
A.right_residual(B)
```




    [[-2. -7.]
     [ 0. -5.]]



It can be verified as an exercise that, for these values of A and B, B\*(B\A)=A but (A/B)\*B < B, a fact that has has strong links to the existence of solutions of some systems of linear equations over this algebra.

An element can be inverted by using the *inverse* method.


```python
print(A.inverse())
print(a.inverse())
```

    [[-1. -2.]
     [-3. -4.]]
    -3.0


The inverse of a matrix is calculating applying inversion of elements over the maxplus or minplus semifield, elementwise. 
Residuating A by B can be thought of as multiplying A by the appropriate conjugate of B in the dual algebra, which over maxplus and minplus is is nothing but the transpose with inverted elements. 


```python
B.right_conjugate()
```




    [[ 0.  3.]
     [-4. -9.]]




```python
A.right_residual(B)
```




    [[-2. -7.]
     [ 0. -5.]]




```python
A.doppelganger()*B.right_conjugate().doppelganger()
```




    [[-2. -7.]
     [ 0. -5.]]



Beware, the latter is an instance of *Minplus*.
