from typing import List


from smart_regex.operators import OPERATORS, concat_exps, handle_alter
from smart_regex.data_structs import Token
from smart_regex.special_chars import SPECIAL_CHARS

'''
TODO: 1. ESCAPE
'''


def convert_exp_str_to_tokens(exp_str: str) -> List[Token]:
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
        elif char in SPECIAL_CHARS:
            tokens_list.append(SPECIAL_CHARS[char]['handle_func']())
            char_idx += 1
        else:
            tokens_list.append(Token(name='TEXT', value=char))
            char_idx += 1
    return tokens_list


def compile_tokens_to_expression(tokens: [List[Token], str], simplify_match_query=True, debug=False):
    """
    Returns:
        1. match_query query of the final expression when debug is set to True. Or
        2. final expression and final token inverted_index
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
    >>> compile_tokens_to_expression('a+bc', debug=True)
    AND(Symbol('ab'), Symbol('bc'))
    >>> compile_tokens_to_expression('a?bc', debug=True)
    Symbol('bc')
    >>> compile_tokens_to_expression('a*bc', debug=True)
    Symbol('bc')
    >>> compile_tokens_to_expression('ad.+cb', debug=True)
    AND(Symbol('ad'), Symbol('cb'))
    """
    if isinstance(tokens, str):
        tokens = convert_exp_str_to_tokens(tokens)

    exp_list = []

    token_idx = 0

    while token_idx < len(tokens):
        cur_token = tokens[token_idx]
        if cur_token.is_normal or cur_token.is_speical_char:
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
        return exp.get_match_query().simplify()#(simplify=False)
    if simplify_match_query:
        exp.simplify_match()
    return exp, token_idx


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # from boolean_operations import AND
    # a = compile_tokens_to_expression('((0|1|2|3|4|5|6|7|8|9) *)+')[0].get_match_query()
    # b = compile_tokens_to_expression('(~|\\|-|\xad–|—|―|－|一|至) *')[0].get_match_query()
    # c = compile_tokens_to_expression('((0|1|2|3|4|5|6|7|8|9) *)+人)')[0].get_match_query()
    # d = AND(a,b,c)
    # print(d.simplify())
    nested_tokens1 = compile_tokens_to_expression('ac.b',debug=True)
    print(nested_tokens1)
    print(nested_tokens1.pretty())
    # print((nested_tokens1, 1))
    # exps = compile_nested_tokens_to_exps(nested_tokens)
    # print(exps)
    # show_args(nested_tokens)
