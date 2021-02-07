import numpy as np
import os
import sys
import multiprocessing
import subprocess

D = 3
N = 1e8
true_nlist = [1.01, 1.1, 1.2, 1.5] + list(range(2, 21))
true_nlist = [1.5, 2, 4, 8, 12, 16, 20, 24]
true_nlist = [1.5, 3, 6]
print(true_nlist)
m = 0.90
nlist = [round(tnn/(1-m)-1, 6) for tnn in true_nlist]
print(nlist)
s = 1.0
#sclist = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.0]
#sclist = [0.01]
#sclist = [0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
sclist = [0.1, 0.5, 1.0]
L = 1
num_empty = 200

n_perms = 1
cmdlist = []
for n in nlist:
    for sc in sclist:
        c = s / sc
        for randix in range(n_perms):
            fout = f"nsc-setisaturday-numempty200/D={D}_n={float(n):.5f}_N={N:.2e}_s={s:.1f}_L={L:.1f}_c={c:.5e}_r={randix}"
            cmd = f"../a.out {D} {n} {N} {s} {c} {L} {fout} {randix} {num_empty}"
            print(cmd)
            cmdlist.append(cmd)
max_processes = min(multiprocessing.cpu_count(), 4)
processes = set()
for cmd in cmdlist:
    #os.system(cmd)
    processes.add(subprocess.Popen([cmd], shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([
            p for p in processes if p.poll() is not None])
