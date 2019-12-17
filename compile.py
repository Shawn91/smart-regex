from collections import deque
from typing import List, Deque

from operators import OPERATORS
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


def compile_tokens_to_nested(tokens:List[Token], container_tokens:List=None, nested_tokens:List=None) -> List[List[Term]]:
    """
    Container_tokens is always the direct parent of nested_tokens.
    Example:
        ['(', 'a', 'b', ')', '|', '(', 'c', '+', 'd', ')', ']': returns [['a', 'b'], ['c', '+', 'd']]
        ['a', '(', 'c', 'v', ')', '+']: returns [['a', ['c', 'v'], '+']].
            When the container_tokens is [['a', ['c', 'v'], '+']], nested_tokens is ['a', ['c', 'v'], '+']
            When the container_tokens is ['a', ['c', 'v'], '+'], nested_tokens is ['c', 'v']
    Tests:
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('a\+b')))
    '[[TEXT:a, TEXT:+, TEXT:b]]'
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('a(b)c')))
    '[[TEXT:a, [TEXT:b], TEXT:c]]'
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('(b)c')))
    '[[[TEXT:b], TEXT:c]]'
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('a(b)')))
    '[[TEXT:a, [TEXT:b]]]'
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('a(b(c))')))
    '[[TEXT:a, [TEXT:b, [TEXT:c]]]]'
    >>> str(compile_tokens_to_nested(convert_pat_str_to_tokens('a(b(c)d)e')))
    '[[TEXT:a, [TEXT:b, [TEXT:c], TEXT:d], TEXT:e]]'
    """
    if container_tokens is None or nested_tokens is None:
        container_tokens = [[]]
        nested_tokens = container_tokens[-1]

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]

        if cur_token.is_normal:
            nested_tokens.append(cur_token)
            token_idx += 1
        elif cur_token.is_escape:
            cur_token.operator_func(tokens[token_idx:], nested_tokens)
            token_idx += 2
        elif cur_token.is_left_paren:
            nested_tokens.append([])
            compile_tokens_to_nested(tokens[token_idx+1:], container_tokens=container_tokens, nested_tokens=nested_tokens[-1])
            count = count_list_elements(nested_tokens[-1])
            token_idx += count['ele'] + 2 * (count['list'] + 1)
        elif cur_token.is_right_paren:
            return None

    return container_tokens


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # 解决 (b(c)) 不对的问题
    tokens = convert_pat_str_to_tokens('a\+b')
    print(compile_tokens_to_nested(tokens))

