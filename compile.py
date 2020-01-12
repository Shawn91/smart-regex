from typing import List

from operators import OPERATORS,  concat_two_exps, concat_exps, handle_alter, handle_star
from data_structs import Token, Expression

'''
TODO: 1. ESCAPE
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
                tokens_list.append(Token(name=OPERATORS[char]['name'], value=char,
                                         operator_func=OPERATORS[char]['handle_func']))
                char_idx += 1
        else:
            tokens_list.append(Token(name='TEXT', value=char))
            char_idx += 1
    return tokens_list


def compile_tokens_to_expression(tokens: [List[Token], str], debug=False):
    """
    Returns:
        1. match_query query of the final expression when debug is set to True. Or
        2. final expression and final token index
    >>> compile_tokens_to_expression('a', debug=True)
    TRUE
    >>> compile_tokens_to_expression('abcd', debug=True)
    AND(Symbol('ab'), Symbol('bc'), Symbol('cd'))
    >>> compile_tokens_to_expression('a\+b', debug=True)
    AND(Symbol('+b'), Symbol('a+'))
    >>> compile_tokens_to_expression('a(bc)d', debug=True)
    AND(Symbol('ab'), Symbol('bc'), Symbol('cd'))
    >>> compile_tokens_to_expression('a(b(c))d', debug=True)
    AND(Symbol('ab'), Symbol('bc'), Symbol('cd'))
    >>> compile_tokens_to_expression('ab|(cd|ef)', debug=True)
    OR(Symbol('ab'), Symbol('cd'), Symbol('ef'))
    >>> compile_tokens_to_expression('a(b|(c|d))', debug=True)
    OR(Symbol('ab'), Symbol('ac'), Symbol('ad'))
    >>> compile_tokens_to_expression('ab|c', debug=True)
    TRUE
    >>> compile_tokens_to_expression('a+bc', True)
    AND(Symbol('ab'), Symbol('bc'))
    >>> compile_tokens_to_expression('a?bc', True)
    Symbol('bc')
    >>> compile_tokens_to_expression('a*bc', True)
    Symbol('bc')
    """
    if isinstance(tokens, str):
        tokens = convert_exp_str_to_tokens(tokens)

    exp_list = []

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]
        if cur_token.is_normal:
            exp_list.append(cur_token.to_exp())
            token_idx += 1
        elif cur_token.is_plus or cur_token.is_qmark or cur_token.is_star:
            last_exp = exp_list.pop()
            last_exp = cur_token.operator_func(last_exp)
            exp_list.append(last_exp)
            token_idx += 1
        elif cur_token.is_left_paren:
            new_exp, num_tokens_to_skip = compile_tokens_to_expression(tokens[token_idx+1:])
            exp_list.append(new_exp)
            token_idx += num_tokens_to_skip + 2
        elif cur_token.is_right_paren:
            break
        elif cur_token.is_alt:
            exp = concat_exps(exp_list)
            next_exp, num_tokens_to_skip = compile_tokens_to_expression(tokens[token_idx+1:])
            exp = handle_alter(exp, next_exp)
            token_idx += num_tokens_to_skip + 1
            exp_list = [exp]

    exp = concat_exps(exp_list)

    if debug:
        return exp.get_match_query(simplify=True)
    return exp, token_idx


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    nested_tokens1 = compile_tokens_to_expression('abc', True)
    nested_tokens2 = compile_tokens_to_expression('a(b|c)', True)
    nested_tokens2 = compile_tokens_to_expression('a(b|c)d|ef(g|h)', True)
    print(nested_tokens1)
    # print((nested_tokens, 1))
    # exps = compile_nested_tokens_to_exps(nested_tokens)
    # print(exps)
    # show_args(nested_tokens)
