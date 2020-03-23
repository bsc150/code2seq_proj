# non block preprocess

from typing import Dict, Any

import angr
import os
import pickle
import re
import shutil
import sys

# change to match max_path_len as entered in config.py
N = 9

bases_dict = dict()
replacement_dict = dict()

adresses_dict = dict()

def address_breakfun(state):
    if state.inspect.address_concretization_result is None:
        return
    expr = state.inspect.address_concretization_expr
    if expr.depth == 1:
        if state.solver.eval(expr) in bases_dict:
            return
        # new var is declared
        var_name = f"var_{len(bases_dict)}"
        bases_dict[state.inspect.address_concretization_result[0]] = var_name
        replacement_dict[state.inspect.address_concretization_result[0]] = f"{var_name}(0)"
    else:
        # depth is 2 (either a new sym-var is being declared or offset calc)
        if expr.op != "__add__":
            return
        childs = list(expr.args)
#        assert len(childs) < 3
        if len(childs) == 1:
            if state.solver.eval(expr) in bases_dict:
                return
            # new var is declared
            var_name = f"var_{len(bases_dict)}"
            bases_dict[state.inspect.address_concretization_result[0]] = var_name
            replacement_dict[state.inspect.address_concretization_result[0]] = f"{var_name}(0)"
        if len(childs) == 2:
            base = None
            offset = None
            for c in childs:
                if not c.concrete:
                    base = state.solver.eval(c)
                else:
                    offset = state.solver.eval(c)
            if base not in bases_dict:
                return
            replacement_dict[state.inspect.address_concretization_result[0]] = f"{bases_dict[base]}({offset})"


def is_qualified(symbol):
    avoid = {'main', 'usage'}
    return symbol.is_function and symbol.is_export and not (symbol.name.startswith("_") or symbol.name in avoid)


def get_functions(proj):
    funcs = []
    for symb in proj.loader.main_object.symbols:
        if is_qualified(symb):
            funcs.append(symb)
    return funcs


def analyze_func(proj, fun, cfg):
    print(f"started running {fun.name}")
    call_state = proj.factory.call_state(fun.rebased_addr)
    call_state.inspect.b('address_concretization', when=angr.BP_AFTER, action=address_breakfun)
    sm = proj.factory.simulation_manager(call_state)
    sm.use_technique(angr.exploration_techniques.LoopSeer(cfg=cfg, bound=2))
    sm.run()
    return sm.deadended


def cons_to_triple(constraint):
    print("Constraint: ",constraint)
    if constraint.concrete:
        return ""
    args = list(filter(None, map(str, constraint.args)))
    triple = [constraint.op] + args
    print("Triple: ",triple)
    return "".join(triple).replace(" ", "")


def relify(conts):
    for k, v in replacement_dict.items():
        conts = re.sub(f"(0x|mem_){format(k, 'x')}[_0-9]*", v, conts)
    return conts.replace('{UNINITIALIZED}', '')


def train_input(binary):
    proj = angr.Project(binary, auto_load_libs=False)
    cfg = proj.analyses.CFGFast()
    funcs = get_functions(proj)
    output_name = binary + ".txt"
    with open(output_name, "w") as f:
        for test_func in funcs:
            bases_dict.clear()
            replacement_dict.clear()
            exec_paths = analyze_func(proj, test_func, cfg)
            if len(exec_paths) == 0:
                continue
            for exec_path in exec_paths:
                blocks = [proj.factory.block(baddr) for baddr in exec_path.history.bbl_addrs]
                print(len(blocks))
                processed_consts = "|".join(list(filter(None, map(cons_to_triple, exec_path.solver.constraints[:N]))))
                relified_consts = relify(processed_consts)
                f.write(f"{test_func.name} _,{relified_consts},_\n")


if __name__ == "__main__":
    binary = sys.argv[1]
    train_input(binary)
