import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from attaque import cas2
delta = float(sys.argv[1]); smax = int(sys.argv[2]); essais = int(sys.argv[3])
for Dk in sys.argv[4].split(","):
    D, k = map(int, Dk.split(":"))
    for g in (1, 2):
        print(json.dumps(cas2(D, k, delta, g, smax, essais)), flush=True)
