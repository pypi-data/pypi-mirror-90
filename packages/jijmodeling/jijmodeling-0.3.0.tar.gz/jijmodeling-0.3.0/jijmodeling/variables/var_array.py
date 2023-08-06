from jijmodeling.expression.expression import Expression
from typing import Union
from jijmodeling.variables.array import Array
from jijmodeling.variables.obj_vars import Binary, DisNum, LogEncInteger
from jijmodeling.variables.placeholders import Placeholder

def BinaryArray(label: str, shape: Union[int, tuple, Placeholder]) -> Array:
    return Array(label, Binary, shape=shape)

def PlaceholderArray(label: str, dim: int=None, shape: Union[int, tuple, Placeholder]=None)->Array:
    if shape is None and isinstance(dim, int):
        _shape = tuple(None for _ in range(dim))
        return Array(label, Placeholder, shape=_shape)
    elif shape is not None:
        shape = (shape, ) if isinstance(shape, int) else shape
        return Array(label, Placeholder, shape)
    else:
        raise ValueError("Input shape or dim.")

def DisNumArray(label: str, shape, lower: float=0.0, upper: float=1.0, bits: int=3):
    return Array(label, DisNum, shape, lower=lower, upper=upper, bits=bits)

def LogEncIntArray(label: str, shape, lower:Union[int, Expression], upper: Union[int, Expression]):
    return Array(label, LogEncInteger, shape, lower=lower, upper=upper)