"""
TODO:
1. flags
2. cache n-grams and expressions
3. *? non-greedy search
"""
import re

from compile import compile_tokens_to_expression


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
    exp = compile('欧 *阳|独 *孤|令 *狐|皇 *甫|夏 *侯|呼 *延|诸 *葛|完 *颜|拓 *跋|公 *孙|宇 *文|北 *野|欧 *文|上 *官|端 *木|轩 *辕|慕 *蓉|公 *叔|司 *寇|百 *里|司 *马|北 *门|拓 *拔|慕 *容|独 *狐|爱 *新 *觉 *罗|尉 *迟|歐 *陽|叶 *赫 *纳 *拉|兀 *颜|司 *徒|耶 *律|单 *于|西 *门|公 *延|第 *五|令 *孤|北 *堂|蔚 *迟|西 *伯|申 *屠|公 *输')
    print(exp.search('欧 阳'))
    print(exp.search('abef'))
    print(exp.search('abcdcdef'))
