from typing import Type, Union
from jijmodeling.expression.expression import Expression
from jijmodeling.variables.variable import Variable, Element
from jijmodeling.variables.placeholders import ArraySizePlaceholder
from jijmodeling.expression.sum import Sum, SumOperator


class Array:
    """Array object of Variable object.

    Args:
        variable (:class:`jijmodeling.Variable`): element object of Array.
        shape (tuple | int): shape of array.

    Attributes:
        variable (:class:`jijmodeling.Variable`): element object of Array.
        var_label (str): label of variable.
        dim (int): number of indices.
    """
    def __init__(
            self,
            label: str,
            var_type: Type[Variable],
            shape, **var_args) -> None:
        self.label = label
        self.var_type = var_type
        self._shape = shape if isinstance(shape, tuple) else (shape, )
        self.dim = len(self._shape)
        self.var_args: dict = var_args

    @property
    def shape(self):
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                array_size = ArraySizePlaceholder(
                    label=self.label + '_shape_%d' % i,
                    array_label=self.label,
                    array_dim=self.dim,
                    dimension=i
                )
                shape.append(array_size)
            else:
                shape.append(s)
        return tuple(shape)

    def __getitem__(self, key) -> Union[Variable, SumOperator]:
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.label, self.dim))

        subscripts = []
        summation_index = []
        for i, k in enumerate(list(key)):
            if isinstance(k, slice):
                # for syntaxsugar x[:]
                # If a slice [:] is used for a key, 
                # it is syntax-sugar that represents Sum, 
                # and the index is automatically created and assigned.
                # i.e. x[:] => Sum({':x_0': n}, x[':x_0']) 
                # This created index is stored in summation_index as Sum will be added later.
                key_element = Element(':{}_{}'.format(self.label, i))
                summation_index.append((i, key_element))
            elif isinstance(k, str):
                key_element = Element(k)
            elif isinstance(k, (int, Expression)):
                key_element = k
            else:
                raise TypeError('subscripts of Array is `str`, `int`, `Expression` or `slice` object, not {}.'.format(type(k)))

            subscripts.append(key_element)

        variable = self.var_type(
                    label=self.label,
                    subscripts=subscripts,
                    shape=self.shape, **self.var_args)

        # for syntax-sugar x[:]
        for i, ind in summation_index:
            variable = Sum({ind: self.shape[i]}, variable)

        return variable

    def __repr__(self) -> str:
        return self.label
