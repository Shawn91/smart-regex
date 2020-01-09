from collections import Iterable
from typing import List


from utils import generate_ngram_chars, bool_algebra
from config import NGRAM_FOR_CHINESE, NGRAM_FOR_ENGLISH



class Token:
    """一个 token 就是正则中的一个字符。可以是纯字符，如a; 也可以是一个操作符，如?
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
            self.match = algebra.symbols('true')
            return exp
        raise Exception('Only tokens of plain characters could be converted to an expression')




class Expression:
    """一个 exp 是正则中的一个匹配单位，由 tokens 合并而成
    Examples:
        a: a 作为一个 token 也可以是一个 expression
        a+b: a+b 本身是一个 expression
        (a+b) | (cd): a+b 和 cd 各是一个 expression
        a|b: a 和 b 各是一个 expression
    """
    EXACT_SET_MAXIMUM_SIZE = 100  # clear the exact set when its size goes beyond maximum size to save memory

    def __init__(self, tokens=None, exps=None, ngram=NGRAM_FOR_CHINESE):
        self.tokens = [] if tokens is None else tokens  # a list of tokens
        self.subexps = [] if exps is None else exps # a list of sub expressions
        self.emptyable = None
        self.exact = set()  # empty set corresponds to "unknown" in https://swtch.com/~rsc/regexp/regexp4.html
        self.prefix = set()
        self.suffix = set()

        # match should be a boolean expression. For details, see https://booleanpy.readthedocs.io/en/latest/users_guide.html
        # Symbol "true" corresponds to "ANY" in https://swtch.com/~rsc/regexp/regexp4.html
        self.match = algebra.symbols('true')

        self.ngram = ngram
        

    def get_last_subexp(self):
        return self.subexps[-1]

    def pop_subexp(self):
        return self.subexps.pop()

    def add_subexp(self, subexp):
        self.subexps.append(subexp)

    def merge_all_subexps(self):
        """ Merge all sub-expressions into a large one"""
        new_exp = Expression()
        new_exp.set_subexps(self.subexps)
        self.set_subexps([new_exp])

    def set_subexps(self, subexps: List):
        if not isinstance(subexps, list):
            raise Exception('subexps parameter accepts a list of expressions.')
        self.subexps = subexps


    def __repr__(self):
        return ''.join([t.value for t in self.tokens])

    def set_ngram(self, n):
        if isinstance(n ,int):
            self.ngram = n
        else:
            raise Exception('Ngram value must be an int.')


    def add_to_exact(self, to_be_added):
        if isinstance(to_be_added, str):
            self.exact.add(to_be_added)
        elif isinstance(to_be_added, Iterable):
            self.exact.update(to_be_added)
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
        self.match = match

    def save_information(self, save_info_in=None):
        """Information saving methods.
        See https://swtch.com/~rsc/regexp/regexp4.html for details
        """
        attrs_map = {'prefix': self.prefix, 'suffix':self.suffix, 'exact': self.exact}
        if save_info_in is None:
            for attr in attrs_map:
                self.match.update(generate_ngram_chars(attrs_map[attr], self.ngram))
        elif save_info_in in attrs_map:
            self.match.update(generate_ngram_chars(attrs_map[save_info_in], self.ngram))
        else:
            raise Exception('Unknown parameter value.')

    def discard_information(self, discard_info_in=None):
        """
        Information discarding methods.
        See https://swtch.com/~rsc/regexp/regexp4.html for details. Only some methods are implemented.
        """
        if discard_info_in is None or discard_info_in == 'exact':
            if len(self.exact) > self.EXACT_SET_MAXIMUM_SIZE:
                self.exact = set()

    def count_subexps(self, count=None):
        if count is None:
            # leaf_exp: an expression with no sub-expressions
            count = {'leaf_exp': 0, 'non_leaf_exp': 0}
        for subexp in self.subexps:
            if subexp.subexp:
                count['non_leaf_exp'] += 1
                subexp.count_subexps(count=count)
            else:
                count['leaf_exp'] += 1
        return count

