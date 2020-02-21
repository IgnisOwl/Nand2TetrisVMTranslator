#VM Translator

import TranslationDictionary

sourceFile = "source.vm"

class Parser:
    def type(self, line):
        return("push", None)
    
    def values(self, line):
        return(0)
    
class Translator:
    def __init__():
        self.dictionary = TranslationDictionary.Dictionary(this)
        self.parser = Paser(this)
        
     
    def translate(self, source):
        translated = ""
        newLine = "\n"
    
        for line in source:
            vals = ["none", "Source"] #default values
            
            if(self.parser.type(line)[0] == "push"):
                if(self.parser.type(line)[1] != None):
                    vals[0] = (self.parser.values(line)[0])
                
                
                translated = translated + dictionary.push(line, vals[0], vals[1])
    

               
source = open(sourceFile, "r").readlines()
print(dictionary.push(2))
