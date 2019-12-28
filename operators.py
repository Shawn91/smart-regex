from collections import deque
from itertools import product

from data_structs import Token, Term
from utils import concat_strings_of_two_lists


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

def concat_two_terms(term1: Term, term2: Term):
    new_term = Term(term1.tokens+term2.tokens)
    new_term.set_emptyable(term1.emptyable and term2.emptyable)

    # set exact of new_term
    exact = concat_strings_of_two_lists(term1.exact, term2.exact) if term1.exact and term2.exact else set()
    new_term.set_exact(exact)

    # set prefix of new_term
    if term1.exact:
        new_term.set_prefix(concat_strings_of_two_lists(term1.exact, term2.prefix))
    elif term1.emptyable:
        new_term.set_prefix(term1.prefix.union(term2.prefix))
    else:
        new_term.set_prefix(term1.prefix)

    # set suffix of new_term
    if term2.exact:
        new_term.set_suffix(concat_strings_of_two_lists(term1.suffix, term2.exact))
    elif term2.emptyable:
        new_term.set_suffix(term1.suffix.union(term2.suffix))
    else:
        new_term.set_suffix(term2.suffix)

    # set match of new_term
    new_term.set_match(term1.match.union(term2.match))
    return new_term






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
