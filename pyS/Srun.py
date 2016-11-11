#!/usr/bin/env python3
import sys
import io
import getopt

from .S.language import SProgram
from .S.interp import StopProgram, SInterp

def usage():
    print("./Sdump [-h | -v] FILE")
    print()
    print("     -h, --help       Displays this message")
    print("     -v, --version    Displays the version of pyS")
    print()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)

    outfile = sys.stdout
    infile = sys.stdin

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-v", "--version"):
            printf("pyS {}".format(config.VERSION))
            sys.exit(0)

    if len(args) > 1:
        sys.stderr.write("Too many sources passed\n")

    if len(args) == 1:
        try:
            infile = open(args[0], 'r')
        except IOError as e:
            sys.stderr.write("Could not open file for read {} (error {}): {}\n".format(args[0], e.errno, e.strerror))
            sys.exit(e.errno)

    s_program = SProgram(int(infile.read()))
    interp = SInterp(s_program)
    while True:
        try:
            # print("{} : {} : {}".format(interp.pos(), interp.var_value(1), interp.var_value(2)))
            interp.step()
        except StopProgram:
            break
    print(interp.var_value(1))
    infile.close()
    outfile.close()
