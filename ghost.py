# This is my code
# this is the python
# version of ghost lul inspirated by Forth... :\
# What not Forth but Porth ??? Anyway
# code is very fun (sometimes...)
# Programmer: MarcoDXV (MarcoDxv)
# Language: Python (CPython)

import re
import sys
import enum
import string

import subprocess
from dataclasses import dataclass

# Global variables
data_pos = 1
tkn_count = int()
parser = None

Macros = dict()

@dataclass
class Macro:
  name:   str
  tokens: list

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

  K_IMPORT = enum.auto()

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

  elif word == "import": return Keywords.K_IMPORT

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
  
  inMacro = bool()
  macroed = bool()
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
        # TODO: Optimize this code
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

        elif keyword == Keywords.K_IMPORT:
          tokens.append([Keywords.K_IMPORT.name, "".join(tmp)]); tmp = []

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

# Error 404:
# Parser not Found

# It was create_parser_from_lex
def check_lex_for_error(tokens):
  imp_dir = "./includes/"

  # TODO: Post on GitHub

  # TODO: If Import directory exists
  for tok in range(len(tokens)):
    if tokens[tok][0] == Keywords.K_IMPORT.name:
      try: open("%s%s" % (imp_dir, tokens[tok + 1][1]), "r")
      except: print("File \"%s\" not found" % tokens[tok + 1][1]); exit(1)

  pass

def generate_nasm_linux_x86_64_from_parser(parser):
  global data_pos

  global Const
  global Macros
  global Var

  var_count = int()
  mem_capacity = int(128)
  asm_lines = list()
  if_cond = int(0)

  curr_tkn = int()

  print("[DEBUG] Generate Assembly From Parser...")
  
  asm_lines.append("section .data\n")
  asm_lines.append("\n")
  asm_lines.append("section .bss\n")
  asm_lines.append("    mem resb %d\n" % mem_capacity)
  asm_lines.append("\n")
  asm_lines.append("section .text\n")
  asm_lines.append("global _start\n")
  asm_lines.append("_start:\n")

  while curr_tkn != len(parser):
    # Macro
    if parser[curr_tkn][1] in Macros:
      uwu = curr_tkn # uwu

      # I hate programming >:( GFEZRARGTER 6453REFZHgyjtrhez6Y245 fuck python T-T
      for o in Macros[parser[curr_tkn][1]]: # Fucking things I don't understand why I wasn't working
        parser.insert(uwu, o)
        uwu += 1; curr_tkn += 1

      len_ = len(Macros[parser[curr_tkn][1]]) # Get the len of the body of the macro

      parser.pop(curr_tkn)

      curr_tkn = curr_tkn - (len_ + 1) # Go Back some tokens
      # Does it work ?

    # Syscall1
    elif parser[curr_tkn][0] == Keywords.K_SYSCALL1.name:
      asm_lines.append("    ; --- syscall1 ---\n")
      
      asm_lines.append("    mov rax, %s\n" % parser[curr_tkn - 1][1])
      asm_lines.append("    mov rdi, %s\n" % parser[curr_tkn - 2][1])
      asm_lines.append("    syscall\n")
      asm_lines.append("\n")
    
    # Syscall3
    elif parser[curr_tkn][0] == Keywords.K_SYSCALL3.name:
      asm_lines.append("    ; --- syscall3 ---\n")
      
      asm_lines.append("    mov rax, %s\n" % parser[curr_tkn - 1][1])
      asm_lines.append("    mov rdi, %s\n" % parser[curr_tkn - 2][1])

      # Is RSI a String or not ?
      if parser[curr_tkn - 3][0] == Types.T_STR.name:
        asm_lines.insert(data_pos, "    LC%d db \"%s\", 0x0A, 0x00\n" % (data_pos, parser[curr_tkn - 3][1]))

        asm_lines.append("    mov rsi, LC%d\n" % data_pos)
        data_pos += 1

      else:
        asm_lines.append("    mov rsi, %s\n" % parser[curr_tkn - 3][1])

      asm_lines.append("    mov rdx, %s\n" % parser[curr_tkn - 4][1])
      asm_lines.append("    syscall\n")
      asm_lines.append("\n")

    # Macro again
    elif parser[curr_tkn][0] == Keywords.K_MACRO.name:
      macro   = Macro(parser[curr_tkn + 1][1], [])
      rtokens = int()

      while parser[curr_tkn][0] != Keywords.K_IN.name:
        rtokens += 1; curr_tkn += 1
    
      curr_tkn += 1
      while parser[curr_tkn][0] != Keywords.K_END.name:
        if parser[curr_tkn][1] == macro.name:
          print("Cannot make a recursion in a recursion in a recursion in a recursion..."); exit(1)
        else: macro.tokens.append(parser[curr_tkn])

        curr_tkn += 1
    
      Macros[macro.name] = macro.tokens
      print(Macros)

    # Import
    elif parser[curr_tkn][0] == Keywords.K_IMPORT.name:
      import_dir  = "./includes"
      import_file = import_dir + "/" + parser[curr_tkn + 1][1]

      print("Importing: \"%s/%s\"\n" % (import_dir, parser[curr_tkn + 1][1]))
      imp_lex = create_lex_from_file(open("%s" % (import_file), "r"))
      print("%s\n" % imp_lex)

      check_lex_for_error(imp_lex)

      imp_asm = generate_nasm_linux_x86_64_from_parser(imp_lex)
      print("%s\n" % imp_asm)

      print("%s.asm" % import_file[:import_file.find(".", 2)])

    curr_tkn += 1

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

  # Files
  inf = open(filein, "r")

  # Functions
  lex = create_lex_from_file(inf)
  print(lex)

  check_lex_for_error(lex)

  asm_code = generate_nasm_linux_x86_64_from_parser(lex)
  
  # Outfile
  outf = open("%s.asm" % fileout, "w")
  for i in asm_code: outf.write(i)
  outf.close()

  # Assembly and Run
  print("[DEBUG] Running ./%s" % fileout)
  cmd_call_and_print("nasm -f elf64 -o %s.o %s.asm" % (fileout, fileout))
  cmd_call_and_print("ld %s.o -o %s" % (fileout, fileout))
  cmd_call_and_print("./%s\n" % fileout)
