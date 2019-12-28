from itertools import product


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


def concat_strings_of_two_lists(str_list1, str_list2):
    """
    >>> concat_strings_of_two_lists(['a', 'b'], ['c', 'd'])
    ['ac', 'ad', 'bc', 'bd']
    >>> concat_strings_of_two_lists(['a', 'b'], [])
    ['a', 'b']
    """
    if not str_list1:
        return str_list2
    if not str_list2:
        return str_list1
    product_result = product(str_list1, str_list2)
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

def generate_ngram_chars_for_str_set(str_set, n):
    """
    >>> generate_ngram_chars_for_str_set(['ab','abcd'], 3)
    [[], ['abc', 'bcd']]
    >>> generate_ngram_chars_for_str_set(['abcd','xwyz'], 3)
    [['abc', 'bcd'], ['xwy', 'wyz']]
    """
    return [generate_ngram_chars(s, n) for s in str_set]



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(generate_ngram_chars_for_str_set(['abcd','xwyz'],3))
