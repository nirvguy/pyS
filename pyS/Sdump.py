#!/usr/bin/env python3
import sys
import io
import getopt

import S.language

def usage():
    print("./Sdump [-h] [-o OUTPUT] FILE")
    print()
    print("     -h, --help       Displays this message")
    print("     -o  OUTPUT       Output file to S")
    print("     -v, --version    Displays the version of pyS")
    print()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvpo:", ["help", "version"])
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
        elif o == "-o":
            try:
                outfile = open(a, 'w')
            except IOError as e:
                sys.stderr.write("Could not open file for write {} (error {}): {}\n".format(a, e.errno, e.strerror))
                sys.exit(e.errno)
        else:
            sys.stderr.write("Unknown option {0}\n".format(o))

    if len(args) > 1:
        sys.stderr.write("Too many sources passed\n")

    if len(args) == 1:
        try:
            infile = open(args[0], 'r')
        except IOError as e:
            sys.stderr.write("Could not open file for read {} (error {}): {}\n".format(args[0], e.errno, e.strerror))
            sys.exit(e.errno)

    s_program = S.language.SProgram(int(infile.read()))
    outfile.write(str(s_program)+'\n')
    infile.close()
    outfile.close()
