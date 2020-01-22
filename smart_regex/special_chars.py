from smart_regex.data_structs import Token, Expression
from smart_regex.boolean_operations import BOOL_TRUE, BOOL_FALSE


class AnyToken(Token):
    """Corresponds to '.' in the re module."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_speical_char = True
        self.name = SPECIAL_CHARS['.']['name']
        self.value = '.'

    def to_exp(self):
        exp = Expression([self])
        exp.emptyable = False
        exp.exact, exp.prefix, exp.suffix = {''}, {''}, {''}
        self.match = BOOL_TRUE
        return exp


SPECIAL_CHARS = {
    '.': {'name': 'ANY', 'handle_func': AnyToken}
}
