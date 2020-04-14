from idemplus import Idemplus, Minplus, Maxplus
import numpy as np
import pandas as pd
import concepts
import datetime

class Context:
    
    def __init__(self, matrix, object_names=None, attribute_names=None):
        
        if isinstance(matrix, Idemplus) and type(matrix.shape) == type((1,2)):
            
            if type(object_names) == type(None):
                
                object_names = range(matrix.shape[0])
                
            if type(attribute_names) == type(None):
                
                attribute_names = range(matrix.shape[1])
            
            len_of_label_lists = (len(object_names), len(attribute_names))
            
            if len_of_label_lists != matrix.shape:
                
                raise ValueError("Labels lists don't match the matrix's dimensions.")
        
        else:
            
            raise TypeError("The matrix needs to be over an idempotent semifield")
            
        self.matrix = matrix
        self.object_names = list(object_names)
        self.attribute_names = list(attribute_names)
        self.own_type = matrix.own_class
        
    @property
    def shape(self):
        
        return self.matrix.shape
        
    def extent(self, column, phi):
                
        Algebra = self.matrix.own_class
        
        phi = Algebra(phi)
        
        if isinstance(column, self.own_type) and column.shape == (self.matrix.shape[1],1):

            attribute_vector = column
        
        elif str(column) in self.attribute_names:
            
            j = list(self.attribute_names).index(column)
            
            attribute_vector = Algebra([[self.matrix.one if k == j else self.matrix.zero] for k in range(self.matrix.shape[1])])
            
        else:
            
            raise ValueError("The 'column' field is neither a known attribute nor an appropriate column vector.")
        
        # option..
        # 
        # context_dg = context.doppelganger()
        # attribute_vector_dg = attribute_vector.doppelganger()
        # phi_dg = phi.doppelganger()
        # 
        # return (phi_dg*attribute_vector_dg.right_conjugate()*context_dg.right_conjugate()).doppelganger()

        return phi.right_residual((self.matrix.inverse())*attribute_vector)
        
    def intent(self, row, phi):
        
        Algebra = self.matrix.own_class
        
        phi = Algebra(phi)
        
        if isinstance(row, self.own_type) and row.shape == (1,self.matrix.shape[0]):
            
            object_vector = row
        
        elif str(row) in self.object_names:
            
            i = list(self.object_names).index(row)
            
            object_vector = Algebra([[self.matrix.one if k == i else self.matrix.zero for k in range(self.matrix.shape[0])]])
            
        else:
            
            raise ValueError("The 'row' field is neither a known attribute nor an appropriate row vector.")
        
        
        # option..
        #
        # context_dg = context.doppelganger()
        # object_vector_dg = object_vector.doppelganger()
        # phi_dg = phi.doppelganger()
        #
        # return (context_dg.right_conjugate()*object_vector_dg.right_conjugate()*phi_dg).doppelganger()
        
        return phi.left_residual(object_vector*(self.matrix.inverse()))
    
    def closure_of(self, vector, phi):
        
        if isinstance(vector, self.own_type) :
            
            if not (vector.shape == (1, self.shape[1]) or vector.shape == (self.shape[0], 1)):
                
                raise ValueError(f"The shape {vector.shape} of the vector {vector} is not compatible with a context of shape {self.shape}")

            
            if vector.shape == (1, self.shape[1]) or vector in self.object_names:
            
                int_ = self.intent(row=vector, phi=phi)
                ext_ = self.extent(column=int_, phi=phi)
            
            
            elif vector.shape == (self.shape[0], 1) or vector in self.attribute_names:
                
                ext_ = self.extent(column=vector, phi=phi)
                int_ = self.intent(row=ext_, phi=phi)
            
            else:

                raise TypeError(f"The closure of a vector of type {type(vector)} cannot be computed w.r.t. a context of type {self.own_type}")
         
        if vector in self.object_names or vector in self.attribute_names:
            
            if vector in self.object_names:
                
                int_ = self.intent(row=vector, phi=phi)
                ext_ = self.extent(column=int_, phi=phi)
                
            
            if vector in self.attribute_names:
                
                ext_ = self.extent(column=vector, phi=phi)
                int_ = self.intent(row=ext_, phi=phi)
        
        else:
            
            raise ValueError(f"The value '{vector}' is not a known label.")
        
        return Concept(
            extent=ext_,
            intent=int_,
            phi=phi
        )
            
    def structural_boolean_table(self, phi, asDf=True):

        from datetime import datetime
        
        
        fca_context = pd.DataFrame(index=self.object_names, columns=self.attribute_names)
    
        attribute_concepts = dict()
        
        m,n = self.shape
        
        i = 1
        for row in self.object_names:
            
            current_object_concept = self.closure_of(row, phi)
            
            j = 1
            for col in self.attribute_names:
                
                if col not in attribute_concepts:
                    attribute_concepts[col] = self.closure_of(col, phi)
                    
                fca_context.loc[row, col] = current_object_concept <= attribute_concepts[col]
                
                percentage = 100 * ((i-1)*n + j)/(m*n)
                
                if percentage % 10 == 0:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print(f"Current state: {percentage}%; Current Time = {current_time}")
                
                j = j + 1
                
            i = i + 1
        
        if asDf:
        
            return fca_context
            
        else:
        
            return fca_context.values
        
    def structural_context(self, phi):
        
        fca_table = self.structural_boolean_table(self, phi=phi, asDf=False)
        
        return Context(
            matrix=fca_table,
            object_names=self.object_names,
            attribute_names=self.attribute_names
        )
    
    def show_structural_lattice(self, phi, verbose=False):
        
        fca_context = self.structural_boolean_table(phi=phi)
        
        objects = [str(a) for a in fca_context.index.tolist()]
        properties = [str(p) for p in list(fca_context)]
        bools = list(fca_context.fillna(False).astype(bool).itertuples(index=False, name=None))

        c_ = concepts.Context(objects, properties, bools)

        l= c_.lattice

        if verbose:
            print(f"The lattice has {len(l)} concepts.")
            
        return l

class Concept:
    
    def __init__(self, extent, intent, phi=None):
        
        if all([
            type(extent) == type(intent),
            isinstance(extent, Idemplus),
            extent.shape[0] == 1,
            intent.shape[1] == 1
        ]):
            
            self.extent = extent
            self.intent = intent
            self.phi = phi
            
        else:
            
            raise ValueError(f"{extent} and {intent} cannot be the extent and intent of a concept, respectively.")
            
    def __le__(self, other):
        
        if type(self) == type(other):
            
            return self.extent <= other.extent
        
        else:
            
            raise TypeError(f"{other} is not comparable to {self}")
            
    
        
        
