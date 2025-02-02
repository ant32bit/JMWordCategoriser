import json

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
                entry = self.fh.__next__().strip()
                if entry == ']':
                    raise StopIteration()
                entryObj = json.loads(entry[:-1])
                return JMDictEntry(entryObj)

            except StopIteration as s:
                self.inner_iter = None
                self.fh.close()
                self.fh = None
                raise StopIteration()

class JMDictEntry:

    def __init__(self, entryObj):
        self.value = None
        self.priority = set()
        self.reading = None
        self.type = None
        self.definition = None
        
        if ('k_ele' in entryObj):
            k_ele = entryObj['k_ele'][0]
            self.value = k_ele['keb']

            if 'ke_pri' in k_ele:
                self.priority = set(k_ele['ke_pri'])
        
        if ('r_ele' in entryObj):
            r_ele = entryObj['r_ele'][0]
            self.reading = r_ele['reb']
            if self.value is None:
                self.value = self.reading
            
            if self.priority is None and 're_pri' in r_ele:
                self.priority = set(r_ele['re_pri'])

        if ('sense' in entryObj):
            sense = entryObj['sense'][0]
            if 'pos' in sense:
                self.type = sense['pos'][0]
            if 'misc' in sense and '&uk;' in sense['misc']:
                self.value = self.reading
            self.definition = sense['gloss'][0]['xml:content']

