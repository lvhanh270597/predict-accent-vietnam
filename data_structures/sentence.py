import re
from config import config
from nltk.tokenize import word_tokenize
class Sentence:
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    u = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ'
    B_C = '__begin__'
    E_C = '__end__'
    S_C = '\t'
    R_S = '__object__'
    replacements = {
        'phone': {
            'regrex': [re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', re.UNICODE)],
            'replace': '__phone__'
        },
        'number': {
            'regrex': [re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?', re.UNICODE)],
            'replace': '__num__'
        },
        'email': {
            'regrex': [re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}', re.UNICODE)],
            'replace': '__email__'
        },
        'name': {
            'regrex': [
                re.compile(r'[' + u + r'A-Z]+[\w]+,?\s+(?:[' + u + r'A-Z][\w]*\s*)*[' + u + r'A-Z][\w]+', re.UNICODE),
                re.compile(r'[' + u + r'A-Z]{3,5}', re.UNICODE)],
            'replace': '__name__'
        },
        'date': {
            'regrex': [re.compile(r"[\d]{1,2}/[\d]{1,2}(/[\d]{2,4})?", re.UNICODE),
                       re.compile(r"[\d]{1,2}-[\d]{1,2}(-[\d]{2,4})?", re.UNICODE)],
            'replace': '__date__'
        }
    }
    replace_items = ['__phone__', '__num__', '__name__', '__url__', '__email__', '__date__']

    def __init__(self, sentence=''):
        self.sentence = sentence
        self.word_cnt = sentence.split()
    def lower(self):
        self.sentence = self.sentence.lower()
    def tokenize(self):
        return ' '.join(word_tokenize(self.sentence))
    def extract(self, typeName):
        if typeName not in self.replacements: return []
        regrexes = self.replacements[typeName]['regrex']
        lst = []
        s = self.sentence
        for regrex in regrexes:
            lst.extend(re.findall(regrex, s))
            s = re.sub(regrex, '', s)
        return [(typeName, lst)]
    def extract_continue(self, lst=['email', 'phone', 'number', 'name', 'date']):
        res = []
        s = self.sentence
        for typeName in lst:
            res.extend(self.extract(typeName))
            self.sentence = self.remove(typeName, '')
        self.sentence = s
        return res
    def revert(self):
        lst = self.extract_continue()
        self.remove_continue()
        words = word_tokenize(self.sentence)
        for item in lst:
            key = item[0]
            values = item[1]
            replace_item = self.replacements[key]['replace']
            indices = [i for i, x in enumerate(words) if x == replace_item]
            for i in range(len(indices)):
                words[indices[i]] = values[i]
        return words

    def extract_n_gram(self, n, sentence, lower=True):
        lst = []
        sentence = sentence.lower()
        words = sentence.split()
        word_size = len(words)
        for i in range(word_size - n + 1):
            lst.append(tuple(words[i: i + n]))
        return lst

    def remove(self, typeName, replace=False):
        if typeName not in self.replacements:
            return self.sentence
        s = self.sentence
        regrexes = self.replacements[typeName]['regrex']
        if replace == False:
            replace = self.replacements[typeName]['replace']
        for regrex in regrexes:
            s = re.sub(regrex, replace, ' ' + s + ' ')
        return s

    def remove_no_replace(self, lst=['phone', 'number', 'measure', 'interval', 'date']):
        for typeName in lst:
            self.sentence = self.remove(typeName)
        return self.sentence

    def remove_continue(self, lst=['email', 'phone', 'number', 'name', 'date']):
        for typeName in lst:
            self.sentence = self.remove(typeName)
        for item in self.replace_items:
            self.sentence = re.sub(r'([^\s]+)(' + item + ')([^\s]*)', self.R_S + ' ', self.sentence)
        self.sentence = self.sentence.strip()
        for special in config.SPECIAL:
            self.sentence = self.sentence.replace(special, "")
        self.word_cnt = len(self.sentence.split())
        return self.sentence
    def check_object(self, word):
        return word.startswith('__') and word.endswith('__')

    def remove_no_vietnamese(self, word):
        return re.sub(r'(\d+)|([wjfz]+)', '', word)

    def check_has_accent(self, input_str):
        return (input_str != self.remove_accents(input_str))
    def remove_accents(self, input_str):
        s = ''
        for c in input_str:
            if c in self.s1:
                s += self.s0[self.s1.index(c)]
            else:
                s += c
        return s
