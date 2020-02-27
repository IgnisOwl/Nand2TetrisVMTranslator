#this is a list of translation temlates for different vm codes
class Dictionary:
    def __init__(self):
        self.util = Utils()
        
    def push(self, value, loc = "none", fileName = "Source"): #loc is the target location, aka like static local etc...
        loc = loc.lower()
        
        if(loc == "none"):
            template = ("""
@%d
D=A
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "local"):
            template = ("""
@%d
D=A
@LCL
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "argument"):
            template = ("""
@%d
D=A
@ARG
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "static"):
            template = ("""
@%s.%d
D=A
%s
A=M-1
M=D
""" % (fileName, value, self.util.IncStackPointer()))

        return(self.util.fixWhitelines(template))

#class of utils that will be used in many differnet vm code chunks
class Utils:
    def IncStackPointer(self):
        return("""
@SP
M=M+1
""")

    def fixWhitelines(self, text):
        #removes any line with empty lines, would use regex but lazy
        text = text.split()
        newText = ""

        for line in text:
            newText = newText + line.strip() + "\n"
            
        newText = newText.strip() #remove the end space
        return(newText)


if(__name__ == "__main__"):
    d = Dictionary()
    print(d.push(2, "argument"))

