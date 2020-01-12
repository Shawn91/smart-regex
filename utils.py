from itertools import product

from boolean_operations import *
import config

def count_list_elements(l, count=None):
    """Count the number of elements after flattening a list and the number of nested lists
    Examples:
        [1,2]: returns {'ele': 2, 'list': 0}
        [1,2,[3,4]]: returns {'ele': 4, 'list': 1}
        [1,2, [3,[4]]]: returns {'ele': 4, 'list': 2}
    """
    if count is None:
        count = {'ele': 0, 'list': 0}
    for ele in l:
        if isinstance(ele, list):
            count['list'] += 1
            count_list_elements(ele, count)
        else:
            count['ele'] += 1
    return count


def concat_strings_in_two_containers(str_container1, str_container2):
    """
    This function corresponds to the X operator in https://swtch.com/~rsc/regexp/regexp4.html
    >>> concat_strings_in_two_containers(['a', 'b'], ['c', 'd'])
    ['ac', 'ad', 'bc', 'bd']
    >>> concat_strings_in_two_containers(['a', 'b'], [])
    ['a', 'b']
    >>> concat_strings_in_two_containers(['a', 'b'], [''])
    ['a', 'b']
    """
    if not str_container1:
        return str_container2
    if not str_container2:
        return str_container1
    product_result = product(str_container1, str_container2)
    return [''.join(l) for l in product_result]


def generate_ngram_chars(string, n):
    """
    >>> generate_ngram_chars('I',2)
    []
    >>> generate_ngram_chars('abcd',3)
    ['abc', 'bcd']
    """
    if len(string) < n:
        return []
    return [string[i:i+n] for i in range(len(string)-n+1)]


def generate_ngram_chars_for_str_lists(str_sets, n):
    """
    >>> generate_ngram_chars_for_str_lists(['ab','abcd'], 3)
    [[], ['abc', 'bcd']]
    >>> generate_ngram_chars_for_str_lists(['abcd','xwyz'], 3)
    [['abc', 'bcd'], ['xwy', 'wyz']]
    """
    return [generate_ngram_chars(s, n) for s in str_sets]


def generate_ngram_chars_logic_exp(str_or_lists, n):
    """Convert a string or a list of strings to ngram logic expression.
    For details, see https://swtch.com/~rsc/regexp/regexp4.html.
    >>> generate_ngram_chars_logic_exp('ab', 3)
    TRUE
    >>> generate_ngram_chars_logic_exp('abc', 3)
    Symbol('abc')
    >>> generate_ngram_chars_logic_exp('abcd', 3)
    AND(Symbol('abc'), Symbol('bcd'))
    >>> generate_ngram_chars_logic_exp(['ab'], 3)
    TRUE
    >>> generate_ngram_chars_logic_exp(['abcd'], 3)
    AND(Symbol('abc'), Symbol('bcd'))
    >>> generate_ngram_chars_logic_exp(['ab', 'abcd'], 3)
    TRUE
    >>> generate_ngram_chars_logic_exp(['abcd', 'wxyz'], 3)
    OR(AND(Symbol('abc'), Symbol('bcd')), AND(Symbol('wxy'), Symbol('xyz')))
    """
    if isinstance(str_or_lists, str):
        str_lists = [generate_ngram_chars(str_or_lists, n)]
    else:
        str_lists = generate_ngram_chars_for_str_lists(str_or_lists, n)

    if not str_lists:
        return BOOL_TRUE

    logic_exp = BOOL_FALSE
    for str_list in str_lists:
        if not str_list:
            logic_exp = OR(logic_exp, BOOL_TRUE)
        else:
            symbols = [bool_symbol(s) for s in str_list]
            if len(symbols) == 1:
                logic_exp = OR(logic_exp, symbols[0])
            else:
                logic_exp = OR(logic_exp, AND(symbols))
    return logic_exp.simplify()


def needs_regex(ngrams, match_query):
    """Given ngrams of a text and a match_query query, check whether this text should be regex-searched against."""
    if isinstance(ngrams, str):
        ngrams = generate_ngram_chars(ngrams, n=config.NGRAM_FOR_CHINESE)

    ngrams = set(ngrams)

    operator = match_query.operator
    if operator == '&':
        return all(symbol.obj in ngrams for symbol in match_query.args)
    elif operator == '|':
        return any(symbol.obj in ngrams for symbol in match_query.args)
    raise Exception('Unknown operator.')


def check_pattern_compiled(f):
    """Use as a decorator to check whether a pattern string is compiled by the re module and set to an Expression
    before invoking the Expressions's search/match/... methods.
    """
    def wrapper(self, *args, **kwargs):
        if not self.compiled_pattern:
            raise Exception('Must compile the pattern first.')
        return f(self, *args, **kwargs)
    return wrapper

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # print(generate_ngram_chars_for_str_lists(['abcd','xwyz'],3))
    # print(concat_strings_in_two_containers(['a', 'b'], ['']))
    # print(generate_ngram_chars_logic_exp('a', 3))