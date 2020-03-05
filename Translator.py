#VM Translator

import TranslationDictionary

sourceFile = "source"

#cmd constants(could use a dictionary as well)
PUSH = "push"
POP = "pop"
LABEL = "label"
ADD = "add"
SUB = "sub"
NEGATE = "neg"
#perhaps in the future have a better way to handle logical operations, like make them each sub types similar to how push has
EQ = "eq"
GREATER_THAN = "gt"
LESS_THAN = "lt"
#bitwise:
AND = "and"
OR = "or"
NOT = "not"

class Parser:
    def type(self, line):
        line = self.split(line)
        cmd = line[0].lower() #the command should always be lowercase, if it's not make it

        if(len(line) == 1):
            return(cmd, None)

        elif(len(line) == 2):
            return(cmd, None)

        elif(len(line) == 3):
            if(cmd == PUSH):
                pushT = line[1]
                return(cmd, pushT)

            elif(cmd == POP):
                popT = line[1]
                return(cmd, popT)

    def split(self, line): #splits a line based on whitespaces
        return(line.split())

    def resemblesInt(self, text):
        try:
            int(text)
            return(True)
        
        except Exception:
            return(False)
    
    def values(self, line):
        vals = []
        
        line = self.split(line)
        for chunk in line:
            if(self.resemblesInt(chunk)):
                vals.append(int(chunk))
            else:
                vals.append(chunk)

        return(vals)
    
class Translator:
    def __init__(self):
        self.dictionary = TranslationDictionary.Dictionary()
        self.parser = Parser()
        
     
    def translate(self, source):
        translated = ""
        newLine = "\n"
    
        for line in source:
            vals = [sourceFile, 0, None] #holds values Filename, target, subtype(for like pushing if its for example a static local etc)
            if(self.parser.type(line)[0] == PUSH):
                if(self.parser.type(line)[1] != None): #if like local static etc...
                    vals[1] = (self.parser.values(line)[2])
                    vals[2] = (self.parser.values(line)[1])

                    translated = translated + self.dictionary.push(vals[1], vals[2], vals[0])
                else: #if it just pushes to stack
                    vals[1] = (self.parser.values(line)[1])
                
                    translated = translated + self.dictionary.push(vals[1])

            elif(self.parser.type(line)[0] == POP):
                if(self.parser.type(line)[1] != None): #if like local static etc...
                    vals[1] = (self.parser.values(line)[2])
                    vals[2] = (self.parser.values(line)[1])

                    translated = translated + self.dictionary.pop(vals[1], vals[2], vals[0])
                else: #if it just pops directly to the target
                    vals[1] = (self.parser.values(line)[1])
                
                    translated = translated + self.dictionary.pop(vals[1])

            elif(self.parser.type(line)[0] == LABEL):
                #We know we just will have label then the value always
                vals[1] = (self.parser.values(line)[1])

                translated = translated + self.dictionary.label(vals[1])

            elif(self.parser.type(line)[0] == ADD):
                translated = translated + self.dictionary.add()
            
            elif(self.parser.type(line)[0] == SUB):
                translated = translated + self.dictionary.sub()

            elif(self.parser.type(line)[0] == NEGATE):
                translated = translated + self.dictionary.negate()

            elif(self.parser.type(line)[0] == EQ):
                translated = translated + self.dictionary.eq()

            elif(self.parser.type(line)[0] == GREATER_THAN):
                translated = translated + self.dictionary.greater_than()
                
            elif(self.parser.type(line)[0] == LESS_THAN):
                translated = translated + self.dictionary.less_than()

            elif(self.parser.type(line)[0] == AND):
                translated = translated + self.dictionary.and_()

            elif(self.parser.type(line)[0] == OR):
                translated = translated + self.dictionary.or_()

            elif(self.parser.type(line)[0] == NOT):
                translated = translated + self.dictionary.not_()



        return(translated + self.dictionary.util.programSuffix())
    
               
out = open(sourceFile+".asm", "w")
source = open(sourceFile+".vm", "r").readlines()
translator = Translator()
out.write(translator.translate(source))
out.close()