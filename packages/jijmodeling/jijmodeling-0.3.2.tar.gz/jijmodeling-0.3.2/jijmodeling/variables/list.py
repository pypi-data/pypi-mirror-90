from jijmodeling.expression.expression import Expression
from jijmodeling.variables.variable import Element
from jijmodeling.variables.placeholders import ArraySizePlaceholder, Placeholder
import numpy as np
from typing import Union, Dict


class List(Placeholder):
    def __init__(self, label: str, dim: int, subscripts: list = []):
        self._dim = dim
        shape = tuple([None for _ in range(len(subscripts))])
        super().__init__(label, subscripts=subscripts, shape=shape)

    @property
    def dim(self) -> int:
        return self._dim

    def length(self):
        if self.dim == len(self.subscripts):
            raise ValueError("{} is scalar.".format(self))
        dimension = len(self.subscripts)
        return ArraySizePlaceholder(
            label=self.label + '_shape_{}'.format(dimension),
            array_label=self.label,
            array_dim=self.dim,
            dimension=dimension,
            subscripts=self.subscripts
        )

    def is_scalar(self):
        return self.dim == len(self.subscripts)

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key, )

        key_list = []
        for k in key:
            if isinstance(k, str):
                key_list.append(Element(k))
            else:
                key_list.append(k)

        subscripts = self.subscripts + key_list
        if len(subscripts) > self.dim:
            raise KeyError(
                    "List `{}`'s dimension is {}, cannot access {} subscripts"
                    .format(self.label, self.dim, len(subscripts)))
        return self.__class__(
                    label=self.label, dim=self.dim, subscripts=subscripts)

    @property
    def operatable(self):
        return len(self.subscripts) == self.dim

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int, list]:
        list_value = placeholder[self.label]
        for s in self.subscripts:
            if isinstance(s, Expression):
                s_value = int(s.calc_value(
                                    decoded_sol, placeholder, fixed_indices))
            else:
                s_value = s
            list_value = list_value[s_value]
        return list_value
