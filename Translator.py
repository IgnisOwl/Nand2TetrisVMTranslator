#VM Translator

import TranslationDictionary

sourceFile = "source.vm"

class Parser:
    def type(self, line):
        return("push", None)

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

        print(vals)
    
class Translator:
    def __init__(self):
        self.dictionary = TranslationDictionary.Dictionary()
        self.parser = Parser()
        
     
    def translate(self, source):
        translated = ""
        newLine = "\n"
    
        for line in source:
            vals = ["none", "Source"] #default values

            if(self.parser.type(line)[0] == "push"):
                if(self.parser.type(line)[1] != None):
                    vals[0] = (self.parser.values(line)[0])
                else:
                    vals[0] = (self.parser.values(line)[0])
                
                translated = translated + self.dictionary.push(vals[0])

        return(translated)
    

               
source = open(sourceFile, "r").readlines()
translator = Translator()
print(translator.translate(source))
