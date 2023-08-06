from typing import Union, Dict, Tuple
from numbers import Number
import numpy as np
from jijmodeling.expression.expression import Expression, Number
from jijmodeling.variables.variable import Variable


class ObjectiveVariable(Variable):

    def decode_from_dict(
            self,
            sample: dict,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]], 
            fixed_variables: Dict[str, Union[int, float, Dict[Tuple[int, ...], Union[int, float]]]]):

        shape = self._shape_value(placeholder)
        array_value = np.full(shape, fill_value=np.nan)

        def set_value(subscript_values: list):
            if len(subscript_values) == self.dim:
                # When the number of `subscript_values` equals dimension of the array,
                # the elements of the array can finally be accessed.
                # The result of accessing and decoding the elements is stored in `array_value`.
                array_value[tuple(subscript_values)] = self._decode_element(
                                                            sample,
                                                            placeholder, 
                                                            fixed_variables, 
                                                            subscript_values)
            else:
                # When `len(subscript_values) < self.dim`,
                # the values of all indices to access elements
                # have not yet been determinded.
                # Next, we will determined the value of the next dimension's subscript
                # due to move on to the next recursive step.
                fixed_num = len(subscript_values)
                for i in range(shape[fixed_num]):
                    new_fixed = subscript_values + [i]
                    set_value(new_fixed)
        set_value([])

        return {self.label: array_value}


    def _decode_element(self, 
                        sample: dict, 
                        placeholder: Dict[str, Union[int, float, np.ndarray, list]], 
                        fixed_variables: Dict[str, Union[int, float, Dict[Tuple[int, ...], Union[int, float]]]], 
                        subscript_values: list):
        label = self.label + ''.join(['[{}]'.format(s) for s in subscript_values])
        if self.label in fixed_variables:
            return np.array(fixed_variables[self.label])[tuple(subscript_values)]
        elif label in sample:
            return sample[label]

        return np.nan


    def _shape_value(self, 
        placeholder: Dict[str, Union[int, float, np.ndarray, list]]={}) -> Tuple[int, ...]:
        def script_to_value(obj):
            if isinstance(obj, Expression):
                return int(obj.calc_value({}, placeholder, {}))
            else:
                return obj
        shape = tuple([script_to_value(i) for i in self.subscripts])
        return shape



class Binary(ObjectiveVariable):
    def __init__(
            self,
            label: str,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        super().__init__(label, children=[], subscripts=subscripts, shape=shape)

    def __mul__(self, other):
        # x \in {0, 1} => x^2 = x
        if isinstance(other, self.__class__) and other.label == self.label:
            if self.subscripts == other.subscripts:
                return self
        return super().__mul__(other)

    def __pow__(self, other):
        if isinstance(other, Number) and int(other) != other:
            raise ValueError("Binary variable's exponent is only integer.")
        return self.__class__(self.label, self.subscripts.values, shape=self.shape)

    def __rtruediv__(self, other):
        raise ZeroDivisionError("'Binary' can take zero")



class Spin(Variable):
    def __init__(self, label: str, subscripts: list=[], shape:Union[list, tuple]=[]):
        super().__init__(label, children=[], subscripts=subscripts, shape=shape)

    def __mul__(self, other):
        # s \in \{1, -1\} => s*s = 1
        if isinstance(other, self.__class__) and other.label == self.label:
            if self.subscripts == other.subscripts:
                return 1
        return super().__mul__(other)


class LogEncInteger(Variable):
    r"""Log encoded integer

    .. math::
        x = \frac{\text{upper}-\text{lower}}{2^l} \sum_{l=0}^{\text{bits}-1} 2^l s_l + \text{lower},~(s_l \in \{0, 1\}~ \forall l)

    .. math::
        \text{lower} \leq x \leq \text{upper}
    """
    def __init__(
            self,
            label: str,
            lower: Union[int, Number],
            upper: Union[int, Number],
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        if not isinstance(lower, Expression):
            lower = Number(lower, 'int')
        if not isinstance(upper, Expression):
            upper = Number(upper, 'int')
        children = [lower, upper]
        super().__init__(label, children=children, subscripts=subscripts, shape=shape)

    @property
    def lower(self) -> Expression:
        return self.children[0]

    @property
    def upper(self) -> Expression:
        return self.children[1]


class DisNum(Variable):
    r"""Discreated number class
    
    .. math::
        x = \frac{\text{upper}-\text{lower}}{2^{\text{bits}}-1} \sum_{l=0}^{\text{bits}-1} 2^l s_l + \text{lower},~
        (s_l \in \{0, 1\}~ \forall l)

    .. math::
        \text{lower} \leq x \leq \text{upper}
    """

    def __init__(
            self,
            label: str,
            lower: Union[float, Number] = 0.0,
            upper: Union[float, Number] = 1.0,
            bits: Union[int, Number] = 3,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        lower = Number(lower) if not isinstance(lower, Expression) else lower
        upper = Number(upper) if not isinstance(upper, Expression) else upper
        bits = Number(bits, 'int') if not isinstance(bits, Expression) else bits
        children = [lower, upper, bits]
        super().__init__(label, children=children, subscripts=subscripts, shape=shape)

    @property
    def lower(self) -> Expression:
        return self.children[0]

    @property
    def upper(self) -> Expression:
        return self.children[1]

    @property
    def bits(self) -> Expression:
        return self.children[2]