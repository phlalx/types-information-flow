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
import typing_os
import pretty_print
import free_vars
import lat_types
import argparse

def main():
    """ entry point to the interpreter.

    Check arguments and run the different steps.
    parsing, printing, free variables calculation and typechecking.
    """
    arg_parser = argparse.ArgumentParser(description = 
        'Information-flow typechecker for a simple imperative language.')
    arg_parser.add_argument("file", metavar="FILE", help="file to be processed", 
      nargs=1)
    arg_parser.add_argument("-v", dest='verbose', action='store_true', 
      help='verbose mode. Print debug information')
    args = arg_parser.parse_args()
    verbose = args.verbose

    filename = args.file[0]

    # TODO(Phil) handle exception
    with open(filename, 'r') as myfile:
        input_program = myfile.read()

    if verbose:
        print("--- parsing", filename)

    prog = parser.parser().parse(input_program)
    fv = free_vars.free_vars_prog(prog)

    if verbose:
        print("--- pretty print")
        pretty_print.print_prog(prog)

    fv = free_vars.free_vars_prog(prog)
    ov = free_vars.output_vars_prog(prog)

    if verbose:
        print("--- free and output variable")
        print('free', fv)
        print('output', ov)

    gamma = lat_types.create_singleton_env(fv)

    print('--- typechecking (hunt-sand)')
    if ov:
        print('WARNING: output variables are ignored')
        
    print('* initial environment:', gamma)

    new_gamma = typing.typecheck(gamma, prog)
    print('* final environment:', new_gamma)

    print('--- typechecking (output-sensitive)')
    gamma = lat_types.create_singleton_env(fv)
    gamma.update(lat_types.create_complement_env(ov))
    alpha = lat_types.create_singleton_env(ov)
    print('* initial gamma', gamma) 
    print('* initial alpha', alpha) 
    V = set()
    Z = set()
    Xo = ov
    gamma, alpha, V, Z  = typing_os.typecheck(gamma, alpha, V, Z, Xo, prog)
    print('* final gamma:', gamma)
    print('* final alpha:', alpha)
    print('* final V:', V)
    print('* final Z:', Z)
    has_return_var = prog[2]
    if not has_return_var: 
        print('--- sanity check: if no leaked variables, gammas should coincide')
        ok = gamma == new_gamma
        print("OK" if ok else "Not OK")


if __name__ == "__main__":
    main()
