"""
The test data in test_suite.dat is "stolen" from https://github.com/xysun/regex.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import smart_regex as re


def testing():
    with open('test_suite.dat') as f:
        lines = [l.strip() for l in f.readlines()]
    for line in lines:
        fields = line.split()
        pattern = fields[0]
        pos_text = fields[1]
        neg_text = fields[2] if len(fields) == 3 else None

        r = re.compile(pattern)
        mat = r.fullmatch(pos_text)
        if not mat or len(mat) > 1 or mat[0][2].group() != pos_text:
            print('Pattern: %s' % pattern)
            print('Pos text: %s' % pos_text)
            print('Got mat: %s' % str(None) if not mat else mat.group())
            print('\n')

        if neg_text:
            mat = r.fullmatch(neg_text)
            if mat:
                print('Pattern: %s' % pattern)
                print('Neg text: %s' % neg_text)
                print('Got: %s' % mat.group())
                print('\n')


def profile_speed():
    patterns = [
        '姓 +名'
    ]
    re_patterns = [re.compile(pat) for pat in patterns]
    folder = r'E:\Study\my_github\smart regex\test\test_data'
    lines = []
    for fname in os.listdir(folder):
        if fname.endswith('txt'):
            with open(os.path.join(folder, fname), encoding='utf-8') as f:
                lines.extend(l.strip() for l in f.readlines())
    # lines = lines * 200
    re_results = []
    for line in lines:
        for re_pat in re_patterns:
            mat = re_pat.search(line)
            # if mat:
            #     re_results.append(mat.group())


# cProfile.run('profile_speed()')
if __name__ == '__main__':
    testing()


