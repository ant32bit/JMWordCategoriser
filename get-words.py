import levels
from jmdict import JMDictIterator

if __name__ == "__main__":
    all_count = 0
    inc_count = 0
    excl_counts = {
        'lvl': 0,
        'pri': 0,
        'def': 0
    }
    lvl_count = [0] * 13
    entries = []
    for i in range(len(lvl_count)):
        entries.append([])

    include_priorities = set(['news1', 'ichi1', 'spec1'])
    exclude_def_tags = set(['work', 'product', 'company', 'given'])
    for entry in JMDictIterator('data/JMDict.json'):
        all_count += 1

        level = 0
        priority = None
        value = None
        reading = None
        first_type = None
        first_def = None

        priority_tags = entry.tags.intersection(include_priorities)
        if len(priority_tags) == 0:
            excl_counts['pri'] += 1
            continue
        
        priority = list(sorted(priority_tags))[0]

        level = levels.get_level(entry.value)
        if level <= 0:
            excl_counts['lvl'] += 1
            continue
        
        value = entry.value
        reading = entry.reading

        definition = None
        for d in entry.definitions:
            if d.tags.intersection(exclude_def_tags):
                continue
            definition = d
        if definition is None:
            excl_counts['def'] += 1
            continue

        first_type = definition.type
        first_def = definition.glossary[0]
        
        inc_count += 1
        lvl_count[level] += 1
        entries[level].append(value)

        print(f"{level} {priority}: {value} ({reading}) ({first_type} {first_def})")

    print("\n".join(entries[0]))

    print(f"Entries: {inc_count} / {all_count}")
    for i in range(len(lvl_count)):
        print(f"Level {i}: {lvl_count[i]}")
    for t in excl_counts:
         print(f"Exclude {t}: {excl_counts[t]}")

    print(''.join(levels.get_unencountered()))



