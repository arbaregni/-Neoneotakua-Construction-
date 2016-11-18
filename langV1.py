import random, pickle, re

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
        self.ALPHA = 'ABDEFGĞHIÎKLMNOPRŘSŞTUVWXYZ'
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
    def __init__(self, obj=None):
        if obj == None:
            self.unloaded = True
            self.filepath = 'no filepath'
        else:
            self.unloaded = False
            self.filepath = 'default object'
        self.unsaved = False
        self.object = obj
        
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
    def main_menu(self):
        stack = []
        while True:
            if len(stack) == 0:
                print('Main Menu of ~Neoneotakua~ Word Construction Program')
                lines = input().split(';')
                while len(lines) > 0:
                    try:
                        if len(lines[-1]) > 0:
                            stack.append(lines.pop(-1))
                        else:
                            lines.pop(-1)
                    except IndexError:
                        break
            try:
                l = stack.pop(-1).split(' ')
            except IndexError:
                l = ['']
            try:
                l.remove('')
            except ValueError:
                pass
            try:
                i = l[0]
            except IndexError:
                i = ''
            else:
                arg = l[1:]
            f = None
            if i == 'help': f = self.help_screen
            elif i == 'load': f = self.load_file
            elif i == 'create': f = self.construction_menu
            elif i == 'info': f = self.read_info
            elif i == 'edit': f = self.change_menu
            elif i == 'copy': f = self.copy_file
            elif i == 'save': f = self.save
            elif i == 'quit':
                print('Quitting...')
                self.save()
                break
            else:
                print('Could not comprehend \''+i+'\' enter \'help\' for help')
            if f != None:
                f(arg=arg)
            print()
        print('Exited.')
    def help_screen(self, arg=[]):
        print('--Help Screen--')
        print("""
            help - access help menu
            load - load another language object
            create - make words
            info - get various infobits about current settings
            edit - change current language object
            save - save current language object
            copy - saves current language object to another file
            quit - saves and quits ~neoneotakua~ word construction program (or leave lower level menus)
        """)
        if input('Would you like to know more? [y/n] ') == 'y':
            print("""
                While editting or viewing:
                vp - percentage that vowels are chosen
                cp - percentage that consonants are chosen for starting syllables
                np - percentages that consonants are chosen after another specific letter
                p - change total percentage (not recommended)
                ds - which consonants are slurred by default
                eds - where consonants that are slurred by default do not get slurred
                ens - where consonants that are not slurred by default do get slurred
                """)
            if input('Would you like to know more? [y/n] ') == 'y':
                print("""
                     Include arguments after the command:
                       load filename;
                     To edit multiple commands, separate by semicolon:
                       load filename; edit np XR 0.5;
                     Percentages are automatically adjusted when file is saved
                     """)
    def load_file(self, arg=[]):
        self.save()
        print('--Load File--')
        while True:
            if len(arg) == 0: filepath = input('Enter name (be very, very sure about this): ')
            else:
                filepath = arg[0]
                arg = []
            if filepath == 'quit':
                return False
            else:
                filepath += '.p'
            try:
                obj = pickle.load(open(filepath, 'rb'))
            except FileNotFoundError:
                print('Invalid filename.')
            else:
                self.object = obj
                self.unloaded = False
                break
        self.filepath = filepath
        print('--File',filepath,'loaded--')
    def construction_menu(self, arg=[]):
        print('--Construction Menu--')
        if self.unloaded:
            print('Nothing to construct - no object loaded')
        else:
            self.save()
            while True:
                try:
                    if len(arg) == 0:
                        x = int(input('How many words? '))
                    else:
                        x = int(arg[0])
                except ValueError:
                    if len(arg) == 0:
                        print('Not a number.')
                    else:
                        arg = []
                else:
                    break
            for i in range(x):
                print(self.object.gen())
        print('--'+str(x),'words constructed--')
    def read_info(self, arg=[]):
        print('--Reading info--')
        if self.unloaded:
            print('No info to read - no object loaded')
        else:
            print('Current location of language object: ',self.filepath)
            print('Vowel percentages (vp):')
            self.display(self.object.VOWELS)
            print('Consonant percentages (cp):')
            self.display(self.object.CONSONANTS)
            print('Next consonant percentages (np):')
            self.display(self.object.NEXTS)
            print('Default slurr letters (ds):')
            print(self.object.TYPE_I)
            print('Exceptions where default slurrs do not slurr (eds):')
            print(self.object.NOT_SLURRED)
            print('Exceptions where non-defaults do slurr (ens):')
            print(self.object.SLURRED)
        print('--Info of file',self.filepath,'read--')
    def change_menu(self, arg=[]):
        print('--Editting Menu--')
        if self.unloaded:
            print('Nothing to edit - no object loaded')
        else:
            self.unsaved = True
            while True:
                if len(arg) == 0:
                    command = input('Enter value to edit: ')
                else:
                    command = arg[0]
                have_inputs = len(arg) > 2
                if command == 'vp':
                    if have_inputs:
                        (vowel, percent) = arg[1:]
                    else:
                        line = input('Enter text (vowel percentage e.g. E 0.32): ')
                        (vowel, percent) = line.split(' ')
                    if vowel in self.object.VOWELS:
                        try:
                            self.object.VOWELS[vowel] = float(percent) # NOTE: whenever Menu() saves or constructs words, it calls fix_percentages() on self.object
                        except ValueError:
                            print('Second argument must be decimal')
                        else:
                            break
                    else:
                        print('First argument must be vowel')
                elif command == 'cp':
                    if have_inputs:
                        (consonant, percent) = arg[1:]
                    else:
                        line = input('Enter text (consonant percentage e.g. K 0.02): ')
                        (consonant, percent) = line.split(' ')
                    if consonant in self.object.CONSONANTS:
                        try:
                            self.object.CONSONANTS[consonant] = float(percent)
                        except ValueError:
                            print('Second argument must be decimal')
                        else:
                            break
                    else:
                        print('First argument must be consonant')
                elif command == 'np':
                    if have_inputs:
                        (pair, percent) = arg[1:]
                    else:
                        line = input('Enter text (pair percentage e.g. LK 0.08): ')
                        (pair, percent) = line.split(' ')
                    if len(pair) == 2 and pair[0] in self.object.ALPHA and pair[1] in self.object.CONSONANTS:
                        try:
                            self.object.NEXTS[pair[0]][pair[1]] = float(percent) # OK to mess around w/ %
                        except ValueError:
                            print('Second argument must be decimal')
                        else:
                            break
                    else:
                        print('First argument must be pair of letters (second can not be vowel)')
                elif command == 'p':
                    if have_inputs:
                        (letter, percent) = arg[1:]
                    else:
                        line = input('Enter text (letter percentage e.g. X 0.08): ')
                        (letter, percent) = line.split(' ')
                    
                elif command == 'ds':
                    if have_inputs:
                        (operation, letter) = arg[1:]
                    else:
                        line = input('Enter text ([add/del] value e.g. add L): ')
                        (operation, letter) = line.split(' ')
                    if letter in self.objects.CONSONANTS:
                        out = self.object.TYPE_I
                        if operation == 'add':
                            out.append(letter)
                            break
                        elif operation == 'del':
                            out.remove(letter)
                            break
                        else:
                            print('Could not recognize operation\'',operation+'\'')
                    else:
                        print('Can only add consonants')
                elif command == 'eds':
                    if have_inputs:
                        (operation, pair) = arg[1:]
                    else:
                        line = input('Enter text ([add/del] value e.g. add LR): ')
                        (operation, pair) = line.split(' ')
                    if len(pair) == 2 and pair[0] in self.object.CONSONANTS and pair[1] in self.object.CONSONANTS:
                        out = self.object.NOT_SLURRED
                        if operation == 'add':
                            out.append(pair)
                            break
                        elif operation == 'del':
                            out.remove(pair)
                            break
                        else:
                            print('Could not recognize operation\'',operation+'\'')
                    else:
                        print('Argument must be consonant pair')
                elif command == 'ens':
                    if have_inputs:
                        (operation, pair) = arg[1:]
                    else:
                        line = input('Enter text ([add/del] value e.g. del VS): ')
                        (operation, pair) = line.split(' ')
                    if len(pair) == 2 and pair[0] in self.object.CONSONANTS and pair[1] in self.object.CONSONANTS:
                        out = self.object.SLURRED
                        if operation == 'add':
                            out.apppend(pair)
                            break
                        elif operation == 'del':
                            out.remove(pair)
                            break
                        else:
                            print('Could not recognize operation\'',operation+'\'')
                    else:
                        print('Argument must be consonant pair')
                else:
                    print('Did not recognize command:',command,'try one of these: vp, cp, np, p, ds, eds, ens')
        print('--Changes saved to local object--')
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
    def copy_file(self, arg=[]):
        print('--Copy File--')
        if self.unloaded:
            print('No file to copy - no object loaded')
        else:
            while True:
                if len(arg) == 0:
                    line = input('Enter name: ')
                else:
                    line = arg[0]
                if line == 'quit':
                    break
                else:
                    filename = line+'.p'
                    pickle.dump(self.object, open(filename, 'wb'))
                    break
        print('--File',filename,'copied from current location:',self.filepath+'--')
        self.load_file(arg=[line])
m = Menu(NNT1())
m.main_menu()
