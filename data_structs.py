import re

from boolean_operations import *
from utils import generate_ngram_chars, generate_ngram_chars_logic_exp, needs_regex, check_pattern_compiled
from config import NGRAM_FOR_CHINESE, NGRAM_FOR_ENGLISH



class Token:
    """A Token is either made from a plain character or an operator like "?"
    """
    def __init__(self, name, value, operator_func=None):
        self.name = name
        self.value = value
        self.operator_func = operator_func  # function for handling operators
        self.is_operator = self.name != 'TEXT'
        self.is_normal = self.name == 'TEXT'  # 普通字符
        self.is_left_paren = self.is_operator and self.value == '('
        self.is_right_paren = self.is_operator and self.value == ')'
        self.is_alt = self.is_operator and self.value == '|'
        self.is_escape = self.is_operator and self.value == '\\'
        self.is_star = self.is_operator and self.value == '*'
        self.is_plus = self.is_operator and self.value == '+'
        self.is_qmark = self.is_operator and self.value == '?'

    def __repr__(self):
        return self.name + ":" + self.value

    def to_exp(self):
        """Convert token to an expression."""
        if self.is_normal:
            exp = Expression([self])
            exp.emptyable = False if self.value else True
            exp.exact, exp.prefix, exp.suffix = {self.value}, {self.value}, {self.value}
            self.match = BOOL_TRUE
            return exp
        raise Exception('Only tokens of plain characters could be converted to an expression')


class Expression:
    EXACT_SET_MAXIMUM_SIZE = 100  # clear the exact set when its size goes beyond maximum size to save memory

    def __init__(self, tokens=None, exps=None, ngram=NGRAM_FOR_CHINESE):
        self.tokens = [] if tokens is None else tokens  # a list of tokens
        self.subexps = [] if exps is None else exps  # a list of sub expressions
        self.emptyable = None
        self.exact = set()  # empty set corresponds to "unknown" in https://swtch.com/~rsc/regexp/regexp4.html
        self.prefix = set()
        self.suffix = set()

        # match_query should be a boolean expression.
        # For details, see https://booleanpy.readthedocs.io/en/latest/users_guide.html
        # BOOL_TRUE corresponds to "ANY" in https://swtch.com/~rsc/regexp/regexp4.html
        self.match_query = BOOL_TRUE
        self.ngram = ngram

        self.compiled_pattern = None  # regex compiled by the re module

    def get_match_query(self, simplify=True):
        if simplify:
            return self.match_query.simplify()
        return self.match_query

    def set_ngram(self, n):
        if isinstance(n, int):
            self.ngram = n
        else:
            raise Exception('Ngram value must be an int.')

    def add_to_exact(self, to_be_added):
        if isinstance(to_be_added, str):
            self.exact.add(to_be_added)
        elif isinstance(to_be_added, Iterable):
            self.exact.update(to_be_added)
        self.save_information('exact')
        self.discard_information('exact')

    def set_exact(self, exact):
        self.exact = set(exact)
        if len(self.exact) > self.EXACT_SET_MAXIMUM_SIZE:
            self.exact = set()

        self.save_information('exact')
        self.discard_information('exact')

    def set_prefix(self, prefix):
        self.prefix = set(prefix)
        self.save_information('prefix')
        self.discard_information('prefix')

    def set_suffix(self, suffix):
        self.suffix = set(suffix)
        self.save_information('suffix')
        self.discard_information('suffix')

    def set_emptyable(self, emptyable):
        self.emptyable = emptyable

    def set_match(self, match):
        self.match_query = match

    def save_information(self, save_info_in=None):
        """Information saving methods.
        See https://swtch.com/~rsc/regexp/regexp4.html for details
        """
        attrs_map = {'prefix': self.prefix, 'suffix': self.suffix, 'exact': self.exact}
        if save_info_in is None:
            for attr in attrs_map:
                new_match_query = self.match_query & generate_ngram_chars_logic_exp(attrs_map[attr], self.ngram)
                self.set_match(new_match_query)
        elif save_info_in in attrs_map:
            new_match_query = self.match_query & generate_ngram_chars_logic_exp(attrs_map[save_info_in], self.ngram)
            self.set_match(new_match_query)
        else:
            raise Exception('Unknown parameter value.')

    def discard_information(self, discard_info_in=None):
        """
        Information discarding methods.
        See https://swtch.com/~rsc/regexp/regexp4.html for details. Not all methods are implemented.
        TODO: Implement more methods in the above article.
        """
        if discard_info_in is None or discard_info_in == 'exact':
            if len(self.exact) > self.EXACT_SET_MAXIMUM_SIZE:
                self.exact = set()

    @classmethod
    def create_empty_expression(cls):
        return Token(name='TEXT', value='').to_exp()

    def set_compiled_pattern(self, pat):
        self.compiled_pattern = pat


RE_FUNCS = {
    'search': None, 'match': None, 'fullmatch': None,
    'split': 'string',  # return the original string in default
    'findall': [], 'finditer': iter(()),
    'sub': 'string', 'subn': 'string'
}

def handle_re_func(func_name):
    if not hasattr(re, func_name):
        print('Warning: The re module of your Python version does not have the "%s" function. \ '
              'Unexpected error will be raised when it is invoked' % func_name)
        return None

    def _re_func(self, string, *args, **kwargs):
        if not self.compiled_pattern:
            raise Exception('Must compile the pattern first.')

        if needs_regex(string, self.get_match_query()):
            return getattr(self.compiled_pattern, func_name)(string, *args, **kwargs)

        # return default value
        if RE_FUNCS[func_name] == 'string':
            return string
        else:
            return RE_FUNCS[func_name]
    return _re_func


for re_func in RE_FUNCS:
    setattr(Expression, re_func, handle_re_func(re_func))