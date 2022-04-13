# This is my code
# anyway this is the python
# version of ghost lul
# code is very fun (sometimes...)
# Programmer: MarcoDXV (MarcoDxv)
# Language: Python (CPython)

import re
import sys
import enum
import string

import subprocess

# Global variables
data_pos = 1
tkn_count = int()

Macros = dict()
Const = dict()
Var = dict()

# TODO: Should I add argc and argv
# TODO: Adding Macros :D
# NOTE: Cool Thing

# Keywords
class Keywords(enum.Enum):
  K_SYSCALL1 = enum.auto()
  K_SYSCALL3 = enum.auto()

  K_IF      = enum.auto()
  K_WHILE   = enum.auto()
  K_MACRO   = enum.auto()
  K_LESS    = enum.auto()
  K_GREATER = enum.auto()
  K_EQUALS  = enum.auto()
  K_IN      = enum.auto()

  K_VAR   = enum.auto()
  K_CONST = enum.auto()

  K_INT = enum.auto()
  K_ADD = enum.auto()
  K_SUB = enum.auto()

  K_SYMB_EQUALS   = enum.auto()
  K_SYMB_COMMENTS = enum.auto()
  K_SYMB_DOT      = enum.auto()

  K_TRUE  = enum.auto()
  K_FALSE = enum.auto()

  K_END = enum.auto()

# Types
class Types(enum.Enum):
  T_INT  = enum.auto()
  T_NAME = enum.auto()
  T_BOOL = enum.auto()
  T_STR  = enum.auto()

# Lexer Functions
def check_word_from_file(word):
  if word == "syscall1": return Keywords.K_SYSCALL1
  elif word == "syscall3": return Keywords.K_SYSCALL3

  elif word == "if": return Keywords.K_IF
  elif word == "while": return Keywords.K_WHILE
  elif word == "macro": return Keywords.K_MACRO
  elif word == "less": return Keywords.K_LESS
  elif word == "greater": return Keywords.K_GREATER
  elif word == "equals": return Keywords.K_EQUALS
  elif word == "in": return Keywords.K_IN

  elif word == "true": return Keywords.K_TRUE
  elif word == "false": return Keywords.K_FALSE

  elif word == "var": return Keywords.K_VAR
  elif word == "const": return Keywords.K_CONST

  elif word == "int": return Keywords.K_INT
  elif word == "add": return Keywords.K_ADD
  elif word == "sub": return Keywords.K_SUB

  elif word == "=": return Keywords.K_SYMB_EQUALS
  elif word == "//": return Keywords.K_SYMB_COMMENTS

  elif word == "end": return Keywords.K_END

  elif re.match("[0-9]+", word): return Types.T_INT
  elif re.match("[\S]+", word): return Types.T_NAME
  else: return word

def create_lex_from_file(code):
  print("[DEBUG] Lexing the Program to Tokens...")
  
  token_row = int(1)
  token_col = int()
  
  n_code = str()

  tokens = list()
  _tid = str()
  tmp = list()

  tmp_code = code.readlines()
  for i in tmp_code: n_code += i[:i.find("//")]

  for word in n_code:
    if word in [" ", "\t", "\n", ".", ";"] and _tid != "string":
      if word == "\n": token_row = token_row + 1; token_col = 0
      elif word == ";":
        print("<No Way> Are you really trying to put a \";\" ???");
        exit(1)
      
      # TODO: put keyword in lowercase for checks
      keyword = check_word_from_file("".join(tmp))
      
      if keyword in list(Keywords):
        if keyword == Keywords.K_SYSCALL1:
          tokens.append([Keywords.K_SYSCALL1.name, "".join(tmp)]); tmp = []
        
        elif keyword == Keywords.K_SYSCALL3:
          tokens.append([Keywords.K_SYSCALL3.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_IF:
          tokens.append([Keywords.K_IF.name, "".join(tmp)]); tmp = []
      
        elif keyword == Keywords.K_WHILE:
          tokens.append([Keywords.K_WHILE.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_MACRO:
          tokens.append([Keywords.K_MACRO.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_LESS:
          tokens.append([Keywords.K_LESS.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_GREATER:
          tokens.append([Keywords.K_GREATER.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_EQUALS:
          tokens.append([Keywords.K_EQUALS.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_IN:
          tokens.append([Keywords.K_IN.name, "".join(tmp)]); tmp = []
        
        elif keyword == Keywords.K_TRUE:
          tokens.append([Keywords.K_TRUE.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_FALSE:
          tokens.append([Keywords.K_FALSE.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_END:
          tokens.append([Keywords.K_END.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_VAR:
          tokens.append([Keywords.K_VAR.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_CONST:
          tokens.append([Keywords.K_CONST.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_INT:
          tokens.append([Keywords.K_INT.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_ADD:
          tokens.append([Keywords.K_ADD.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_SUB:
          tokens.append([Keywords.K_SUB.name, "".join(tmp)]); tmp = []

        elif keyword == Keywords.K_SYMB_EQUALS:
          tokens.append([Keywords.K_SYMB_EQUALS.name, "".join(tmp)]); tmp = []

      elif keyword in list(Types):
        if keyword == Types.T_INT:
          tokens.append([Types.T_INT.name, "".join(tmp)]); tmp = []

        elif keyword == Types.T_NAME:
          tokens.append([Types.T_NAME.name, "".join(tmp)]); tmp = []

      # if word == ".": tokens.append([Keywords.K_SYMB_DOT.name, word]); tmp = []

    elif word == "\"" and _tid == "":
      _tid = "string"; tmp = []

    elif word == "\"" and _tid == "string":
      tokens.append([Types.T_STR.name, "".join(tmp)])
      _tid = ""; tmp = []

    else:
      token_col = token_col + 1
      tmp.append(word)
  
  print("[DEBUG] Program Succesfully Lexed to Tokens\n")
  return tokens

# Parser

# NOTE: Better Errors Messages
def parse_syscall1(tree, tokens, tkn_count):
  parent = tokens[tkn_count]
  child1 = tokens[tkn_count - 1]    
  child2 = tokens[tkn_count - 2]
  
  tree.append([parent, child1, child2])

def parse_syscall3(tree, tokens, tkn_count):
  parent = tokens[tkn_count]
  child1 = tokens[tkn_count - 1]
  child2 = tokens[tkn_count - 2]
  child3 = tokens[tkn_count - 3]
  child4 = tokens[tkn_count - 4]
  
  tree.append([parent, child1, child2, child3, child4])

def parse_add(tree, tokens, tkn_count):
  parent = tokens[tkn_count]
  child1 = tokens[tkn_count - 1]
  child2 = tokens[tkn_count + 1]
  
  tree.append([parent, child1, child2])

def parse_sub(tree, tokens, tkn_count):
  parent = tokens[tkn_count]
  child1 = tokens[tkn_count - 1]
  child2 = tokens[tkn_count + 1]
  
  tree.append([parent, child1, child2])

def parse_var(tree, tokens):
  global tkn_count

  parent = tokens[tkn_count] # var
  child1 = tokens[tkn_count - 1] # name
  child2 = tokens[tkn_count + 2] # value

  if tokens[tkn_count + 1][1] != "=": print("Error: Should be an \"=\""); exit(1)

  tree.append([parent, child1, child2])

def parse_const(tree, tokens):
  global tkn_count

  parent = tokens[tkn_count] # const
  child1 = tokens[tkn_count - 1] # name
  child2 = tokens[tkn_count + 2] # value

  if tokens[tkn_count + 1][1] != "=": print("Error: Should be an \"=\""); exit(1)

  tree.append([parent, child1, child2])

# NOTE: Why make functions that makes the same things ???
# NOTE: (add and sub, if and while...)

def parse_if(tree, tokens):
  global tkn_count

  # TODO: Check if argument is true or false

  parent = tokens[tkn_count]
  child1 = tokens[tkn_count + 1]
  child2 = tokens[tkn_count + 2]
  child3 = tokens[tkn_count + 3]
  child4 = list()

  rtokens = int(0)

  while tokens[tkn_count][0] != Keywords.K_IN.name: tkn_count += 1; rtokens += 1
  if rtokens != 4: print("No Way !!!"); exit(1)
      
  tkn_count += 1
  while (tokens[tkn_count][0] != Keywords.K_END.name and
         tokens[tkn_count][0] != Keywords.K_IF.name):
        
    if tokens[tkn_count][0] == Keywords.K_SYSCALL3.name:
      parse_syscall3(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_SYSCALL1.name:
      parse_syscall1(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_ADD.name:
      parse_add(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_SUB.name:
      parse_sub(child4, tokens, tkn_count)

    tkn_count += 1

  tree.append([parent, child1, child2, child3, child4])

def parse_macro(tree, tokens):
  global tkn_count
  global Macros

  # TODO: Check all arguments not just if one

  parent = tokens[tkn_count] # macro
  child1 = tokens[tkn_count + 2] # name
  child2 = tokens[tkn_count + 1] # argument
  child4 = list() # body
  
  if child1[0] != Types.T_NAME.name: print("macro name should be a name not %s" % child1[0]); exit(1)
  elif child2[0] != Types.T_NAME.name: print("arguments of macros are name not %s" % child2[0]); exit(1)

  tkn_count += 1
  while (tokens[tkn_count][0] != Keywords.K_END.name and
         tokens[tkn_count][0] != Keywords.K_MACRO.name):
        
    if tokens[tkn_count][0] == Keywords.K_SYSCALL3.name:
      parse_syscall3(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_SYSCALL1.name:
      parse_syscall1(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_ADD.name:
      parse_add(child4, tokens, tkn_count)

    elif tokens[tkn_count][0] == Keywords.K_SUB.name:
      parse_sub(child4, tokens, tkn_count)

    tkn_count += 1

  tree.append([parent, child1, child2, child4])
  Macros[child1[1]] = child1[1]

def create_parse_from_lex(tokens):
  print("[DEBUG] Parse the Tokens to AST...")

  global tkn_count
  global Macros

  ast = list()

  while tkn_count != len(tokens):
    if tokens[tkn_count][0] == Keywords.K_SYSCALL1.name:
      parse_syscall1(ast, tokens, tkn_count)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_SYSCALL3.name:
      parse_syscall3(ast, tokens, tkn_count)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_ADD.name:
      parse_add(ast, tokens, tkn_count)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_SUB.name:
      parse_sub(ast, tokens, tkn_count)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_VAR.name:
      parse_var(ast, tokens)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_CONST.name:
      parse_const(ast, tokens)
      ###############################

    elif tokens[tkn_count][0] == Keywords.K_MACRO.name:
      parse_macro(ast, tokens)
      ###############################

    elif tokens[tkn_count][1] in Macros:
      ast.append([tokens[tkn_count]])

    elif tokens[tkn_count][0] == Keywords.K_WHILE.name:
      parent = tokens[tkn_count]
      child1 = tokens[tkn_count + 1]
      child2 = tokens[tkn_count + 2]
      child3 = tokens[tkn_count + 3]
      child4 = list()

      rtokens = int(0)

      while tokens[tkn_count][0] != Keywords.K_IN.name: tkn_count += 1; rtokens += 1
      if rtokens != 4: print("No Enough Argument for While Loop"); exit(1)

      tkn_count += 1
      while (tokens[tkn_count][0]!= Keywords.K_END.name and
             tokens[tkn_count][0] != Keywords.K_WHILE.name):
        
        if tokens[tkn_count][0] == Keywords.K_SYSCALL3.name:
          parenta = tokens[tkn_count]
          child1a = tokens[tkn_count - 1]
          child2a = tokens[tkn_count - 2]
          child3a = tokens[tkn_count - 3]
          child4a = tokens[tkn_count - 4]
      
          child4.append([parenta, child1a, child2a, child3a, child4a])

        tkn_count += 1      
    
      ast.append([parent, child1, child2, child3, child4])
      ###############################
    
    elif tokens[tkn_count][0] == Keywords.K_IF.name:
      parse_if(ast, tokens)
      ###############################

    tkn_count += 1

  print("[DEBUG] Tokens Succesfully Parsed to AST\n")
  return ast


def asm_syscall3(parser, asm_lines):
  global data_pos

  asm_lines.append("    ; --- syscall 3 ---\n")

  if parser[3][0] == Types.T_STR.name:
    asm_lines.insert(data_pos, "    LC%d db \"%s\", 0x0A, 0x00\n" % (data_pos, parser[3][1]))

    asm_lines.append("    mov rax, %s\n" % parser[1][1])
    asm_lines.append("    mov rdi, %s\n" % parser[2][1])
    asm_lines.append("    mov rsi, LC%d\n" % data_pos)
    asm_lines.append("    mov rdx, %s\n" % parser[4][1])
    asm_lines.append("    syscall\n")
    data_pos += 1

  elif parser[3][0] == Types.T_NAME.name:
    if parser[3][1] in Var:
      asm_lines.append("    lea rcx, %s\n" % Var[parser[3][1]])
      
      asm_lines.append("    mov rax, %s\n" % parser[1][1])
      asm_lines.append("    mov rdi, %s\n" % parser[2][1])
      asm_lines.append("    mov rsi, rcx\n")
      asm_lines.append("    mov rdx, %s\n" % parser[4][1])
      asm_lines.append("    syscall\n")

    elif parser[3][1] in Const:
      asm_lines.append("    lea rcx, %s\n" % Const[parser[3][1]])

      asm_lines.append("    mov rax, %s\n" % parser[1][1])
      asm_lines.append("    mov rdi, %s\n" % parser[2][1])
      asm_lines.append("    mov rsi, rcx\n")
      asm_lines.append("    mov rdx, %s\n" % parser[4][1])
      asm_lines.append("    syscall\n")
    
    elif parser[3][1] == "mem":
      asm_lines.append("    mov rax, %s\n" % parser[1][1])
      asm_lines.append("    mov rdi, %s\n" % parser[2][1])
      asm_lines.append("    mov rsi, mem\n")
      asm_lines.append("    mov rdx, %s\n" % parser[4][1])
      asm_lines.append("    syscall\n")

    else:
      print("ERROR: Undefined Name: \"%s\"" % parser[3][1])
      exit(1)
    
  elif parser[3][0] == Types.T_INT.name:
    print("It is a integer !!!")

  asm_lines.append("\n")

def asm_syscall1(parser, asm_lines):
  asm_lines.append("    ; --- syscall 1 ---\n")
  asm_lines.append("    mov rax, %s\n" % parser[1][1])
  asm_lines.append("    mov rdi, %s\n" % parser[2][1])
  asm_lines.append("    syscall\n")
  asm_lines.append("\n")

def asm_add(parser, asm_lines, Var, Const):
  asm_lines.append("    ; --- add ---\n")
  # Arg 1
  if parser[1][0] == Types.T_NAME.name:
    if parser[1][1] in Var: asm_lines.append("    mov rax, %s\n" % Var[parser[1][1]])
    elif parser[1][1] in Const: asm_lines.append("    mov rax, %s\n" % Const[parser[1][1]])
    else: print("Undefined name: \"%s\"" % parser[1][1]); exit(1)

  if parser[2][0] == Types.T_NAME.name:
    if parser[2][1] in Var: asm_lines.append("    mov rbx, %s\n" % Var[parser[2][1]])
    elif parser[2][1] in Const: asm_lines.append("    mov rbx, %s\n" % Const[parser[2][1]])
    else: print("Undefined name: \"%s\"" % parser[2][1]); exit(1)
  
  if parser[1][0] == Types.T_INT.name: asm_lines.append("    mov rax, %s\n" % parser[1][1])
  if parser[2][0] == Types.T_INT.name: asm_lines.append("    mov rbx, %s\n" % parser[2][1])

  asm_lines.append("    add rax, rbx\n")
  if parser[1][0] == Types.T_NAME.name:
    if parser[1][1] in Var: asm_lines.append("    mov %s, rax\n" % Var[parser[1][1]])
    elif parser[1][1] in Const: asm_lines.append("    mov %s, rax\n" % Const[parser[1][1]])
  
  else: asm_lines.append("    mov [mem], rax\n")

  # TODO: Check Size of the variables arguments
  # TODO: Store the value in the memory buffer
  asm_lines.append("\n")

def asm_sub(parser, asm_lines, Var):
  asm_lines.append("    ; --- sub ---\n")
  asm_lines.append("    sub byte %s, %s\n" % (Var[parser[1][1]], parser[2][1]))
  # TODO: Check Size of the variables arguments
  # TODO: Check if the two arguments are variable if not:
  # TODO: Store the value in the memory buffer
  asm_lines.append("\n")

def asm_while(parser, asm_lines):
  asm_lines.append("    ; --- while loop ---\n")
  asm_lines.append("    LW:")
        
  for i in parser[4]:
    if i[0][0] == Keywords.K_SYSCALL3.name:
      # print("[DEBUG] New Syscall3")
        asm_syscall3(i, asm_lines)

  asm_lines.append("    mov rax, %s\n" % parser[1][1])
  asm_lines.append("    mov rbx, %s\n" % parser[3][1])
  asm_lines.append("    cmp rax, rbx\n")

  # TODO: Check Variables

  if parser[2][0] == Keywords.K_LESS.name: asm_lines.append("    jl LW\n")
  elif parser[2][0] == Keywords.K_GREATER.name: asm_lines.append("    jg LW\n")
  elif parser[2][0] == Keywords.K_EQUALS.name: asm_lines.append("    je LW\n")
  asm_lines.append("\n")

def asm_var(parser, asm_lines, var_count):
  asm_lines.append("    ; --- var ---\n")
  asm_lines.append("    mov byte [rsp-%d], %s\n" % (var_count, parser[2][1]))
  asm_lines.append("\n")

def asm_const(parser, asm_lines, var_count):
  asm_lines.append("    ; --- const ---\n")
  asm_lines.append("    mov byte [rsp-%d], %s\n" % (var_count, parser[2][1]))
  asm_lines.append("\n")

def asm_if_cond(parser, asm_lines, if_cond, Var):
  asm_lines.append("    ; --- if condition ---\n")
  if parser[1][1] in Var: asm_lines.append("    mov rax, %s\n" % Var[parser[1][1]])
  else: asm_lines.append("    mov rax, %s\n" % parser[1][1])
  
  if parser[3][1] in Var: asm_lines.append("    mov rbx, %s\n" % Var[parser[3][1]])
  else: asm_lines.append("    mov rbx, %s\n" % parser[3][1])

  asm_lines.append("    cmp rax, rbx\n")

  if parser[2][0] == Keywords.K_LESS.name: asm_lines.append("    jl LD%d\n" % if_cond)
  elif parser[2][0] == Keywords.K_GREATER.name: asm_lines.append("    jg LD%d\n" % if_cond)
  elif parser[2][0] == Keywords.K_EQUALS.name: asm_lines.append("    je LD%d\n" % if_cond)

  asm_lines.append("    jmp LE%d\n" % if_cond)

  # body
  asm_lines.append("    LD%d:\n" % if_cond)
        
  for i in parser[4]:
    if i[0][0] == Keywords.K_SYSCALL3.name: asm_syscall3(i, asm_lines)
    elif i[0][0] == Keywords.K_SYSCALL1.name: asm_syscall1(i, asm_lines)
    
    elif i[0][0] == Keywords.K_ADD.name: asm_add(i, asm_lines, Var)
    elif i[0][0] == Keywords.K_SUB.name: asm_sub(i, asm_lines, Var)

  # Not ...
  asm_lines.append("    LE%d:\n" % if_cond)
  asm_lines.append("\n")

def asm_macro(parser, asm_lines):
  asm_lines.append("    ; --- macro ---\n")
  asm_lines.append("    LM:\n")
  asm_lines.append("\n")

  for i in parser[3]:
    if i[0][0] == Keywords.K_SYSCALL3.name: asm_syscall3(i, asm_lines)
    elif i[0][0] == Keywords.K_SYSCALL1.name: asm_syscall1(i, asm_lines)
    
    elif i[0][0] == Keywords.K_ADD.name: asm_add(i, asm_lines, Var)
    elif i[0][0] == Keywords.K_SUB.name: asm_sub(i, asm_lines, Var)
  asm_lines.append("\n")

  # TODO: Finish Macros

def asm_jump_macro(asm_lines, Macros):
  asm_lines.append("    ; --- macro jump ---\n")
  asm_lines.append("    jmp LM\n")
  asm_lines.append("\n")

def generate_nasm_linux_x86_64_from_parser(parser):
  global data_pos

  global Const
  global Macros
  global Var

  var_count = int()
  mem_capacity = int(128)
  asm_lines = list()
  if_cond = int(0)

  print("[DEBUG] Generate Assembly From Parser...")
  
  asm_lines.append("section .data\n")
  asm_lines.append("\n")
  asm_lines.append("section .bss\n")
  asm_lines.append("    mem resb %d\n" % mem_capacity)
  asm_lines.append("\n")
  asm_lines.append("section .text\n")
  asm_lines.append("global _start\n")
  asm_lines.append("_start:\n")

  for i in range(len(parser)):
    if parser[i][0][0] == Keywords.K_SYSCALL1.name:
      asm_syscall1(parser[i], asm_lines)

    elif parser[i][0][0] == Keywords.K_SYSCALL3.name:
      asm_syscall3(parser[i], asm_lines)
    
    elif parser[i][0][0] == Keywords.K_ADD.name:
      asm_add(parser[i], asm_lines, Var, Const)

    elif parser[i][0][0] == Keywords.K_SUB.name:
      asm_sub(parser[i], asm_lines, Var)

    elif parser[i][0][0] == Keywords.K_WHILE.name:
      asm_while(parser[i], asm_lines)

    elif parser[i][0][0] == Keywords.K_MACRO.name:
      asm_macro(parser[i], asm_lines)
    
    elif parser[i][0][1] in Macros:
      asm_jump_macro(asm_lines, Macros)

    elif parser[i][0][0] == Keywords.K_IF.name:
      asm_if_cond(parser[i], asm_lines, if_cond, Var)
      if_cond += 1;
    
    elif parser[i][0][0] == Keywords.K_VAR.name:
      asm_var(parser[i], asm_lines, var_count)
      Var[parser[i][1][1]] = "[rsp-%d]" % var_count
      var_count += 1

    elif parser[i][0][0] == Keywords.K_CONST.name:
      asm_const(parser[i], asm_lines, var_count)  
      Const[parser[i][1][1]] = "[rsp-%d]" % var_count  
      var_count += 1 

  print("[DEBUG] Succesfully Generated Assembly From Parser\n")
  
  return asm_lines

def cmd_call_and_print(cmd = ""):
    print("[CMD] %s" % cmd)
    subprocess.call(cmd.split())

if "__main__" == __name__:
  # Arguments
  filein  = sys.argv[1]
  fileout = sys.argv[3]
  option  = sys.argv[4]
  flag = sys.argv[2]

  # Files
  inf = open(filein, "r")

  # Functions
  lex = create_lex_from_file(inf)
  print(lex)

  parse = create_parse_from_lex(lex)
  print(parse)

  asm_code = generate_nasm_linux_x86_64_from_parser(parse)
  
  # Outfile
  outf = open("%s.asm" % fileout, "w")
  for i in asm_code: outf.write(i)
  outf.close()

  # Assembly and Run
  print("[DEBUG] Running ./%s" % fileout)
  cmd_call_and_print("nasm -f elf64 -o %s.o %s.asm" % (fileout, fileout))
  cmd_call_and_print("ld %s.o -o %s" % (fileout, fileout))
  cmd_call_and_print("./%s\n" % fileout)
