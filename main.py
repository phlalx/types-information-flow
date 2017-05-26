#!/usr/local/bin/python3
"""main.

Typechecking non-interference.

Implementation of the type system defined in 
"On Flow-Sensitive Security Types" (S.Hunt and D.Sands):
"""

import os
import sys
import parser
import typing
import pretty_print
import free_vars

def _usage():
    print('usage: ./main.py file')
    exit(1)

def main():
    """ entry point to the interpreter.

    Check arguments and run the different steps.
    parsing, printing, free variables calculation and typechecking.
    """
    if len(sys.argv) != 2:
        _usage()

    filename = sys.argv[1]

    with open(filename, 'r') as myfile:
        input_program = myfile.read()

    print("--- parsing", filename)
    prog = parser.parser().parse(input_program)

    print("--- pretty print")
    pretty_print.print_prog(prog)

    print("--- free variable")
    fv = free_vars.free_vars_prog(prog)
    print(fv)

    print('--- typechecking')
    # we build the initial typing environment
    # Types are elements of the lattice of finie sets of variables
    # (see typing.py)
    # An environment is a dictionary that maps variable
    # to their types
    # Initial typing environnment maps each variable to the corresponding
    # singleton.
    # TODO(phil) define types in their own module
    gamma = dict([(x,set([x])) for x in fv])
    print('initial environment:', gamma)
    new_gamma = typing.typecheck(gamma, prog)
    print('final environment:', new_gamma)

if __name__ == "__main__":
    main()