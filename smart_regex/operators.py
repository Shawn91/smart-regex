from smart_regex.data_structs import Token, Expression
from smart_regex.utils import concat_strings_in_two_containers
from smart_regex.boolean_operations import *



def concat_two_exps(exp1: Expression, exp2: Expression):
    new_exp = Expression.create_empty_expression()
    new_exp.set_emptyable(exp1.emptyable and exp2.emptyable)

    # set match_query of new_exp
    match = AND(exp1.get_match_query(), exp2.get_match_query())
    new_exp.set_match(match)

    # set exact of new_exp
    exact = concat_strings_in_two_containers(exp1.exact, exp2.exact) if exp1.exact and exp2.exact else set()
    new_exp.set_exact(exact)

    # set prefix of new_exp
    if exp1.exact:
        new_exp.set_prefix(concat_strings_in_two_containers(exp1.exact, exp2.prefix))
    elif exp1.emptyable:
        new_exp.set_prefix(exp1.prefix.union(exp2.prefix))
    else:
        new_exp.set_prefix(exp1.prefix)

    # set suffix of new_exp
    if exp2.exact:
        new_exp.set_suffix(concat_strings_in_two_containers(exp1.suffix, exp2.exact))
    elif exp2.emptyable:
        new_exp.set_suffix(exp1.suffix.union(exp2.suffix))
    else:
        new_exp.set_suffix(exp2.suffix)

    return new_exp


def concat_exps(exp_list):
    if not exp_list:
        raise Exception('Parameter exp_list cannot be an empty list.')
    if len(exp_list) == 1:
        return exp_list[0]
    final_exp = Expression.create_empty_expression()
    for exp in exp_list:
        final_exp = concat_two_exps(final_exp, exp)
    return final_exp


def handle_alter(exp1: Expression, exp2: Expression) -> Expression:
    new_exp = Expression()
    new_exp.set_emptyable(exp1.emptyable or exp2.emptyable)

    # set match_query of new_exp
    match = OR(exp1.match_query, exp2.match_query)
    new_exp.set_match(match)

    # set exact of new_exp
    exact = exp1.exact.union(exp2.exact) if exp2.exact else set()
    new_exp.set_exact(exact)

    # set prefix of new_exp
    new_exp.set_prefix(exp1.prefix.union(exp2.prefix))

    # set suffix of new_exp
    new_exp.set_suffix(exp1.suffix.union(exp2.suffix))

    return new_exp


def handle_star(exp: Expression) -> Expression:
    exp.set_emptyable(True)
    if not exp.converted_from_an_anytoken():
        exp.set_exact(exp.exact.union(e*2 for e in exp.exact).union(set([''])))
    exp.set_prefix(exp.prefix.union(set([''])))
    exp.set_suffix(exp.suffix.union(set([''])))
    # exp.set_exact(set())
    # exp.set_prefix(set(['']))
    # exp.set_suffix(set(['']))
    exp.set_match(BOOL_TRUE)
    return exp


def handle_qmark(exp: Expression) -> Expression:
    exp.set_emptyable(True)
    if not exp.converted_from_an_anytoken():
        exp.set_exact(exp.exact.union(set([''])))
    exp.set_prefix(exp.prefix.union(set([''])))
    exp.set_suffix(exp.suffix.union(set([''])))
    # exp.set_prefix(set(['']))
    # exp.set_suffix(set(['']))
    exp.set_match(BOOL_TRUE)
    return exp

def handle_plus(exp: Expression) -> Expression:
    exp.set_exact(exp.exact.union(e*2 for e in exp.exact))
    return exp


OPERATORS = {
    '(': {'name': 'LEFT_PAREN', 'handle_func': None},
    ')': {'name': 'RIGHT_PAREN', 'handle_func': None},
    '*': {'name': 'STAR', 'handle_func': handle_star},
    '|': {'name': 'ALT', 'handle_func': None},
    '+': {'name': 'PLUS', 'handle_func': handle_plus},
    '?': {'name': 'QMARK', 'handle_func': handle_qmark},
    '\\': {'name': 'ESCAPE', 'handle_func': None}
}


if __name__ == '__main__':
    result = concat_two_exps(Token(name='TEXT', value='a').to_exp(), Token(name='TEXT', value='b').to_exp(),)
    result.match = result.match.simplify()
    result