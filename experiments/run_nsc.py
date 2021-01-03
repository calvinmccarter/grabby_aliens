import numpy as np
import os
import sys
import multiprocessing
import subprocess

D = 3
N = 1e8
nlist = [0.5, 1, 2, 5, 10, 20]
c = 1.0
slist = [0.01, 0.1, 0.2, 0.5, 0.8, 0.9, 0.99]

n_perms = 1
cmdlist = []
for n in nlist:
    for s in slist:
        L = s
        for randix in range(n_perms):
            fout = f"nsc/D={D}_n={float(n)}_N={N:.2e}_s={s:.5e}_L={float(L)}_c={float(c)}_r={randix}.csv"
            cmd = f"../simulate {D} {n} {N} {s} {c} {L} > {fout}"
            print(cmd)
            cmdlist.append(cmd)
max_processes = multiprocessing.cpu_count()
processes = set()
for cmd in cmdlist:
    #os.system(cmd)
    processes.add(subprocess.Popen([cmd], shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([
            p for p in processes if p.poll() is not None])
