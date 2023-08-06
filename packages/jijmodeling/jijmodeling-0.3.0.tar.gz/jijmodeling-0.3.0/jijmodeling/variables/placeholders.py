from typing import Union, Dict
import numpy as np
from jijmodeling.variables.variable import Variable


class Placeholder(Variable):
    def __init__(
            self,
            label: str,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        children = []
        super().__init__(
                label,
                children=children,
                subscripts=subscripts,
                shape=shape)


class ArraySizePlaceholder(Placeholder):
    def __init__(
            self,
            label: str,
            array_label: str,
            array_dim: int,
            dimension: int,
            subscripts: list = []):
        self.array_label = array_label
        self.array_dim = array_dim
        self.dimension = dimension
        shape = [None for _ in range(len(subscripts))]
        super().__init__(label, subscripts=subscripts, shape=shape)

    def __make_latex__(self):
        dim_str = str(self.dimension + 1)
        return "|" + self.array_label + "|_" + "{" + dim_str + "}"

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:
        array_value = placeholder[self.array_label]
        if isinstance(array_value, np.ndarray):
            return array_value.shape[self.dimension]

        list_value = placeholder[self.array_label]
        for s in self.subscripts:
            s_value = s.calc_value(decoded_sol, placeholder, fixed_indices)
            list_value = list_value[s_value]
        return len(list_value)
