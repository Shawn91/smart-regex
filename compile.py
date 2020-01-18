from typing import List

from operators import OPERATORS,  concat_two_exps, concat_exps, handle_alter, handle_star
from data_structs import Token, AnyToken,Expression
from special_chars import SPECIAL_CHARS
from boolean_operations import OR

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
        elif char in SPECIAL_CHARS:
            tokens_list.append(AnyToken())
            char_idx += 1
        else:
            tokens_list.append(Token(name='TEXT', value=char))
            char_idx += 1
    return tokens_list


def compile_tokens_to_expression(tokens: [List[Token], str], debug=False):
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
    >>> compile_tokens_to_expression('a+bc', True)
    AND(Symbol('ab'), Symbol('bc'))
    >>> compile_tokens_to_expression('a?bc', True)
    Symbol('bc')
    >>> compile_tokens_to_expression('a*bc', True)
    Symbol('bc')
    >>> compile_tokens_to_expression('ad.+cb',True)
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
        return exp.get_match_query()#.simplify()#(simplify=False)
    return exp, token_idx


if __name__ == '__main__':
    import doctest,re
    doctest.testmod()
    # pats = '欧 *阳|独 *孤|令 *狐|皇 *甫|夏 *侯|呼 *延|诸 *葛|完 *颜|拓 *跋|公 *孙|宇 *文|北 *野|欧 *文|上 *官|端 *木|轩 *辕|慕 *蓉|公 *叔|司 *寇|百 *里|司 *马|北 *门|拓 *拔|慕 *容|独 *狐|爱 *新 *觉 *罗|尉 *迟|歐 *陽|叶 *赫 *纳 *拉|兀 *颜|司 *徒|耶 *律|单 *于|西 *门|公 *延|第 *五|令 *孤|北 *堂|蔚 *迟|西 *伯|申 *屠|公 *输'
    # pats = pats.split('|')
    # exps = []
    # for pat in pats:
    #     exps.append(compile_tokens_to_expression(pat, True))
    # # Expression().set_match(OR(exps))
    # print(OR(exps).pretty())
    # nested_tokens1 = compile_tokens_to_expression('欧 *阳|独 *孤|令 *狐|皇 *甫|夏 *侯|呼 *延|诸 *葛|完 *颜|拓 *跋|公 *孙|宇 *文|北 *野|欧 *文|上 *官|端 *木|轩 *辕|慕 *蓉|公 *叔|司 *寇|百 *里|司 *马|北 *门|拓 *拔|慕 *容|独 *狐|爱 *新 *觉 *罗|尉 *迟|歐 *陽|叶 *赫 *纳 *拉|兀 *颜|司 *徒|耶 *律|单 *于|西 *门|公 *延|第 *五|令 *孤|北 *堂|蔚 *迟|西 *伯|申 *屠|公 *输',True)
    # print(nested_tokens1.get_match_query())
    # print(nested_tokens1.pretty())
    # print((nested_tokens1, 1))
    # exps = compile_nested_tokens_to_exps(nested_tokens)
    # print(exps)
    # show_args(nested_tokens)
