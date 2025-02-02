
def read_levels():
    level_sets = []
    fh = open('data/levels.txt', 'r')
    for line in fh:
        chars_only = line.strip()
        if len(chars_only) == 0:
            continue
        if chars_only.startswith('#'):
            continue
        level_sets.append(set(chars_only))
    fh.close()
    level_sets.append(set())
    return list(map(lambda set: dict(zip(set, [0] * len(set))), level_sets))

counts = read_levels()

def get_char_level(ch):
    level = -1
    for l in range(len(counts)):
        if ch in counts[l]:
            level = l
    if level == -1:
        level = len(counts) - 1
        counts[level][ch] = 0
    counts[level][ch] += 1
    return level

def get_level(word):
    return max(map(get_char_level, word))

def get_unencountered():
    return list(sorted(counts[-1].keys()))


