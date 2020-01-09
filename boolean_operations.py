import boolean
from collections import Iterable

bool_algebra = boolean.BooleanAlgebra()

# constants
BOOL_TRUE, BOOL_FALSE, NOT, _AND, OR, bool_symbol = bool_algebra.definition()

def AND(*args):
    """The original AND class in module boolean does not accept a list of symbols/expressions as a parameter.
    This function simply iterates the passed-in list and uses the original AND class on the elements.
    """
    if len(args) == 1:  # when a list of symbols/expression is passed in.
        if not isinstance(args[0], Iterable):
            raise TypeError('The argument of AND should be iterable when only one argument is provided.')
        if isinstance(args[0], str):
            raise TypeError('Arguments of AND could not be string.')
        args = args[0]

    logic_exp = BOOL_TRUE
    symbol_idx = None
    for symbol_idx, symbol in enumerate(args):
        logic_exp = _AND(logic_exp, symbol)
    if not symbol_idx:
        raise Exception('There should be more than one arguments or the only argument should be a list of length bigger than 1..')
    return logic_exp
