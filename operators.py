from collections import deque
from itertools import product

from data_strucs import Token, Term


def handle_concat(cur_token, exp_tokens, terms_stack, callback):
    """cur_t could be either a token or a term."""
    pass
    # if not terms_stack:
    #     terms_stack.append(exp_tokens[0].to_term())
    # else:
    #     last_term = terms_stack.pop()
    #     last_term.tokens.append(exp_tokens[0])
    #     last_term.emptyable = last_term.emptyable or cur_term.emptyable
    #
    #
    #     terms_stack.append(last_term)



def handle_star(exp_tokens, terms_stack, callback):
    """cur_token is the star operator"""
    cur_token = exp_tokens[0]
    last_term = terms_stack.pop()
    last_term.tokens.append(cur_token)
    last_term.emptyable = True
    last_term.exact = set()
    last_term.prefix = {''}
    last_term.suffix = {''}
    last_term.match = set()
    terms_stack.append(last_term)


def handle_qmark(exp_tokens, terms_stack, callback):
    cur_token = exp_tokens[0]
    last_term = terms_stack.pop()
    last_term.tokens.append(cur_token)
    last_term.emptyable = True
    last_term.exact = last_term.exact.union({''})
    last_term.prefix = {''}
    last_term.suffix = {''}
    last_term.match = set()
    terms_stack.append(last_term)


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
