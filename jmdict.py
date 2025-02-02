import json

_ke_inf_exclusions = set(['ik', 'iK', 'io', 'oK', 'rK', 'sK'])
_re_inf_exclusions = set(['ik', 'ok', 'rk', 'sk'])
_sense_exclusions = set(['arch', 'derog', 'vulg', 'X'])

class JMDictIterator:

    def __init__(self, file):
        self.file = file
        self.fh = None
        self.inner_iter = None

    def __iter__(self):
        if self.fh is not None:
            self.inner_iter
            self.fh.close()
        self.fh = open(self.file, 'r')
        self.inner_iter = self.fh.__iter__()
        self.fh.__next__()
        return self

    def __next__(self):
        if self.fh is not None:
            try:
                while(True):
                    entry = self.fh.__next__().strip()
                    if entry == ']':
                        raise StopIteration()
                    entryObj = json.loads(entry[:-1])
                    entry = build_entry(entryObj)
                    if entry is not None:
                        return entry

            except StopIteration as s:
                self.inner_iter = None
                self.fh.close()
                self.fh = None
                raise StopIteration()

def clean_tags(tags):
    return set(map(lambda x: x[1:-1], tags))  

def build_entry(obj): 
    seq_id = obj['ent_seq']
    nk = 0
    nr = 0
    nd = 0
    tags_set = set()
    alt_kanji = []
    alt_readings = []

    kanji = None
    reading = None
    definitions = []
    
    if ('k_ele' in obj):
        nk = len(obj['k_ele'])
        for k in obj['k_ele']:
            is_alt = kanji is not None
            if 'ke_inf' in k:
                ke_inf_set = clean_tags(k['ke_inf'])
                if ke_inf_set.intersection(_ke_inf_exclusions):
                    continue
                if '&ateji;' in ke_inf_set:
                    is_alt = True
            if not is_alt:
                kanji = k['keb']
                if 'ke_pri' in k:
                    tags_set = tags_set.union(set(k['ke_pri']))
            else:
                alt_kanji.append(k['keb'])

    if ('r_ele' in obj):
        nr = len(obj['r_ele'])
        for r in obj['r_ele']:
            is_alt = reading is not None
            if 're_inf' in r:
                re_inf_set = clean_tags(r['re_inf'])
                if re_inf_set.intersection(_re_inf_exclusions):
                    continue
            if not is_alt:
                reading = r['reb']
                if 're_pri' in r:
                    tags_set = tags_set.union(set(r['re_pri']))
            else:
                alt_readings.append(r['reb'])
    
    if ('sense' in obj):
        nd = len(obj['sense'])
        for d in obj['sense']:
            if ('pos' not in d):
                continue
            type = ' '.join(map(lambda x: x[1:-1] + '.', d['pos']))
            glossary = []
            def_tags_set = set()
            if ('misc' in d):
                re_misc_set = clean_tags(d['misc'])
                if re_misc_set.intersection(_sense_exclusions):
                    continue
                def_tags_set = def_tags_set.union(re_misc_set)
            for entry in d['gloss']:
                if 'xml:lang' in entry and entry['xml:lang'] != 'eng':
                    continue
                glossary.append(entry['xml:content'])
            if glossary:
                definitions.append(JMDictDefinition(type, glossary, def_tags_set))
    
    if (not kanji and not reading) or not definitions:
        return None
    
    debug = JMDictDebugInfo(seq_id, nk, nr, nd)
    return JMDictEntry(kanji, reading, definitions, tags_set, alt_kanji, alt_readings, debug)


class JMDictDefinition:
    def __init__(self, type, glossary, tags=None):
        self.type = type
        self.glossary = glossary if glossary is not None else list()
        self.tags = tags if tags is not None else set()

class JMDictDebugInfo:
    def __init__(self, seq_id, k_count, r_count, d_count):
        self.seq_id = seq_id
        self.counts = {
            'kanji': k_count,
            'reading': r_count,
            'definition': d_count
        }

class JMDictEntry:
    def __init__(self, kanji, reading, definitions: list[JMDictDefinition], tags=None, alt_kanji=None, alt_readings=None, debug_info:JMDictDebugInfo=None):
        self.value = kanji if kanji is not None else reading
        self.kanji = kanji
        self.reading = reading
        self.definitions = definitions if definitions is not None else list()
        self.tags = tags if tags is not None else set()
        self.alt_kanji = alt_kanji if alt_kanji is not None else list()
        self.alt_readings = alt_readings if alt_readings is not None else list()
        self.debug_info = debug_info
