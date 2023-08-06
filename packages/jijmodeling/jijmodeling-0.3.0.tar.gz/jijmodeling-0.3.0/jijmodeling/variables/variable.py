from typing import Tuple, Union, Dict
import numpy as np
from jijmodeling.expression.expression import Expression, _latex_repr, Children


class Variable(Expression):
    def __init__(
            self,
            label: str,
            children: list = [],
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        self._label = label
        for s in subscripts:
            if not isinstance(s, (Expression, int)):
                raise TypeError(
                        "The type of subscripts is list \
                            of Element or int. not {}.".format(type(s)))
        self._subscripts = Children(subscripts)
        self._shape = shape
        if len(shape) != len(subscripts):
            raise ValueError("{}'s length of shape ({}) and subscripts ({}) should be equal.".format(label, shape, subscripts))
        super().__init__(children=children)

    @property
    def label(self):
        return self._label

    @property
    def subscripts(self):
        return self._subscripts

    @property
    def dim(self) -> int:
        return len(self.subscripts)

    @property
    def indices(self):
        return self.children.indices + self.subscripts.indices

    @property
    def shape(self):
        return self._shape

    @property
    def length(self):
        return self._shape[0]

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]] = {},
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:

        if self.label in decoded_sol:
            sol = np.array(decoded_sol[self.label])
        elif self.label in placeholder:
            sol = np.array(placeholder[self.label])
        elif self.label in fixed_indices:
            return fixed_indices[self.label]
        else:
            raise ValueError('"{}" is not found in placehoder and solution.'
                             .format(self.label))

        if self.dim != len(sol.shape):
            raise ValueError("{}'s dimension mismatch.\
                             {} expect {}-dim array. not {}-dim."
                             .format(self.label, self.label,
                                     self.dim, len(sol.shape)))

        def script_to_value(obj):
            if isinstance(obj, Expression):
                return int(
                        obj.calc_value(
                            decoded_sol, placeholder, fixed_indices))
            else:
                return obj

        s_values = [script_to_value(s) for s in self.subscripts]
        try:
            value = np.array(sol)[tuple(s_values)]
        except IndexError as e:
            raise ValueError(
                    "{}.\nThe shape of '{}' is {}, \
                    but access indices are {}."
                    .format(e, self.label, np.array(sol).shape, s_values))

        if value is np.nan:
            return 0
        return value

    def decode_from_dict(
            self,
            sample: dict,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]] = {},
            fixed_variables: Dict[str, Union[int, float, Dict[Tuple[int, ...], Union[int, float]]]] = {},
            indices: list = []):
        raise NotImplementedError("need `decode_from_dict`")

    def __repr__(self) -> str:
        subscripts_str = ''
        for i in self.subscripts:
            subscripts_str += '[%s]' % i
        return self.label + subscripts_str

    def __make_latex__(self):
        subscripts_str = ','.join([_latex_repr(i, False) for i in self.subscripts])
        return self.label + "_{" + subscripts_str + "}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Variable):
            return False
        if o.__class__ != self.__class__:
            return False
        if o.label != self.label or o.dim != self.dim:
            return False

        for s, os in zip(self.subscripts, o.subscripts):
            if isinstance(s, Variable):
                if not isinstance(os, Variable):
                    return False
                if s != o:
                    return False
            elif isinstance(s, Expression):
                if s.__class__ != os.__class__:
                    return False
                elif str(s) != str(os):
                    return False
        return True


class Element(Variable):
    def __init__(self, label: str, set=None):
        children = []
        subscripts = []
        self.set: Variable = set
        import jijmodeling.variables.list as var_list
        if isinstance(self.set, (self.__class__, var_list.List)):
            if self.set.dim == 0:
                raise ValueError("`{}` is scalar, so cannot assign a set of {}".format(set, self.label))
        super().__init__(label, children=children, subscripts=subscripts)

    def __hash__(self) -> int:
        return self.label.__hash__()

    @property
    def dim(self):
        import jijmodeling.variables.list as var_list
        if isinstance(self.set, var_list.List):
            return self.set.dim - 1
        elif isinstance(self.set, self.__class__):
            return self.set.dim - 1
        else:
            return 0

    def is_scalar(self):
        return self.dim == 0
