"""
TODO:
1. flags
2. cache n-grams and expressions
3. *? non-greedy search
4. complete codes for special chars including AnyToken
"""
import re

from smart_regex.compile import compile_tokens_to_expression


def compile(pattern, flags=0):
    # use the re module to compile the pattern first to make sure it's a valid regex pattern
    regex = re.compile(pattern, flags=flags)
    exp, _ = compile_tokens_to_expression(pattern)

    exp.set_compiled_pattern(regex)
    return exp


def search(pattern, string, flags=0):
    return compile(pattern, flags).search(string)


def match(pattern, string, flags=0):
    return compile(pattern, flags).match(string)


def fullmatch(pattern, string, flags=0):
    return compile(pattern, flags).fullmatch(string)


def sub(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).sub(repl, string, count)


def subn(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).subn(repl, string, count)


def split(pattern, string, maxsplit=0, flags=0):
    return compile(pattern, flags).split(string, maxsplit)


def findall(pattern, string, flags=0):
    return compile(pattern, flags).findall(string)


def finditer(pattern, string, flags=0):
    return compile(pattern, flags).finditer(string)


def purge():
    return re.purge()


def escape(pattern):
    return re.escape(pattern)


def template(pattern, flags=0):
    print("Warning: template function simply invokes the re module's template function without doing nothing else.")
    return re.compile(pattern, flags | re.RegexFlag.T)


for attr in ["error", "Pattern", "Match", "A", "I", "L", "M", "S", "X", "U",
             "ASCII", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "VERBOSE", "UNICODE"]:
    globals()[attr] = getattr(re, attr)


# 测试用，要删除
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

if __name__ == '__main__':
    exp = compile('已 *婚|(已|未)结 *婚')
    print(exp.fullmatch('已婚'))
    print(exp.search('abef'))
    print(exp.search('abcdcdef'))
