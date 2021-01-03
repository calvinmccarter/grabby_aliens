import numpy as np
import os
import sys
import multiprocessing
import subprocess

# for D=3 n=1             N=1e9 s=0.250  c=2.0 L=1.0


# L/s = 4
# for D=3 n=[1,2,5,10,20] N=1e5 s=1.000  c=1.0 L=1.0   -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e5 s=0.500  c=1.0 L=0.5   -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e5 s=0.250  c=1.0 L=0.25  -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e5 s=0.125  c=1.0 L=0.125 -> 10 simulations

# s/c = 8
# for D=3 n=[1,2,5,10,20] N=1e6 s=0.500  c=4.0 L=1.0 -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e6 s=0.250  c=2.0 L=1.0 -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e6 s=0.125  c=1.0 L=1.0 -> 10 simulations
# for D=3 n=[1,2,5,10,20] N=1e6 s=0.0625 c=0.5 L=1.0 -> 10 simulations

# for D=3 n=[1] N=1e6 (L,s)=[(1,1), (0.5,0.5) (0.25,0.25) (0.125,0.125)] c=1.0

# for D=3 n=1 N=8e6 (L,s)=[(2,1) (1.0, 0.5) (0.5, 0.25) (0.25, 0.125)]

D = 3
nlist = [1]
N = 2*(1/512)*1e6
#N = 6e6
#N = 2.7e7
c = 1.0

cmdlist = []
#for L, s in [(3.0, 1.0), (1.5, 0.5), (0.75, 0.25), (0.375, 0.125)]:
#for L, s in [(1.0, 1.0), (0.5, 0.5), (0.25, 0.25), (0.125, 0.125)]:
#for L, s in [(2.0, 1.0), (1, 0.5), (0.5, 0.25), (0.25, 0.125)]:
#for L, s in [(1.0, 1.0), (0.5, 0.5), (0.25, 0.25), (0.125, 0.125)]:
#for L, s in [(0.5, 1.0), (0.25, 0.5), (0.125, 0.25), (0.0625, 0.125)]:
#for L, s in [(0.25, 1.0), (0.125, 0.5), (0.0625, 0.25), (0.03125, 0.125)]:
#for L, s in [(1.0, 1.0), (0.5, 0.5), (0.25, 0.25), (0.125, 0.125)]:
    for n in nlist:
        NLsD = N / np.power(L/s, D)
        print(NLsD)
        for randix in range(10):
            fout = f"para/D={D}_n={float(n)}_N={N:.2e}_s={s:.5e}_L={float(L)}_c={float(c)}_r={randix}.csv"
            cmd = f"../simulate {D} {n} {N} {s} {c} {L} > {fout}"
            print(cmd)
            cmdlist.append(cmd)
#"""
max_processes = multiprocessing.cpu_count()
processes = set()
for cmd in cmdlist:
    #os.system(cmd)
    processes.add(subprocess.Popen([cmd], shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([
            p for p in processes if p.poll() is not None])
#"""
