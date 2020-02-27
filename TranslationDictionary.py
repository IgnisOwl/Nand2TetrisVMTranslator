#this is a list of translation temlates for different vm codes
#register constants
R0 = SP = 0
R1 = LCL = 1
R2 = ARG = 2
R3 = THIS = PTR = 3
R4 = THAT = 4
R5 = TEMP = 5
R6 = 6
R7 = 7
R8 = 8
R9 = 9
R10 = 10
R11 = 11
R12 = 12
R13 = FRAME = 13
R14 = RET   = 14
R15 = COPY  = 15

END_INSTRUCTION_CHAR = "\n//next instruction\n"

class Dictionary:
    def __init__(self):
        self.util = Utils()
#PUSH:     
    def push(self, value, loc = "none", fileName = "Source"): #loc is the target location, aka like static local etc...
        loc = loc.lower() #make the push type lowercase
        
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

#POP:
    def pop(self, value, loc = "none", fileName = "Source"):
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

        #the suffic:
        newText = newText + END_INSTRUCTION_CHAR
        return(newText)

    def programSuffix(self):
        return("""(END)
@END
0;JMP""")


if(__name__ == "__main__"):
    d = Dictionary()
    print(d.push(2, "argument"))

