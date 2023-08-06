from numbers import Number
from jijmodeling.variables.array import ArraySizePlaceholder
from jijmodeling.variables.placeholders import Placeholder
import jijmodeling.variables.list as var_list
import warnings
import numpy as np


def array_size(s, placeholder):
    if isinstance(s, (int, np.int)):
        return s
    elif isinstance(s, ArraySizePlaceholder):
        return np.array(placeholder[s.array_label]).shape[s.dimension]
    elif isinstance(s, Placeholder):
        return placeholder[s.label]
    else:
        raise TypeError(
                "{}'s shape should be " +
                'int, ArraySizePlaceholder or Placeholder, not {}'
                .format(s, type(s)))


def variables_validation(placeholder: dict, variables: dict):
    array = variables['array']
    ph_values = variables['placeholders']
    for label, var in placeholder.items():
        if isinstance(var, Number):
            pass
        elif isinstance(var, (list, np.ndarray)):
            if label not in ph_values and label not in array:
                warnings.warn('"{}" is not found in your model.'.format(label))
                continue
            if label not in ph_values:
                continue
            var_obj = ph_values[label]
            if isinstance(var_obj, var_list.List):
                continue
            var_shape = tuple([array_size(s, placeholder)
                               for s in var_obj.shape])
            var = np.array(var)
            if var.shape != var_shape:
                raise TypeError('The shape of "{}" should be {}, not {}'
                                .format(label, var_shape, var.shape))
