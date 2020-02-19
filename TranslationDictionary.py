#this is a list of translation temlates for different vm codes
class Dictionary:
    def __init__(self):
        self.util = Utils()
        
    def push(self, value):
        template = ("""
@%d
D=A""" % (value))
        
        template = template + self.util.IncStackPointer()

        return(self.util.fixWhitelines(template))

#class of utils that will be used in many differnet vm code chunks
class Utils:
    def IncStackPointer(self):
        return("""
@SP
M=M+1
A=M-1
M=D""")

    def fixWhitelines(self, text):
        #removes any line with empty lines, https://stackoverflow.com/questions/3711856/how-to-remove-empty-lines-with-or-without-whitespace-in-python
        text = text.split("\n")
        for lineIndex in range(len(text)):
            if re.match(r'^\s*$', line):
                
                
        text = "".join(text)
        print(text)


d = Dictionary()
print(d.push(5))
