#this is a list of translation temlates for different vm codes

END_INSTRUCTION_CHAR = "\n//next_instruction\n"
CURRENT_UTIL_JUMP_INDEX = 0 #used for stuff like logic labels

#NOTE: these are not at all the most efficient ways of doing things, also I could probably make it so some more work is done in the translator, such as with popping and pushing the pointers having the translator figure out the ram[offset+3] instead of it being handled by the assembler
class Dictionary:
    def __init__(self):
        self.util = Utils()
#PUSH:     
    def push(self, value, loc = "none", fileName = "Source"): #loc is the target location, aka like static local etc...
        loc = loc.lower() #make the push type lowercase
        
        if(loc == "none" or loc == "constant"):
            template = ("""
@%s
D=A
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "local"):
            template = ("""
@%s
D=A
@LCL
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "argument"):
            template = ("""
@%s
D=A
@ARG
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))
            
        elif(loc == "static"):
            template = ("""
@%s.%s
D=A
%s
A=M-1
M=D
""" % (fileName, value, self.util.IncStackPointer()))
            
        elif(loc == "pointer"):
            template = ("""
@3
D=A
@%s
A=D+A
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))

        elif(loc == "temp"):
            template = ("""
@5
D=A
@%s
A=D+A
D=M
%s
A=M-1
M=D
""" % (value, self.util.IncStackPointer()))

        return(self.util.fixWhitelines(template))

#POP:
    def pop(self, value, loc = "none", fileName = "Source"):
        loc = loc.lower()
        value = str(value)
        
        if(loc == "none" or loc == "constant"):
            template = ("""
%s
""" % (self.util.DecStackPointer()))
            
        elif(loc == "local"):
            template = ("""
%s
@%s
D=A
@LCL
A=M
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
""" % (self.util.DecStackPointer(), value))
            
        elif(loc == "argument"):
            template = ("""
%s
@%s
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
""" % (self.util.DecStackPointer(), value))
            
        elif(loc == "static"):
            template = ("""
%s
@%s.%s
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
""" % (self.util.DecStackPointer(), fileName, value))

        elif(loc == "pointer"):
            template = ("""
%s
@3
D=A
@%s
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
""" % (self.util.DecStackPointer(), value))

        elif(loc == "temp"):
            template = ("""
%s
@5
D=A
@%s
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
""" % (self.util.DecStackPointer(), value))

        return(self.util.fixWhitelines(template))

    def label(self, value):
        template = ("""
(%s)
""" % (value))

        return(self.util.fixWhitelines(template))

    def add(self):
        template = ("""
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M+D
M=D
%s
""" % (self.util.DecStackPointer()))
        return(self.util.fixWhitelines(template))

    def sub(self):
        template = ("""
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M-D
M=D
%s
""" % (self.util.DecStackPointer()))
        return(self.util.fixWhitelines(template))

    def negate(self):
        self.util.increaseJumpIndex()

        template = ("""
%s
@SP
A=M
D=M
D=-D
@SP
A=M
M=D
%s
""" % (self.util.DecStackPointer(), self.util.IncStackPointer()))

        return(self.util.fixWhitelines(template))

    def eq(self):
        self.util.increaseJumpIndex()
        #note: $lgl stands for logic jump label, the $ is because that it isn't allowed in vm language labels, so no one accientally overwrites it
        template = ("""
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$LJL%s
D;JEQ
@SP
A=M-1
M=0
@$LJL%s
0;JMP
($LJL%s)
@SP
A=M-1
M=-1
($LJL%s)
""" % (self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex(), self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex()))

        return(self.util.fixWhitelines(template))

    def greater_than(self):
        self.util.increaseJumpIndex()

        template = ("""
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$LJL%s
D;JGT
@SP
A=M-1
M=0
@$$LJL%s
0;JMP
($LJL%s)
@SP
A=M-1
M=-1
($LJL%s)
""" % (self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex(), self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex()))

        return(self.util.fixWhitelines(template))

    def less_than(self):
        self.util.increaseJumpIndex()

        template = ("""
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$LJL%s
D;JLT
@SP
A=M-1
M=0
@$LJL%s
0;JMP
($LJL%s)
@SP
A=M-1
M=-1
($LJL%s)
""" % (self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex(), self.util.getCurrentJumpIndex()-1, self.util.getCurrentJumpIndex()))

        return(self.util.fixWhitelines(template))
    
    def and_(self):

        template = ("""
%s
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=D&A
@SP
A=M
M=D
%s
""" % (self.util.DecStackPointer(), self.util.IncStackPointer()))

    def or_(self):
    
        template = ("""
%s
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=D|A
@SP
A=M
M=D
%s
""" % (self.util.DecStackPointer(), self.util.IncStackPointer()))
        
        return(self.util.fixWhitelines(template))

    def not_(self):
        
        template = ("""
%s
@SP
A=M
D=M
D=!D
@SP
A=M
M=D
%s
""" % (self.util.DecStackPointer(), self.util.IncStackPointer()))

        return(self.util.fixWhitelines(template))

    def jump(self, dest):
        
        template = ("""
@%s
0;JMP
""" % (dest))

        return(self.util.fixWhitelines(template))

    def jump_if(self, dest): #val is top of stack
        
        template = ("""
%s
@SP
A=M
D=M
@%s
D;JNE
""" % (self.util.IncStackPointer(), dest))

        return(self.util.fixWhitelines(template))

    def create_subroutine(self, subroutine_name, localVariables):
        template = ""

        #first, we need to declare the function start:
        template = template + ("""(%s)
""" % subroutine_name)
        #handle each local variable we want with a for loop:
        for i in range(localVariables): #we must initialize all these local variables to 0, aka push 0 that many times
            template = template + ("""@0
D=A
@SP
A=M
M=D
%s""" % self.util.IncStackPointer())

        return(self.util.fixWhitelines(template))

    def return_subroutine(self):

        #R1 = mem[1] which is local, we are then setting frame to this whichw e will use later
        #R14 = temporary var, we will put the return address in here. Frame - 5, which would be the return address/ We are using r13 for the computation of frame-5
        #We have to set things to how they were before so first we have to set the data at ARG(amount of arguments) to value pop returns
        #after this we restore all the other stuff such as SP(just arg+1), THAT(frame-1), THIS(frame-2), etc..
        #finally we jump to the return address that the caller provided
        template = ("""
@R1
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
M=M-1
@ARG
AD=M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
@R2
D=M
@R0
M=D+1
@R13
D=M
D=D-1
@R13
M=D
A=D
D=M
@R4
M=D
@R13
D=M
D=D-1
@R13
M=D
A=D
D=M
@R3
M=D
@R13
D=M
D=D-1
@R13
M=D
A=D
D=M
@R2
M=D
@R13
D=M
D=D-1
@R13
M=D
A=D
D=M
@R1
M=D
@R14
A=M
0;JMP
""")
        return(self.util.fixWhitelines(template))


    def call_subroutine(self, subroutine_name, args):
        self.util.increaseJumpIndex()
        template = ("""
@$SJL%s
D=A
@SP
A=M
M=D
@SP
M=M+1
@R1
D=M
@SP
A=M
M=D
@SP
M=M+1
@R2
D=M
@SP
A=M
M=D
@SP
M=M+1
@R3
D=M
@SP
A=M
M=D
@SP
M=M+1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1
@%s
D=A
@R0
A=M
AD=A-D
@R2
M=D
@R0
D=M
@R1
M=D
@%s
0;JMP
($SJL%s) """ % (self.util.getCurrentJumpIndex(), args+5, subroutine_name, self.util.getCurrentJumpIndex())) #The reason we do args+5 is because we are setting arg, remember ARG=SP-n-5, with n being number of args.(the subtraction from sp is handled by the assembler, but we are handling n and 5) SJL stands for subroutine jump label

        return(self.util.fixWhitelines(template))

#class of utils that will be used in many differnet vm code chunks
class Utils:
    def IncStackPointer(self):
        return("""@SP
M=M+1
""")

    def DecStackPointer(self):
        return("""@SP
M=M-1
""")

    def getCurrentJumpIndex(self):
        return(CURRENT_UTIL_JUMP_INDEX)

    def increaseJumpIndex(self):
        global CURRENT_UTIL_JUMP_INDEX
        CURRENT_UTIL_JUMP_INDEX += 1

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

