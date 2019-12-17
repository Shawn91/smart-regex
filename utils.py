def count_list_elements(l, count=None):
    """Count the number of elements after flattening a list and the number of nested lists
    Examples:
        [1,2]: returns {'ele': 2, 'list': 0}
        [1,2,[3,4]]: returns {'ele': 4, 'list': 1}
        [1,2, [3,[4]]]: returns {'ele': 4, 'list': 2}
    """
    if count is None:
        count = {'ele':0, 'list':0}
    for ele in l:
        if isinstance(ele, list):
            count['list'] += 1
            count_list_elements(ele, count)
        else:
            count['ele'] += 1
    return count

if __name__ == '__main__':
    l = [1,2,[3,[4]]]
    print(count_list_elements(l))
