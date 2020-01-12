"""
TODO:
1. flags
2. cache n-grams of texts that will be regex-searched against
3. implement functions like re.escape, re.search
"""
import re

from compile import compile_tokens_to_expression
from utils import generate_ngram_chars
import config


def compile(pattern, flags=0):
    # use the re module to compile the pattern first to make sure it's a valid regex pattern
    regex = re.compile(pattern, flags=flags)
    exp, _ = compile_tokens_to_expression(pattern)

    exp.set_compiled_pattern(regex)
    return exp


if __name__ == '__main__':
    exp = compile('a(b|c)')
    print(exp.search('ef'))