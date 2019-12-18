from collections import deque
from typing import List, Deque

from operators import OPERATORS, concat_two_terms
from data_structs import Token, Term
from utils import count_list_elements

'''
TODO: 1. ESCAPE
'''


def convert_pat_str_to_tokens(pat_str: str) -> List[Token]:
    char_idx = 0
    tokens_list = []
    while char_idx < len(pat_str):
        char = pat_str[char_idx]
        if char in OPERATORS:
            tokens_list.append(Token(name=OPERATORS[char]['name'], value=char, operator_func=OPERATORS[char]['handle_func']))
        # elif char == '\\':
        #     char_idx += 1
        #     tokens_list.append(Token(name='TEXT', value=pat_str[char_idx]))
        else:
            tokens_list.append(Token(name='TEXT', value=char))
        char_idx += 1
    return tokens_list


def compile_tokens_to_nested(tokens:List[Token], nested_tokens:List=None) -> List[List[Term]]:
    """
    todo: a|b should be converted to (a)|(b) first
    Example:
        ['(', 'a', 'b', ')', '|', '(', 'c', '+', 'd', ')', ']': returns [['a', 'b'], ['c', '+', 'd']]
        ['a', '(', 'c', 'v', ')', '+']: returns [['a', ['c', 'v'], '+']].
    Tests:
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('a\+b'))
    [TEXT:a, TEXT:+, TEXT:b]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('a(b)+c'))
    [TEXT:a, [TEXT:b], PLUS:+, TEXT:c]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('(b)c'))
    [[TEXT:b], TEXT:c]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('a(b)'))
    [TEXT:a, [TEXT:b]]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('a(b(c))'))
    [TEXT:a, [TEXT:b, [TEXT:c]]]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('a(b(c)d)e'))
    [TEXT:a, [TEXT:b, [TEXT:c], TEXT:d], TEXT:e]
    >>> compile_tokens_to_nested(convert_pat_str_to_tokens('(a)|(b(c))'))
    [[TEXT:a], [TEXT:b, [TEXT:c]]]
    """
    if nested_tokens is None:
        nested_tokens = []

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]

        if cur_token.is_escape:
            cur_token.operator_func(tokens[token_idx:], nested_tokens)
            token_idx += 2
        elif cur_token.is_left_paren:
            nested_tokens.append([])
            compile_tokens_to_nested(tokens[token_idx+1:], nested_tokens=nested_tokens[-1])
            count = count_list_elements(nested_tokens[-1])
            token_idx += count['ele'] + 2 * (count['list'] + 1)
        elif cur_token.is_right_paren:
            return []
        elif cur_token.is_alt:
            nested_tokens.append([])
            compile_tokens_to_nested(tokens[token_idx+2:], nested_tokens=nested_tokens[-1])
            count = count_list_elements(nested_tokens[-1])
            token_idx += count['ele'] + 2 * (count['list'] + 1) + 1
        else:
            nested_tokens.append(cur_token)
            token_idx += 1

    return nested_tokens

def compile_nested_tokens_to_terms(nested_tokens):
    token_idx = 0
    terms_list = []
    while token_idx < len(nested_tokens):
        cur_token = nested_tokens[token_idx]
        if isinstance(cur_token, Token):
            if cur_token.is_normal:
                if token_idx == 0:
                    terms_list.append(cur_token.to_term())
                else:
                    terms_list[-1] = concat_two_terms(terms_list[-1], cur_token.to_term())




if __name__ == '__main__':
    import doctest
    doctest.testmod()
    tokens = convert_pat_str_to_tokens('a(b)+c')
    print(compile_tokens_to_nested(tokens))

