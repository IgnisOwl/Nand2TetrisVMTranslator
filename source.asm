(why)
//next instruction
@15
D=A
@SP
M=M+1
A=M-1
M=D
//next instruction
@5
D=A
@12
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//next instruction
@SP
M=M-1
@SP
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
//next instruction
@SP
M=M+1
@SP
A=M
D=M
@why
D;JNE
//next instruction
(END)
@END
0;JMP