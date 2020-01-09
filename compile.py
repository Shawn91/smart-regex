from collections import deque
from typing import List, Deque

from operators import OPERATORS,  concat_two_exps, handle_alter_two_exps
from data_structs import Token, Expression
from utils import count_list_elements

'''
TODO: 1. ESCAPE
2. A single character's match query is set to ANY. Is it more reasonable to set it to the character it self?
'''


def convert_exp_str_to_tokens(exp_str: str) -> List[Token]:
    # TODO: skip spaces between )/( and | such as in  (ab)  | (cd)

    char_idx = 0
    tokens_list = []
    while char_idx < len(exp_str):
        char = exp_str[char_idx]
        if char in OPERATORS:
            if char == '\\':
                tokens_list.append(Token(name='TEXT', value=exp_str[char_idx + 1]))
                char_idx += 2
            else:
                tokens_list.append(Token(name=OPERATORS[char]['name'], value=char))
                char_idx += 1
        else:
            tokens_list.append(Token(name='TEXT', value=char))
            char_idx += 1
    return tokens_list



def compile_tokens_to_expression(tokens: List[Token], exp: Expression = None) -> [Expression, None]:
    """
    TODO: a(x|y)|b(c|d) 匹配 a, bc, bd
    a(b|(c|d))
    Example:
        ['(', 'a', 'b', ')', '|', '(', 'c', '+', 'd', ')', ']': returns [['a', 'b'], ['c', '+', 'd']]
        ['a', '(', 'c', 'v', ')', '+']: returns [['a', ['c', 'v'], '+']].
    Tests:
    >>> compile_tokens_to_expression('a\+b')
    [TEXT:a, TEXT:+, TEXT:b]
    >>> compile_tokens_to_expression('a(b)+c')
    [TEXT:a, [TEXT:b], PLUS:+, TEXT:c]
    >>> compile_tokens_to_expression('(b)c')
    [[TEXT:b], TEXT:c]
    >>> compile_tokens_to_expression('a(b)')
    [TEXT:a, [TEXT:b]]
    >>> compile_tokens_to_expression('a(b(c))')
    [TEXT:a, [TEXT:b, [TEXT:c]]]
    >>> compile_tokens_to_expression('a(b(c)d)e')
    [TEXT:a, [TEXT:b, [TEXT:c], TEXT:d], TEXT:e]
    >>> compile_tokens_to_expression('(a)|(b(c))')
    [[TEXT:a], [TEXT:b, [TEXT:c]]]
    >>> compile_tokens_to_expression('ab|c')
    [[TEXT:a, TEXT:b], [TEXT:c]]
    """
    if isinstance(tokens, str):
        tokens = convert_exp_str_to_tokens(tokens)

    if exp is None:
        exp = Expression()

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]
        if cur_token.is_normal:
            exp.add_subexp(cur_token.to_exp())
            token_idx += 1
        elif cur_token.is_left_paren:
            exp.add_subexp(Expression())
            compile_tokens_to_expression(tokens[token_idx + 1:], exp=exp.get_last_subexp())
            subexp_count = exp.get_last_subexp().count_subexps()
            token_idx += subexp_count['leaf_exp'] + 2 * (subexp_count['non_leaf_exp'] + 1)
        elif cur_token.is_right_paren:
            return None
        elif cur_token.is_alt:
            exp.merge_all_subexps()
            in_alt_mode = 1  # now we are going to deal with tokens after "|"
            token_idx += 1
    return exp



            




    #     elif cur_token.is_alt:
    #         nested_tokens.append([])
    #         compile_tokens_to_expression(tokens[token_idx + 2:], nested_tokens=nested_tokens[-1])
    #         count = count_list_elements(nested_tokens[-1])
    #         token_idx += count['ele'] + 2 * (count['list'] + 1) + 1
    #     else:
    #         nested_tokens.append(cur_token)
    #         token_idx += 1
    #
    # return nested_tokens


def compile_tokens_to_expression(tokens: List[Token]):

    exp = Expression(exps=[Token(name='TEXT', value='').to_exp()])

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]
        if cur_token.is_normal:
            last_exp = exp.pop_subexp()
            last_exp = concat_two_exps(last_exp, cur_token.to_exp())
            exp.add_subexp(last_exp)
            token_idx += 1
        elif cur_token.is_alt:
            alt_exp, token_idx_skipping = compile_nested_tokens_to_exps(tokens[token_idx+1])
            last_exp = exp.pop_subexp()
            last_exp = handle_alter_two_exps(last_exp, alt_exp)
            exp.add_subexp(last_exp)
            token_idx += token_idx_skipping



    return exp, token_idx


def compile_nested_tokens_to_exps(nested_tokens):
    token_idx = 0
    exps_list = []
    while token_idx < len(nested_tokens):
        cur_token = nested_tokens[token_idx]
        if isinstance(cur_token, Token):
            if cur_token.is_normal:
                if token_idx == 0:
                    exps_list.append(cur_token.to_exp())
                else:
                    exps_list[-1] = concat_two_exps(exps_list[-1], cur_token.to_exp())
                token_idx += 1
        else: # cur_token is actually a list of tokens
            pass



    return exps_list


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    tokens = convert_exp_str_to_tokens('a|b')
    nested_tokens = compile_tokens_to_expression(tokens)
    print(nested_tokens)
    # exps = compile_nested_tokens_to_exps(nested_tokens)
    # print(exps)


