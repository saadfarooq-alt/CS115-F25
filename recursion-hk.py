#!/usr/bin/env python3

# Copyright 2020 Cameron Morland
# Modified 2025 by Sa'ad’s ChatGPT Assistant to detect nested recursion.

import sys

help = '''recursion-hk.py [-l] [filenames]
    Creates a report of files containing recursive Racket code, including:
    - top-level functions
    - local helper functions
    - nested defines
    - lambda-based recursive helpers
    or with [-l], list all global functions in the file.
'''

############################################################
# TOKENIZER (unchanged)
############################################################

def tokenize(filename, keepcomments=False):
    def keep_item(x):
        if not isinstance(x, str): return True
        elif x == '': return False
        elif keepcomments: return True
        elif x[0] == ';': return False
        else: return True

    def tokenize_raw(L, endchar=')'):
        def tokenize_string(L, endchar):
            R = []
            while L and L[-1] != endchar:
                R.append(L.pop())
            L.pop()
            return "".join(R)

        R = ['']
        while L:
            char = L.pop()
            if char == ';':       R.append(char + tokenize_string(L, endchar='\n'))
            elif char == '"':     R.append('"{}"'.format(tokenize_string(L, endchar='"')))
            elif char == endchar: break
            elif char == '(':
                R.append(tokenize_raw(L, endchar=')'))
            elif char == '[':
                R.append(tokenize_raw(L, endchar=']'))
            elif char == '\n':    pass
            elif char == ' ':     R.append('')
            else:                 R[-1] += char

        return list(filter(keep_item, R))

    with open(filename,'r') as f:
        L = [x for x in "".join(f.readlines()[3:])]
        L.reverse()
        return tokenize_raw(L)

############################################################
# NEW: extract all nested function definitions
############################################################

def gather_all_defines(expr, collected):
    """Recursively collect any form that looks like (define (f ...) body)."""
    if not isinstance(expr, list):
        return

    # Pattern: (define (f args...) body)
    if len(expr) == 3 and expr[0] == 'define' and isinstance(expr[1], list):
        collected.append(expr)

    # Keep searching inside lists
    for item in expr:
        if isinstance(item, list):
            gather_all_defines(item, collected)

############################################################
# Seek for a function name inside an expression (unchanged)
############################################################

def seek(target, expr):
    for item in expr:
        if item == target:
            return True
        if isinstance(item, list) and seek(target, item):
            return True
    return False

############################################################
# UPDATED: detect recursion including nested helpers
############################################################

def seek_recursion(filename):
    found = False

    # First tokenize into top-level expressions
    top = tokenize(filename)

    # Collect ALL defines (top-level + nested)
    all_defines = []
    for expr in top:
        gather_all_defines(expr, all_defines)

    # Check each define for recursion
    for L in all_defines:

        funcname = L[1][0]
        args = L[1][1:]
        body = L[2]

        # Ignore "accidentally shadowed" recursion
        if funcname not in args:
            if seek(funcname, body):
                if not found:
                    print(f"*** {filename} contains recursive functions:")
                found = True
                print(f"    {funcname}")

############################################################
# List global functions only (unchanged)
############################################################

def list_functions(filename):
    funclist = []
    for L in tokenize(filename):
        if len(L) == 3 and L[0] == 'define' and isinstance(L[1], list):
            funclist.append(L[1][0])

    funclist.sort()
    print(filename + ":\t", " ".join(funclist))
    return 0

############################################################
# MAIN
############################################################

if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    print(help)
    exit(0)

if len(sys.argv) > 1 and sys.argv[1] == '-l':
    for f in sys.argv[2:]:
        list_functions(f)
else:
    for f in sys.argv[1:]:
        seek_recursion(f)

