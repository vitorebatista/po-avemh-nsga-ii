import sys
import numpy as np
import random
import pandas as pd
from dec_reprod import avemh
from avemh import optimize


instance = int(sys.argv[1])
rep = 10
benchmarks = ["hangseng", "dax", "ftse", "sp", "nikkei"]
size = [31, 85, 89, 98, 225]
savedir = "tmp/{}/avemh/".format(benchmarks[instance-1])

N, T, gen = 10, 20, 20
sigma, nr = 0.9, 2
par = [1e-05, 0.3, round(1/size[instance-1], 5), 20]

#print(instance, benchmarks[instance-1])
# print(par)
# print("====================================")

for i in range(rep):
    np.random.seed(500+i)
    random.seed(500+i)
    print("Start {}-th experiment.".format(i+1))
    res = optimize(instance, N, T, gen, avemh, par, sigma, nr, True, 100)
    res = pd.DataFrame(res, columns=["return", "risk"])
    res.to_csv(savedir + str(i+1) + ".csv", index=False)
