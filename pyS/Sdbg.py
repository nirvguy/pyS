#!/usr/bin/env python3
import sys
import io
import getopt
import re

from .S.language import SProgram
from .S.interp import StopProgram, SInterp
from . import config

def usage():
    print("./Sdump [-h | -v] FILE")
    print()
    print("     -h, --help       Displays this message")
    print("     -v, --version    Displays the version of pyS")
    print()

class Sdb:
    def __init__(self, filename, s_program):
        self._filename = filename
        self._interp = SInterp(s_program)
        self._breakpoints = set()
        self._display_vars = set()
        self._list_pos = 0
        self._is_running = False

    def step(self):
        try:
            self._interp.step()
            self._list_pos = self._interp.pos()
            self.display_current_line()
            self.display_vars()
        except StopProgram:
            self._is_running = False
            print("The program is no longer running")

    def _run_until_breakpoint(self):
        while True:
            try:
                self._interp.step()
                if self._interp.pos() in self._breakpoints:
                    self._list_pos = self._interp.pos()
                    self.display_current_line()
                    break
            except StopProgram:
                self._is_running = False
                print("Program finished")
                break
        self._list_pos = self._interp.pos()
        self.display_vars()

    def _load_program(self, args):
        self._interp.rewind(args)
        self._list_pos = 0
        self._is_running = True
        self._run_until_breakpoint()

    def add_breakpoint(self, lineno):
        self._breakpoints.add(lineno)

    def display_current_line(self):
        self.list_lines(self._list_pos, 1)

    def display_vars(self, local_var_nums = None, sep='\n'):
        if len(self._display_vars) == 0:
            return

        if local_var_nums is None:
            dvars = self._display_vars
        else:
            dvars = local_var_nums

        print(sep.join(("V_{} : {}".format(nvar,                         \
                                           self._interp.var_value(nvar)) \
                        for nvar in dvars)))

    def list_lines(self, line, n = config.LIST_LINES):
        try:
            for i, rt_inst in self._interp.list(line, n):
                print("{}{}. {}".format(" " if i != self._interp.pos() else "",
                                        i, rt_inst))
        except StopProgram:
            print("Line number {} out of range; "
                  "{} has {} lines".format(line,           \
                                           self._filename, \
                                           self._interp.lines()))

    def run(self):
        history = []
        while True:
            orig_command = input('(sdb) ').strip()

            if len(orig_command) == 0:
                orig_command = history[-1]
            else:
                history.append(orig_command)

            commands = orig_command.split(' ', 1)

            command = commands[0].strip()

            args = []
            if len(commands) > 1:
                args = commands[1].split(",")
                args = [arg.strip() for arg in args]

            if command in ('r', 'run'):
                self.cmd_run(args)
            elif command in ('c', 'continue'):
                self.cmd_continue(args)
            elif command in ('b', 'break'):
                self.cmd_break(args)
            elif command in ('s', 'steap'):
                self.cmd_step(args)
            elif command in ('l', 'list'):
                self.cmd_list(args)
            elif command in ('d', 'display'):
                self.cmd_display(args)
            elif command in ('q', 'quit'):
                self.cmd_quit(args)
            else:
                print("Error: command {} unknown".format(command))
                continue

    def cmd_run(self, args):
        if len(args) > 1:
            print("Invalid syntax error")
        if self._is_running:
            while True:
                print("The program is already started.")
                resp = input("Start it from the beginning? (y or n) ")
                if resp in ('n', 'no'):
                    print("Program not restarted.")
                    return
                elif resp in ('y', 'yes'):
                    break

        s_args = [] if len(args) == 0 else args[0].split(" ")
        in_params = {}
        for i, s_arg in enumerate(s_args):
            in_params[i+1] = int(s_arg)

        print("Starting program: {}".format(self._filename))
        self._load_program(in_params)

    def cmd_break(self, args):
        if len(args) != 1:
            print("Error: invalid breakpoint")
            return

        self.add_breakpoint(int(args[0]))

    def cmd_step(self, args):
        if len(args) != 0:
            print("Error: invalid step call")
            return

        self.step()

    def cmd_continue(self, args):
        if len(args) != 0:
            print("Error: invalid continue call")
            return

        self._run_until_breakpoint()

    def cmd_list(self, args):
        line = self._list_pos
        if len(args) > 1:
            print("Error: invalid list")
            return
        if len(args) == 2:
            line = int(args[0])

        self.list_lines(line, config.LIST_LINES)
        self._list_pos += min(config.LIST_LINES/2, self._interp.lines())

    def cmd_display(self, args):
        if len(args) == 0:
            self.display_vars()
        else:
            local_disp_vars = set()
            disp_vars = args
            exp_digits = re.compile("^V_\d+$")
            for var in disp_vars:
                var = var.strip()
                if not exp_digits.match(var):
                    print("{} is not a valid name."
                          "Valid variables are: V_[0-9]+".format(var))
                    return
                local_disp_vars.add(int(var[2:]))
                self._display_vars.add(int(var[2:]))

            self.display_vars(local_disp_vars, ', ')

    def cmd_quit(self, args):
        sys.exit(0)

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
        sys.stderr.write("Too many sources passed")

    filename = 'stdin'
    if len(args) == 1:
        try:
            filename = args[0]
            infile = open(filename, 'r')
        except IOError as e:
            sys.stderr.write("Could not open file for read {} (error {}): {}".format(args[0], e.errno, e.strerror))
            sys.exit(e.errno)

    s_program = SProgram(int(infile.read()))

    sdb = Sdb(filename, s_program)
    sdb.run()

    infile.close()
    outfile.close()
