
def read_levels():
    lists = []
    fh = open('data/levels.txt', 'r')
    for line in fh:
        chars_only = line.strip()
        if len(chars_only) == 0:
            continue
        if chars_only.startswith('#'):
            continue
        lists.append(set(chars_only))
    fh.close()
    lists.append(set())
    return lists

sets = read_levels()

def get_level(word):
    max = -1
    for ch in word:
        idx = -1
        for i in range(len(sets)):
            if ch in sets[i]:
                idx = i
        if idx == -1:
            idx = len(sets) - 1
            sets[idx].add(ch)
        if idx > max:
            max = idx

    return max

def get_unencountered():
    return list(sorted(sets[-1]))


