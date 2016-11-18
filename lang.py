import random, pickle, re
import tkinter as t

def doprobs(freq):
    if type(freq) is list:
        return random.choice(freq)
    
    total = 0
    for elem in freq:
        total += freq[elem]
    if total == 0:
        raise ValueError('Nothing to choose from here')
    r = random.random() % total

    threshold = 0
    for elem in freq:
        threshold += freq[elem]
        if r < threshold:
            return elem

def analyze(generator, trials=10000):
    """
    analyzes output of f
    returns dictionary of output:frequency
    """
    d = {}
    for i in range(trials): 
        output = next(generator)
        try:
            d[output] += 1
        except KeyError:
            d[output] = 1
    for output in d:
        d[output] /= trials
    return d

class NeoLang():
    def __init__(self):
        self.ALPHA = 'ABDEFGĞHIÎKLMNOPRŘSŞTUVWXYZ'
    def gen_pair(self, precedent):
        """
        generates a pair of consonants
        """
        if precedent == None or precedent == ' ':
            first = doprobs(self.LETTERS)
        else:
            first = doprobs(self.NEXTS[precedent])
        try:
            second = doprobs(self.NEXTS[first])
        except ValueError:
            return first
        if self.slurr_pair(first, second, precedent=precedent):
            return first+second
        else:
            return first+"'"+second
    def slurr_pair(self, first, second, precedent=' '):
        """
        is this pair of letters, slurred if this scenario?
        """
        if first+second in self.SLURRED:
            return True
        elif second not in self.TYPE_I and precedent not in self.VOWELS:
            return False
        elif first in self.TYPE_I or second in self.TYPE_I:
            if first+second in self.NOT_SLURRED:
                return False
            else:
                return True
        else:
            return False
    def template_gen(self,template):
        word = ' '
        last = ' '
        for letter in template:
            if last == '*':
                word += letter
            elif letter == 'c' or letter == 'C':
                if last == 'c' and self.slurr_pair(last, letter):
                    word += "'"
                word += doprobs(self.CONSONANTS)
                last = 'c'
            elif letter == 'v' or letter == 'V':
                word += doprobs(self.VOWELS)
                last = 'v'
            elif letter == "'":
                word += "'"
                last = "'"
            else:
                last = letter
                
        return word
    def gen(self, s=2, prefix=' ', suffix=''):
        """
        generates a two syllable word
        """
        word = ' '
        for syllable in range(s):
            if random.random() < 0.4:
                word += self.gen_pair(word[-1])
            else:
                word += doprobs(self.CONSONANTS)
            word += doprobs(self.VOWELS)
        word += suffix
        return word
    def letter_info(self, letter):
        """
        returns some info about the letter
        """
        letter = letter.upper()
        d = self.NEXTS[letter]
        print("Possible consonants that follow",letter)
        for char in d.keys():
            if self.slurr_pair(letter, char): s="slurred"
            else: s="not slurred"
            print("\t"+char+": "+str(100*d[char])+"% ("+s+")")

class NNT1(NeoLang):
    # updated as of Nov 12
    def __init__(self):
        self.ALPHA = 'ABDEFGĞHIÎKLMNOPRŘSŞTUVWXYZ' # vowels: AEIÎUOaeiîo consonants: BDFGĞHKLMNPRŘSŞTVWXYZbdfgğhklmnprřsştvwxyz
        self.VOWELS = {'A': .16, 'E': .16, 'I': .16, 'Î': .16, 'O': .16, 'U': .16}
        self.CONSONANTS = {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16}
        self.LETTERS = {'A': .04, 'B': .04, 'D': .04, 'E': .04, 'F': .04, 'G': .04, 'Ğ': .04, 'H': .04, 'I': .04, 'Î': .04, 'K': .04, 'L': .04, 'M': .04, 'N': .04, 'O': .04, 'P': .04, 'R': .04, 'Ř': .04, 'S': .04, 'Ş': .04, 'T': .04, 'U': .04, 'V': .04, 'W': .04, 'Y': .04, 'Z': .04}
        self.NEXTS = { # for each letter, the probabilities that another letter will follow it (excluding vowels, which can always follow a given letter)
            'A': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'B': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25},
            'D': {'R':.20, 'Ř':.20, 'W':.20, 'X':.20, 'Y':.20},
            'E': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'F': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25},
            'G': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25},
            'Ğ': {'R':1.0},
            'H': {'Y':.33},
            'I': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'Î': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'K': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25}, 
            'L': {'B':.07, 'D':.07, 'F':.07, 'G':.07, 'K':.07, 'M':.07, 'N':.07, 'P':.07, 'S':.07, 'Ş':.07, 'T':.07, 'V':.07, 'X':.07, 'Z':.07},
            'M': {'R':.08, 'Ř':.08, 'F':.08, 'G':.08, 'K':.08, 'N':.08, 'S':.08, 'Ş':.08, 'V':.08, 'X':.08, 'Y':.08, 'Z':.08},
            'N': {'B':.08, 'D':.08, 'F':.08, 'K':.08, 'P':.08, 'R':.08, 'Ř':.08, 'S':.08, 'Ş':.08, 'V':.08, 'X':.08, 'Y':.08, 'Z':.08},
            'O': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'P': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25},
            'R': {'B':.07, 'D':.07, 'F':.07, 'G':.07, 'Ğ':.07, 'K':.07, 'L':.07, 'M':.07, 'N':.07, 'P':.07, 'S':.07, 'T':.07, 'V':.07, 'X':.07, 'Z':.07},
            'Ř': {'B':.07, 'D':.07, 'F':.07, 'G':.07, 'Ğ':.07, 'K':.07, 'L':.07, 'M':.07, 'N':.07, 'P':.07, 'S':.07, 'T':.07, 'V':.07, 'X':.07, 'Z':.07},
            'S': {'K':.13, 'P':.13, 'M':.13, 'N':.13, 'T':.13, 'V':.13, 'W':.13, 'Y':.13},
            'Ş': {'K':.13, 'P':.13, 'M':.13, 'N':.13, 'T':.13, 'V':.13, 'W':.13, 'Y':.13},
            'T': {'R':.14, 'Ř':.14, 'S':.14, 'Ş':.14,'W':.14, 'X':.14, 'Y':.14},
            'U': {'B': .05, 'D': .05, 'F': .05, 'G': .05, 'Ğ': .05, 'H': .05, 'K': .05, 'L': .05, 'M': .05, 'N': .05, 'P': .05, 'R': .05, 'Ř': .05, 'S': .05, 'Ş': .05, 'T': .05, 'V': .05, 'X': .05, 'W': .05, 'Y': .05, 'Z': .16},
            'V': {'R':.25, 'Ř':.25, 'W':.25, 'Y':.25},
            'X': {'R':.50, 'Ř':.50},
            'W': {},
            'Y': {},
            'Z': {'W':.50, 'Y':.50}
            }
        
        self.TYPE_I = [ # consonants that generally slurr together with other consonants
            'R',
            'Ř',
            'W',
            'Y'
            ]
        self.NOT_SLURRED = [ # exceptions: where type I consonants don't slurr
            'RL',
            'ŘL',
            'LR',
            'LŘ',
            'RB',
            'ŘB'
            ]
        self.SLURRED = [ # exceptions: where non type I consonants slurr
            'DX',
            'TS',
            'TŞ',
            'KS',
            ]
        self.percents = [self.VOWELS, self.CONSONANTS, self.LETTERS]
        for char in self.NEXTS:
            self.percents.append(self.NEXTS[char])
    def fix_percentages(self):
        for dicto in self.percents:
            total = sum(dicto.values())
            if total != 0:
                for key in dicto:
                    val = dicto[key]
                    dicto[key] = val / total

        
        
class Menu():
    class Bundle():
        def __init__(self, entry=None, output=None):
            self.entry = entry
            self.output = output
        def pack(self):
            self.entry.pack()
            self.output.pack()
        def get(self):
            return self.entry.get()
        def set(self, value):
            return self.output.config(text=value)
    
    def __init__(self, obj=None):
        if obj == None:
            self.unloaded = True
            self.filepath = 'no filepath'
        else:
            self.unloaded = False
            self.filepath = 'default object'
        self.unsaved = False
        self.object = obj

        topack = []
        self.root = t.Tk()
        self.root.geometry('{}x{}'.format(500,500))
        self.root.wm_title('Neoneotakua Construction')

        self.con_bund = self.Bundle(entry=t.Entry(self.root), output=t.Label(self.root,text='^^ leave blank or use c/v to mark consonants/vowels ^^'))
        self.load_bund = self.Bundle(entry=t.Entry(self.root), output=t.Label(self.root,text=self.filepath+' is loaded'))
        self.prcnt_bund = self.Bundle(entry=t.Entry(self.root), output=t.Label(self.root,text='Edit letter or letter combo percentages'))
        self.prcnt_scale = t.Scale(self.root, from_=0, to_=1, orient=t.HORIZONTAL, resolution=0.01)
        self.copy_bund = self.Bundle(entry=t.Entry(self.root), output=t.Label(self.root,text='Save file or save file as'))
        topack = [
            self.load_bund,
            t.Button(self.root, text='LOAD', command=self.load),
            t.Frame(height=4, bd=1, relief=t.SUNKEN),
            self.con_bund,
            t.Button(self.root, text='CONSTRUCT', command=self.construct),
            t.Frame(height=24, bd=1, relief=t.SUNKEN),
            self.prcnt_bund,
            self.prcnt_scale,
            t.Button(self.root, text='EDIT', command=self.edit),
            t.Frame(height=24, bd=1, relief=t.SUNKEN),
            self.copy_bund,
            t.Button(self.root, text='SAVE', command=self.copy)
            ]

        for element in topack: element.pack()
    def display(self, dictionary, prefix='\t'):
        for char in self.object.ALPHA:
            try:
                toPrint = dictionary[char]
            except KeyError:
                pass
            else:
                if type(toPrint) is not dict:
                    print(prefix+char+':', toPrint)
                else:
                    print(prefix+char+':')
                    self.display(toPrint, prefix=prefix+'\t')
    def load(self):
        self.save()
        path = self.load_bund.get()
        if re.match(r'^\w+$', path):
            try:
                with open(path+'.p', 'rb') as file:
                    self.object = pickle.load(file)
            except FileNotFoundError:
                print('Invalid filename')
                result = 'could not find that filename'
            else:
                self.unloaded = False
                self.filepath = path+'.p'
                result = self.filepath+' is loaded'
        else:
            result = 'could not load file.'
        self.load_bund.set(result)
    def construct(self, arg=[]):
        if self.unloaded:
            print('Nothing to construct - no object loaded')
        else:
            line = self.con_bund.get()
            if line == '':
                result='Generated:'+self.object.gen()
            elif re.match(r"^[cvCV*BDFGĞHKLMNPRŘSŞTWXYZbdfgğhklmnprřsştwxyzAEIÎUOaeiîou]+$", line):
                result='Generated:'+self.object.template_gen(line)
            else:
                result='Could not generate.'
            self.con_bund.set(result)
    def edit(self, arg=[]):
        print('--Editting Menu--')
        if self.unloaded:
            print('Nothing to edit - no object loaded')
        else:
            self.unsaved = True
            line = self.prcnt_bund.get()
            percent = self.prcnt_scale.get()
            if re.match(r'^[AEIÎUOaeiîou]$', line): # vowel
                self.object.VOWELS[line] = percent
            elif re.match(r'^[BDFGĞHKLMNPRŘSŞTVWXYZbdfgğhklmnprřsştvwxyz]$', line): # consonant
                self.object.CONSONANTS[line] = percent
            elif re.match(r'^[BDFGĞHKLMNPRŘSŞTVWXYZbdfgğhklmnprřsştvwxyz]{2}$', line): # nexts thing
                self.object.NEXTS[line[0]][line[1]] = percent
            else:
                self.unsaved = False
            if self.unsaved:
                self.prcnt_bund.set("'"+line+'\' percentage changed: '+str(percent))
            else:
                self.prcnt_bund.set('could not update.')
    def save(self, arg=[]):
        print('--Save File--')
        if self.unsaved:
            if self.unloaded or self.filepath == 'default object':
                print('No file to save - no file loaded')
            else:
                print('--Fixing percentages--')
                self.object.fix_percentages()
                print('--Percentages fixed--')
                pickle.dump(self.object, open(self.filepath, 'wb'))
            self.unsaved = False
            print('--Saved to',self.filepath+'--')
        else:
            print('--File',self.filepath,'already saved--')
    def copy(self, arg=[]):
        print('--Copy File--')
        if self.unloaded:
            print('No file to copy - no object loaded')
        else:
            line = self.copy_bund.get()
            if line == '': # just saving
                self.save()
                result = 'saving '+self.filepath
            elif re.match(r'^\w+$', line): # making a copy
                with open(line+'.p', 'wb') as file:
                        pickle.dump(self.object, file)
                result = 'saving '+self.filepath+' as '+line+'.p'
            else:
                result = 'could not save'
            self.copy_bund.set(result)
m = Menu(NNT1())

