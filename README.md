$\textit{idemplus}$ is a python module for computations in linear algebras over $\mathbb{R}_{max,+}$ and $\mathbb{R}_{min,+}$, modelled by classes $\textbf{Maxplus}$ and $\textbf{Minplus}$, respectively. They are coded as subclasses of class $\textbf{Idemplus}$, a general class for any algebra over an idempotent semifield with values in $\mathbb{R}$ and sum $+$ as its product $\otimes$, where the addition $\oplus$ can be any idempotent operation. 
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

Moreover, the class handles the product between elements of compatible dimensions.


```python
a*B
```




    [[  4.   5.]
     [  6. -inf]]




```python
It alerts you when something goes wrong.
```


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


The algebras over $\mathbb{R}_{max,+}$ and $\mathbb{R}_{min,+}$ can be extended naturally when the two idempotent semifields are replaced by their canonical completions $\overline{\mathbb{R}}_{max,+}$ and $\overline{\mathbb{R}}_{min,+}$, because the latter are the lower (upper) and upper (lower) canonical completion of $\mathbb{R}_{max,+}$ ($\mathbb{R}_{min,+}$) as a lattice-ordered semifield.


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



but they have a doppelganger in $\textbf{Minplus}$, that multiply as it's rule for instances of $\textbf{Minplus}$.


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


