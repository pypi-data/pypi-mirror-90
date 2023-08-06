from jijmodeling.expression.sum import SumOperator
from jijmodeling.variables.variable import Element
from typing import Dict
from functools import singledispatch
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.obj_vars import ObjectiveVariable
from jijmodeling.expression.expression import Expression
from jijmodeling.variables.array import Array, ArraySizePlaceholder
from jijmodeling import Placeholder


def extracte_variables(term) -> Dict[str, Dict[str, Variable]]:
    vars = {
        'placeholders': {},
        'obj_vars': {},
        'array': {}
    }
    return _extracte_variables(term, vars)


@singledispatch
def _extracte_variables(term, variables: dict) -> Dict[str, Dict[str, Variable]]:
    if isinstance(term, Expression):
        for child in term.children:
            variables = _extracte_variables(child, variables)
    return variables


@_extracte_variables.register(Placeholder)
def placeholder_extracte_variables(term: Placeholder, variables: dict):
    if term.label in variables['placeholders']:
        return variables
    variables['placeholders'][term.label] = term
    return variables


@_extracte_variables.register(ObjectiveVariable)
def objvar_extracte_variables(term: ObjectiveVariable, variables: dict):
    if term.label in variables['obj_vars']:
        return variables
    variables['obj_vars'][term.label] = term
    return variables


@_extracte_variables.register(Variable)
def variable_extracte_variables(term: Variable, variables: dict):
    if isinstance(term, Placeholder):
        return placeholder_extracte_variables(term, variables)

    if term.label in variables['obj_vars']:
        return variables
    variables['obj_vars'][term.label] = term
    return variables


@_extracte_variables.register(SumOperator)
def sum_extracte_variables(term: SumOperator, variables: dict):
    for child in term.children:
        variables = _extracte_variables(child, variables)
    for key, value in zip(term.sum_indices, term.index_sets):
        variables = _extracte_variables(key, variables)
        variables = _extracte_variables(value, variables)
    return variables


@_extracte_variables.register(Array)
def array_extracte_variables(term: Array, variables: dict):
    variables['array'][term.label] = term
    return variables


@_extracte_variables.register(Element)
def element_extracte_variables(term: Element, variables: dict):
    return variables


@_extracte_variables.register(ArraySizePlaceholder)
def arraysize_extracte_variables(term: ArraySizePlaceholder, variables: dict):
    return variables
