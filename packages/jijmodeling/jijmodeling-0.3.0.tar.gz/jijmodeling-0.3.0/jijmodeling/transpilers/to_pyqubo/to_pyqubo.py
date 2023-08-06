from functools import singledispatch
from jijmodeling.expression.constraint import Constraint, Penalty
from jijmodeling.expression.expression import Expression, Operator, Number
from jijmodeling.expression.sum import SumOperator, convert_index_set
from jijmodeling.variables.variable import Variable
from .var_to_pyqubo import _var_to_pyqubo
import numpy as np
import pyqubo as pyq


def to_pyqubo(
        term,
        placeholder: dict = {},
        fixed_variables: dict = {},
        fixed_indices: dict = {}):
    pyq_obj = _to_pyqubo(
                    term,
                    placeholder=placeholder,
                    fixed_variables=fixed_variables,
                    fixed_indices=fixed_indices,
                    cache={})

    return pyq_obj


@singledispatch
def _to_pyqubo(
        term,
        placeholder: dict,
        fixed_variables: dict,
        fixed_indices: dict,
        cache: dict):
    if isinstance(term, Expression):
        raise TypeError("`{}` cannot convert to PyQUBO object."
                        .format(term.__class__.__name__))


@_to_pyqubo.register(Variable)
def variable_to_pyqubo(
        term: Variable,
        *,
        placeholder: dict,
        fixed_variables: dict,
        fixed_indices: dict,
        cache: dict
        ) -> pyq.Base:
    # .subscripts convert to int value
    subscripts = [int(_to_pyqubo(
                        s,
                        placeholder=placeholder,
                        fixed_variables=fixed_variables,
                        fixed_indices=fixed_indices,
                        cache=cache))
                  for s in term.subscripts]

    # if variable in fixed_variable or placeholder,
    # it's value is returned.
    if term.label in placeholder:
        if len(term.subscripts) == 0:
            return placeholder[term.label]
        else:
            if not isinstance(placeholder[term.label], np.ndarray):
                placeholder[term.label] = np.array(placeholder[term.label])
            return placeholder[term.label][tuple(subscripts)]
    elif term.label in fixed_variables:
        if len(term.subscripts) == 0:
            return fixed_variables[term.label]
        else:
            if tuple(subscripts) in fixed_variables[term.label]:
                return fixed_variables[term.label][tuple(subscripts)]
    elif term.label in fixed_indices:
        return fixed_indices[term.label]

    # make variable's label with subscript values.
    var_label = term.label
    if len(subscripts) > 0:
        var_label += '[' + ']['.join([str(int(s)) for s in subscripts]) + ']'

    # if variable object in cache dictionary, return it.
    if var_label in cache:
        return cache[var_label]

    # Create a PyQUBO object according to
    # the conversion rules defined for each type of the variable.
    # _var_to_pyqubo function is written at
    # jijmodeling/transpliers/to_pyqubo/var_to_pyqubo
    var_obj = _var_to_pyqubo(
                term,
                var_label,
                placeholder,
                fixed_variables,
                fixed_indices,
                cache)

    # The object is saved in cache.
    cache[var_label] = var_obj

    return var_obj


@_to_pyqubo.register(Operator)
def operation_to_pyqubo(
        term: Operator,
        *,
        placeholder: dict,
        fixed_variables: dict,
        fixed_indices: dict,
        cache: dict):
    child_values = [_to_pyqubo(
        v,
        placeholder=placeholder,
        fixed_variables=fixed_variables,
        fixed_indices=fixed_indices,
        cache=cache
    ) for v in term.children]

    return term.operation(child_values)


@_to_pyqubo.register(SumOperator)
def sum_to_pyqubo(
        term: SumOperator,
        *,
        placeholder: dict,
        fixed_variables: dict,
        fixed_indices: dict,
        cache: dict):
    # convert index set values
    # ex. (0, n)   => np.arange(0, n)
    #     V: Array => placeholder['V']
    ind_set_list = [
        convert_index_set(
            index_set=ind_set,
            decoded_sol={},
            placeholder=placeholder,
            fixed_indices=fixed_indices)
        for ind_set in term.index_sets]

    value = 0.0
    for ind_set in zip(*ind_set_list):
        sum_index = {ind.label: ind_set[_i]
                     for _i, ind in enumerate(term.sum_indices)}
        sum_index.update(fixed_indices)
        if term.condition is not None:
            if not term.condition.calc_value(
                    decoded_sol={},
                    placeholder=placeholder,
                    fixed_indices=sum_index):
                continue

        child_val = _to_pyqubo(
                        term.inner_term,
                        placeholder=placeholder,
                        fixed_variables=fixed_variables,
                        fixed_indices=sum_index,
                        cache=cache)
        value += child_val

    return value


@_to_pyqubo.register(Penalty)
def penalty_to_pyqubo(
        term: Penalty,
        *,
        placeholder: dict = {},
        fixed_variables: dict = {},
        fixed_indices: dict = {},
        cache: dict = {}):
    return _to_pyqubo(
            term.children[0],
            placeholder=placeholder,
            fixed_variables=fixed_variables,
            fixed_indices=fixed_indices,
            cache=cache)


@_to_pyqubo.register(Constraint)
def constraint_to_pyqubo(
        term: Constraint,
        *,
        placeholder: dict = {},
        fixed_variables: dict = {},
        fixed_indices: dict = {},
        cache: dict = {}):

    child = _to_pyqubo(
                term.penalty,
                placeholder=placeholder,
                fixed_variables=fixed_variables,
                fixed_indices=fixed_indices,
                cache=cache)

    return pyq.Constraint(child, term.label)


@_to_pyqubo.register(Number)
def number_to_pyqubo(term: Number, **kwargs):
    return term.value
