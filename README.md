There are two files: analyze.py and simulate.cc. You are intended to run analyze.py, which compiles and runs simulate.cc itself.

Inputs: analyze.py takes the following arguments<br>
--n The power in the origin-time power-law. You may pass a comma-separated list of values<br>
--N The number of potential civilizations.<br>
--c The speed of light. You may pass a comma-separated list of values.<br>
--s The speed of civilization expansion (default 1.0)<br>
--m The power in the universe expansion scale factor (default 2/3; see section "8 Cosmology")<br>
--D The dimensions of space. Should be 1,2 or 3 (default 3)<br>
--L The size of the universe (default 1.0)<br>
--seed A random seed (default 0)<br>
--empty_samples How precisely to estimate how full the universe is (default 0, meaning no estimate at all)<br>

Outputs: analyze.py will produce two output files, one ending in "civs.csv" and one ending in "years.csv".

The "civs" file contains the following columns, with one row per "surviving" civilization:<br>
- D columns (X,Y,Z) for the position in space<br>
- OriginTime: The model/conformal OriginTime<br>
- MinArrival: The model time when another civilization first arrives at our origin point<br>
- MinSee: The model time when we first see signals from another civilization<br>
- NumberSeen: The number of alien civilizations we see signals from at our origin time<br>
- MaxAngle: How much of the sky another civilization takes up in our sky at our origin time (section 10 H; between 0 and pi)<br>
- PctEmpty: An estimate of how much of the universe is empty at our origin time<br>

The "years" file contains the following columns, all in "clock" years:<br>
- OriginTime: Sampled distribution of civilization origin times<br>
- MinWait: Sampled distribution of how long civilizations will have to wait to meet another civilization<br>
- MinSETI: Sampled distribution of how long civilizations will have to wait to see signals from another civilization<br>

For example, you can use the following command to generate figure 13:
`
time python3 analyze.py --D 3 --n 4.5,8,15,35 --N 1e8 --c 1.0,0.75,0.5,0.25 --L 1 --s 1 --seed 0 --empty 100 --m 0.66666666666666666666666
`

`time python3 analyze.py --D 3 --n 5 --N 1e8 --c 1.25 --L 1 --s 1 --seed 0 --empty 100`

`python3 analyze.py --help`
