from collections import deque
from typing import List, Deque

from operators import OPERATORS,  concat_two_exps, concat_exps
from data_structs import Token, Expression, create_empty_expression
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


def compile_tokens_to_expression(tokens: List[Token], debug=False):
    """
    Returns:
        1. match query of the final expression when debug is set to True. Or
        2. final expression and final token index
    >>> compile_tokens_to_expression('a', debug=True)
    TRUE
    >>> compile_tokens_to_expression('abcd', debug=True)
    AND(Symbol('ab'), Symbol('bc'), Symbol('cd'))
    >>> compile_tokens_to_expression('a\+b', debug=True)
    AND(Symbol('+b'), Symbol('a+'))
    """
    if isinstance(tokens, str):
        tokens = convert_exp_str_to_tokens(tokens)
    exp = create_empty_expression()

    exp_list = []

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]
        if cur_token.is_normal:
            exp_list.append(cur_token.to_exp())
            token_idx += 1
        elif cur_token.is_plus or cur_token.is_qmark or cur_token.is_star:
            last_exp = exp_list.pop()
            last_exp = cur_token.handle_operator(last_exp) # TODO
            exp_list.append(last_exp)
            token_idx += 1
        elif cur_token.is_left_paren:
            new_exp, num_tokens_to_skip = compile_tokens_to_expression(token_idx[token_idx+1])
            exp_list.append(new_exp)
            token_idx += num_tokens_to_skip
        elif cur_token.is_right_paren:
            # TODO: calculate how many tokens to skip
            break
        elif cur_token.is_alt:
            exp = concat_exps(exp_list)
            next_exp = compile_tokens_to_expression(tokens[token_idx+1])
            exp = handle_alt_exps(exp, next_exp)
            exp_list = [exp]

    exp = concat_exps(exp_list)

    if debug:
        return exp.get_match()
    return exp, token_idx



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    tokens = convert_exp_str_to_tokens('a\+b')
    nested_tokens = compile_tokens_to_expression(tokens, True)
    print(nested_tokens)
    # exps = compile_nested_tokens_to_exps(nested_tokens)
    # print(exps)


