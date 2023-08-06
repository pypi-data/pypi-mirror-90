from functools import singledispatch
from types import new_class

from numpy.lib.function_base import place

from jijmodeling.variables.element import Element

from jijmodeling.expression.expression import Operator, Mul
from jijmodeling.expression.constraint import Constraint, Penalty
from jijmodeling.variables.array import ArraySizePlaceholder, Tensor
from jijmodeling.variables.variable import Binary, Placeholder, Variable
from jijmodeling.expression.sum import SumOperator
from jijmodeling.transpilers.utils import _reshape_index, _index_values_list, exist_expression
from typing import Dict, Union
import numpy as np
import math


def calc_value(term, decoded_sol: dict, placeholder: dict={}, fixed_indices: dict={})->Union[float, int]:
    """calculate value of term

    Args:
        term ([type]): [description]
        decoded_sol (dict): [description]
        placeholder (dict, optional): [description]. Defaults to {}.
        fixed_indices (dict, optional): [description]. Defaults to {}.

    Returns:
        [type]: [description]
    """
    # convert placeholder type
    ph = {k: v if isinstance(v, np.ndarray) else np.array(v) for k,v in placeholder.items()}
    return _calc_value(term, decoded_sol, placeholder=ph, fixed_indices=fixed_indices)

@singledispatch
def _calc_value(term, decoded_sol: dict, placeholder={}, **kwargs)->float:
    if isinstance(term, (int, float)):
        return term
    if isinstance(term, Variable):
        if term.label in decoded_sol:
            return decoded_sol[term.label]
        elif term.label in placeholder:
            return decoded_sol[placeholder]
        else:
            raise ValueError('{} is not found in solution and placeholder'.format(term.label))
    else:
        print(term)
        raise TypeError('calc_value do not support {}'.format(type(term)))


@_calc_value.register(Operator)
def calc_operator_value(term: Operator, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    child_values = [calc_value(child, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices) for child in term.children]
    term_value: float = term.operation(child_values)
    return term_value


@_calc_value.register(Binary)
def calc_binary_value(term: Binary, decoded_sol: dict, placeholder={}, **kwargs)->float:
    if term.label in decoded_sol:
        return decoded_sol[term.label]
    else:
        # TODO: add warning
        return 0

@_calc_value.register(Placeholder)
def calc_placeholder_value(term: Placeholder, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    return placeholder[term.label]

@_calc_value.register(ArraySizePlaceholder)
def calc_placeholder_value(term: ArraySizePlaceholder, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    array = placeholder[term.array_label]
    return array.shape[term.dimension]


@_calc_value.register(Element)
def calc_element_value(term: Element, decoded_sol: dict, placeholder={}, fixed_indices={}):
    return fixed_indices[term.label]


@_calc_value.register(Tensor)
def calc_tensor_value(term: Tensor, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    sol: Dict[tuple, float] = {}
    if term.label in decoded_sol:
        sol = decoded_sol[term.label]
    elif term.label in placeholder:
        sol = placeholder[term.label]
    else:
        ValueError('"{}" is not found in placehoder and solution.'.format(term.label))
    
    def to_index(obj):
        if isinstance(obj, str):
            return fixed_indices[obj]
        else:
            value = calc_value(obj, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
            if isinstance(value, (float, int)):
                return int(value)
            else:
                return value
    index_label = [to_index(label) for label in term.indices]

    try:
        value = np.array(sol)[tuple(index_label)]
    except IndexError as e:
        raise ValueError("{}.\nThe shape of '{}' is {}, but access indices are {}.".format(e, term.label, np.array(sol).shape, index_label))

    if value is np.nan:
        return 0
    return value


@_calc_value.register(SumOperator)
def calc_sum_value(term: SumOperator, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    # Sum の calc_valueを書く
    # Sumのcalc_valueはいったん普通に要素に対してやるが、TODOでnumpyの演算をうまく使うようにメモしておく
    # If the calculation is like the inner product of vectors, 
    # replace it with the numpy calculation to make it as fast as possible.
    # 
    innered = len(term.index_keys) == 1
    innered = innered and isinstance(term.children[0], (Operator, Variable))
    innered = innered and not np.any([exist_expression(SumOperator, c) for c in term.children])
    
    def check_inner_product():
        sum_ind_set = _index_values_list(term.indices, fixed_indices, placeholder)
        
        new_indices = fixed_indices.copy()

        ind_set_list = np.array(sum_ind_set[term.index_keys[0]])
        new_indices[term.index_keys[0]] = ind_set_list
        child_val = calc_value(term.children[0], decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=new_indices)
        if not isinstance(child_val, np.ndarray):
            return child_val

        

        if term.condition is not None:
            ind_set_list = calc_value(term.condition, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=new_indices)

        return np.sum(child_val[ind_set_list])

    if innered:
        return check_inner_product()

    sum_index = _reshape_index(term.indices, fixed_indices=fixed_indices, placeholder=placeholder)
    term_value:float = 0.0
    if term.condition is not None:
        child = term.children[0]
        for ind in sum_index:
            sum_cond = calc_value(term.condition, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
            if sum_cond:
                child_val: float = calc_value(child, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
                term_value += child_val if not math.isnan(child_val) else 0.0
    else:
        child = term.children[0]
        for ind in sum_index:
            child_val: float = calc_value(child, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
            term_value += child_val if not math.isnan(child_val) else 0.0
    return term_value



@_calc_value.register(Constraint)
def calc_constraint_value(term: Constraint, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    penalty_value = calc_value(term.children[0], decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
    if term.condition == '==' and penalty_value == term.constant:
        return 0.0
    elif term.condition == '<=' and penalty_value <= term.constant:
        return 0.0
    elif term.condition == '<' and penalty_value < term.constant:
        return 0.0
    else:
        return penalty_value - term.constant


@_calc_value.register(Penalty)
def calc_penalty_value(term: Penalty, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    return calc_value(term.penalty_term, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
