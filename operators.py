from collections import deque
from itertools import product

from data_structs import Token, Expression, create_empty_expression
from utils import concat_strings_in_two_containers



def concat_two_exps(exp1: Expression, exp2: Expression):
    new_exp = Expression()
    new_exp.set_emptyable(exp1.emptyable and exp2.emptyable)

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
    final_exp = create_empty_expression()
    for exp in exp_list:
        final_exp = concat_two_exps(final_exp, exp)
    return final_exp


def handle_alter_two_exps(exp1: Expression, exp2: Expression):
    new_exp = Expression()
    new_exp.set_emptyable(exp1.emptyable or exp2.emptyable)

    # set match of new_exp
    new_exp.set_match(exp1.match.union(exp2.match))

    # set exact of new_exp
    exact = exp1.exact.union(exp2.exact)
    new_exp.set_exact(exact)

    # set prefix of new_exp
    new_exp.set_prefix(exp1.prefix.union(exp2.prefix))

    # set suffix of new_exp
    new_exp.set_suffix(exp1.suffix.union(exp2.suffix))

    # set match of new_exp
    new_exp.set_match(exp1.match.union(exp2.match))
    return new_exp






def handle_star(exp_tokens, exps_stack, callback):
    """cur_token is the star operator"""
    cur_token = exp_tokens[0]
    last_exp = exps_stack.pop()
    last_exp.tokens.append(cur_token)
    last_exp.emptyable = True
    last_exp.exact = set()
    last_exp.prefix = {''}
    last_exp.suffix = {''}
    last_exp.match = set()
    exps_stack.append(last_exp)


def handle_qmark(exp_tokens, exps_stack, callback):
    cur_token = exp_tokens[0]
    last_exp = exps_stack.pop()
    last_exp.tokens.append(cur_token)
    last_exp.emptyable = True
    last_exp.exact = last_exp.exact.union({''})
    last_exp.prefix = {''}
    last_exp.suffix = {''}
    last_exp.match = set()
    exps_stack.append(last_exp)


def handle_paren(exp_tokens, tokens_list, callback):
    token_idx = 1
    while token_idx < len(exp_tokens):
        cur_token = exp_tokens[token_idx]





def handle_escape(exp_tokens, tokens_list):
    """the first token of exp_tokens is '\'
    """
    if exp_tokens[1].is_operator:
        exp_tokens[1] = Token(name='TEXT', value=exp_tokens[1].value, operator_func=handle_concat)
        tokens_list.append(exp_tokens[1])

OPERATORS = {
    '(': {'name': 'LEFT_PAREN', 'handle_func': None},
    ')': {'name': 'RIGHT_PAREN', 'handle_func': None},
    '*': {'name': 'STAR', 'handle_func': handle_star},
    '|': {'name': 'ALT', 'handle_func': None},
    '+': {'name': 'PLUS', 'handle_func': None},
    '?': {'name': 'QMARK', 'handle_func': handle_qmark},
    '\\': {'name': 'ESCAPE', 'handle_func': handle_escape}
}

if __name__ == '__main__':
    result = concat_two_exps(Token(name='TEXT', value='a').to_exp(), Token(name='TEXT', value='b').to_exp(),)
    result.match = result.match.simplify()
    result