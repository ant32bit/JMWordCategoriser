import levels
from jmdict import JMDictIterator

if __name__ == "__main__":
    all_count = 0
    pri_count = 0
    lvl_count = [0] * 13
    entries = []
    for i in range(len(lvl_count)):
        entries.append([])

    for entry in JMDictIterator('data/JMDict.json'):
        all_count += 1

        pri = None
        for p in ['news1', 'ichi1', 'spec1']:
            if (p in entry.priority):
                pri = p
                break
        
        if pri is not None:
            l = levels.get_level(entry.value)
            if l > 0:
                pri_count += 1
                
                lvl_count[l] += 1
                entries[l].append(entry.value)

                print(f"{l} {pri}: {entry.value} ({entry.reading}) ({entry.type} {entry.definition})")

    print("\n".join(entries[0]))

    print(f"Entries: {pri_count} / {all_count}")
    for i in range(len(lvl_count)):
        print(f"Level {i}: {lvl_count[i]}")

    

    print(''.join(levels.get_unencountered()))



