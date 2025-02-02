from jmdict import JMDictIterator

def display_entry(entry):
    if entry.value != entry.reading:
        print(f"{entry.value} ({entry.reading})")
    else:
        print(entry.value)
    if entry.alt_kanji:
        print(', '.join(entry.alt_kanji))
    if entry.alt_readings:
        print(', '.join(entry.alt_readings))
    if entry.tags:
        print(', '.join(entry.tags))
    for definition in entry.definitions:
        if (definition.tags):
            print (f"{definition.type} ({', '.join(definition.tags)})")
        else:
            print(definition.type)
        for g in definition.glossary:
            print(g)
    print("")

if __name__ == "__main__":
    for entry in JMDictIterator('data/JMDict.json'):
        if entry.debug_info.counts['kanji'] > (len(entry.alt_kanji) + 1):
            display_entry(entry)
