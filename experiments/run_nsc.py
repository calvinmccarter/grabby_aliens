import numpy as np
import os
import sys
import multiprocessing
import subprocess

D = 3
N = 1e7
nlist = [1, 4, 7, 10, 16, 22, 28, 37, 46, 49]
s = 1.0
sclist = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
L = 1.0
n_empty = 200

n_perms = 5
cmdlist = []
for n in nlist:
    for sc in sclist:
        c = s / sc
        for randix in range(n_perms):
            fout = f"nsc-monday/D={D}_n={float(n)}_N={N:.2e}_s={s:.1f}_L={L:.1f}_c={c:.5e}_r={randix}"
            cmd = f"../a.out {D} {n} {N} {s} {c} {L} {fout} {randix} {n_empty}"
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
