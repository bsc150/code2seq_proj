#!/usr/bin/env python

import angr
import sys

def write_binary(binary_path):
    project = angr.Project(binary_path, load_options={'auto_load_libs':False})
    cfg = project.analyses.CFG(fail_fast=True) # note: this is a fixed CFG, consider giving it as a parameter instead
    # return [(addr, func.name) for addr, func in cfg.kb.functions.items()]
    return [(hex(addr), func.name) for addr, func in cfg.kb.functions.items() if func.name == "main"]

def main():
    assert(len(sys.argv) > 1)
    return write_binary(sys.argv[1])

if __name__ == "__main__":
    with open("res_file", 'a') as f:
        for (addr, name) in main():
            f.write("file name: " + sys.argv[1] + "\n")
            f.write("\t" + addr + ", " + name + "\n")

