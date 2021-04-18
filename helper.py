import itertools


# I found an elegant solution on Stackoverflow which I copied: https://stackoverflow.com/questions/323750/how-to-access-the-previous-next-element-in-a-for-loop/41047005#41047005
def pairwise_helper(iterable):
    '''
    we pass paths to the function which look like this: [startNode, v1, v2, v3,.. , endNode].
    returned path would be: (startNode,v1), (v1,v2), (v2, v3), ... , (vn, endNode)
    '''
    ""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def get_list_of_edges(iterable):
    return list(itertools.chain.from_iterable(iterable))    


'''
code snipped was taken from
https://stackoverflow.com/questions/39192777/how-to-split-a-list-into-n-groups-in-all-possible-combinations-of-group-length-a
this solution was much cleaner, and faster, since it does not filter elements from a much larger set of possible combinations.
'''
def _sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in shortlex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)

    # Sort the parts in each partition in shortlex order
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]

    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))

    return result        