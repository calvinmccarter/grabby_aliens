import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import argparse
import subprocess
import math

parser = argparse.ArgumentParser()
parser.add_argument('--D', type=int)
parser.add_argument('--n', type=float)
parser.add_argument('--N', type=int)
parser.add_argument('--s', type=float)
parser.add_argument('--c', type=float, default=1.0)
parser.add_argument('--L', type=float, default=1.0)

args = parser.parse_args()
D,n,N,s,c,L = args.D,args.n,args.N,1.0/args.s,args.c,args.L

fname = f'D={D}_n={n}_N={N:.2e}_s={s}'
subprocess.check_output(f'g++ -std=c++17 -O3 -Wall -Werror -Wextra -Wshadow -Wno-sign-compare simulate.cc && ./a.out {D} {n} {N} {1.0/s} {c} {L} > {fname}.csv', shell=True)

XYTW = []
XT = []
T = []
W = []
A = []
with open(f'{fname}.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        T.append(float(row['OriginTime']))
        W.append(float(row['MinWait']))
        A.append(float(row['MaxAngle']))
        XT.append((float(row['X']), float(row['OriginTime'])))
        if D>=2:
            XYTW.append((float(row['X']), float(row['Y']), float(row['OriginTime']), float(row['MinWait'])))

T50 = np.median(T)
TS = [x/T50 for x in T]
WS = [x/T50 for x in W]
AS = [x/T50 for x in A]

fig, p = plt.subplots(3)
fig.suptitle(f'D={D} n={n} N={N:.2e} s={s} |C|={len(TS)} |C|*s^D={len(TS)*s**D}')

p[0].plot(TS)
p[0].set_ylabel('OriginTime')
p[0].set_xlabel('Index')

p[1].plot(sorted(WS))
p[1].set_ylabel('MinWait')
p[1].set_xlabel('Index')

p[2].plot(sorted(AS))
p[2].set_ylabel('MaxAngle')
p[2].set_xlabel('Index')

plt.savefig(f'{fname}.png')
subprocess.check_output(f'cmd.exe /C start {fname}.png', shell=True)

assert False


if D == 1:
    XT = sorted(XT)
    meeting_points = []
    GCs_and_meeting_points = []
    for i in range(len(XT) - 1):
        x0, t0 = XT[i]
        x1, t1 = XT[i+1]
        x = ((s*(t1 - t0)) + (x0 + x1)) / 2
        t = t0 + (x - x0)*(1/s)
        GCs_and_meeting_points.append((x0, t0))
        GCs_and_meeting_points.append((x, t))
        meeting_points.append((x, t))
    GCs_and_meeting_points.append((XT[-1]))

    plt.suptitle(f'D={D} n={n} N={N:.2e} s={s} |C|={len(TS)} |C|/s^D={len(TS)/s**D}')
    plt.figure(figsize=(6, 2.5))
    ax = plt.subplot(1, 1, 1)

    xs = [x for x,t in XT]
    ts = [t for x,t in XT]
    plt.scatter(xs, ts, s=3.5, color='blue', label="GC origin")

    plt.plot(*zip(*GCs_and_meeting_points), linewidth=0.85, color='purple', label="GC expansion boundary")
    plt.xlabel("x", fontsize=11)
    plt.xticks(fontsize=9)
    plt.ylabel("t", fontsize=11)
    plt.yticks(fontsize=9)
    # plt.ylim(None, 0.47)

    plt.grid(True)
    ax.set_axisbelow(True)

    plt.legend(prop={'size': 7})

    plt.subplots_adjust(bottom=0.2)
    plt.savefig("1d-plot.png", dpi=400)
    subprocess.check_output(f'cmd.exe /C start 1d-plot.png', shell=True)

if D == 2:
    resolution = 250
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    for x,y,t,w in XYTW:
        h = np.linspace(0, w, resolution)
        theta = np.linspace(0, 2*np.pi, resolution)
        X = np.outer(s*np.cos(theta), h) + x
        Y = np.outer(s*np.sin(theta), h) + y
        Z = np.outer(np.ones(np.size(theta)), h) + t
        ax.plot_surface(X, Y, Z, color=matplotlib.cm.rainbow(np.random.rand()), alpha=0.4)
    ax.view_init(elev=-20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    plt.savefig("2d-plot.png", dpi=200)
    subprocess.check_output(f'cmd.exe /C start 2d-plot.png', shell=True)
