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

    def __repr__(self):
        return self.name + ":" + self.value

    def to_term(self):
        """本 token 转换成一个 term"""
        term = Term([self])
        term.emptyable = False
        term.exact, term.prefix, term.suffix = {self.value}, {self.value}, {self.value}
        term.match = set()
        return term



class Term:
    """一个 term 是正则中的一个匹配单位，由 tokens 合并而成
    Examples:
        a: a 作为一个 token 也可以是一个 term
        a+b: a+b 本身是一个 term
        (a+b) | (cd): a+b 和 cd 各是一个 term
        a|b: a 和 b 各是一个 term
    """
    EXACT_SET_MAXIMUM_SIZE = 100  # clear the exact set when its size goes over maximum size to save memory

    def __init__(self, tokens):
        self.tokens = tokens  # a list of tokens
        self.emptyable = None
        self.exact = set()  # empty set corresponds to "unknown" in https://swtch.com/~rsc/regexp/regexp4.html
        self.prefix = set()
        self.suffix = set()
        self.match = set()  # empty set corresponds to "any" in https://swtch.com/~rsc/regexp/regexp4.html

    def __repr__(self):
        return ''.join([t.value for t in self.tokens])

    def concat_with(self, term):
        """和另一个 term 合并"""
        self.tokens.extend(term.tokens)

    def add_to_exact(self, str):
        self.exact.add(str)
        if len(self.exact) > self.EXACT_SET_MAXIMUM_SIZE:
            self.exact = set()


    # def _update_set_with(self, update_set='exact', another_set=None):
