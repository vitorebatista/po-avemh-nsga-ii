import numpy as np
import pandas as pd
import prob
from nbi_decomp import neighbor
from nbi_decomp import extreme_point
from nbi_decomp import update_extreme
from nbi_decomp import utopia_points
from nbi_decomp import weight_vector
from nbi_decomp import to_update
from metric import igd
from utils import population, objective
from enum import Enum, unique


@unique
class Heuristic(Enum):
    PSO = 0
    ABC = 1
    DE = 2


# TODO: it is possible to create a class to control these variables
initial_probability = 0.33
heuristic_probability = {
    Heuristic.PSO: initial_probability,
    Heuristic.ABC:  initial_probability,
    Heuristic.DE:  initial_probability
}


def reward(h):
    # se houve uma melhora, a probabilidade da heurística que enviou o indivíduo é
    # incrementada em 0.01, enquanto que as demais são diminuídas em 0.005
    for i in Heuristic:
        if i == h:
            heuristic_probability[h] += 0.001
        else:
            heuristic_probability[i] -= 0.005


def penalize(h):
    # se não houve melhora, a heurística que enviou o indivíduo tem sua probabilidade
    # decrementada em 0.01 e as demais tem sua probabilidade aumentada em 0.005
    for i in Heuristic:
        if i == h:
            heuristic_probability[h] -= 0.01
        else:
            heuristic_probability[i] += 0.005


def choose_heuristic():
    """
    Escolha da heurística que ser á executada

    @param ‘‘ probabilidades ’’ que representa o vetor mantido com as probabilidades de cada heur í stica utilizada
    Caso resultado seja 0, a heur í stica escolhida é o PSO ;
    Caso resultado seja 1, a heur í stica escolhida é o ABC ;
    Caso resultado seja 2, a heur í stica escolhida é o DE;
    """
    value = np.random.uniform(0.001, 1)
    # print(value)
    if value < heuristic_probability[Heuristic.PSO]:
        return Heuristic.PSO
    elif value >= heuristic_probability[Heuristic.PSO] and value < (heuristic_probability[Heuristic.PSO] + heuristic_probability[Heuristic.ABC]):
        return Heuristic.ABC
    return Heuristic.DE


def best_individual(h):
    # /**
    # *Mé todo estático que avalia a nova população a partir de seu melhor
    # indiv íduo . Neste caso é considerado o melhor o indiv í duo que
    # atende como melhor na popula ção para a qual ser á enviado .
    # *
    # * @param ‘‘pop ’’ popula ção da qual sair á o melhor indiv í duo
    # * @param ‘‘i ’’ indiv íduo enviado - candidato a ser o melhor indiv índuo da popula ção que chega esta chegando
    # * @param ‘‘i_ ’’ melhor indiv í duo consolidado da popula ção para a qual o candidato sera enviado
    # *
    # * @return boolean , caso o candidato seja melhor que o melhor indiv índividuo consolidado da popula ção retorna true ; caso contr ário , retorna false
    # */
    # public static boolean MelhorInd ( Populacao pop , Individuo i ,
    # Individuo i_ ) {
    #  boolean sinal = false ;
    #  pop . getProblema () . qualidadeIndividuo_ (i , pop ) ;
    #  if( pop . getProblema () . isMaximizacao ( pop . getFuncao () )) {
    #  if( (i . getQualidades2 () > i_ . getQualidades2 () ) && ( i.
    # getQualidades2 () > 0) ){
    #  sinal = true ;
    #  }
    #  } else {
    #  if( (i . getQualidades1 () < i_ . getQualidades1 () ) && ( i.
    # getQualidades1 () > 0) ){
    #  sinal = true ;
    #  }
    #  }
    #  return sinal ;
    #  }
    reward(h)


def execute_heuristic(heuristic, N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2):
    # TODO: sorry for the amount of parameters :(
    if heuristic == Heuristic.PSO:
        return execute_pso(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)
    elif heuristic == Heuristic.ABC:
        return execute_abc(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)
    elif heuristic == Heuristic.DE:
        return execute_de(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)
    else:
        print("Unexpected heuristic:", heuristic)
        raise


def execute_pso(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2):
    return execute_de(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)


def execute_abc(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2):
    return execute_de(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)


def execute_de(N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2):
    for i in range(len(P)):  # for every individual
        if np.random.uniform(0, 1) < sigma:  # decide parent source
            b = B[i]  # parent source from neighbor
        else:
            b = np.arange(N//2)  # parent source from whole population
        y = operator(P, i, b, lb, ub, par)  # reproduce a offspring
        ############################################################
        # enable this line to compute length of trial vector
        # len_trial = np.linalg.norm(y-P[i])
        ############################################################
        obj_y = objective([y], port, r, s, c)[0]  # evaluate offspring
        M_y, V_y = obj_y[0], obj_y[1]
        F1, F2 = update_extreme(obj_y, F1, F2)  # update CHIM
        w = weight_vector(F1, F2)  # compute normal vector
        Z = utopia_points(N, F1, F2)  # compute reference points on CHIM
        update_count = 0  # update limit counter for neighbors
        np.random.shuffle(b)  # shuffle parent source
        for bi in b:
            zk = Z[bi]
            obj_k = objs[bi]
            M_k, V_k = obj_k[0], obj_k[1]
            if to_update(M_y, V_y, M_k, V_k, w, zk):  # Tchebycheff value
                P[bi] = y  # update to value of offspring
                objs[bi] = obj_y
                update_count += 1
            if update_count >= nr:
                break  # break if reached update limit
        ################################################################
        # enable this line to record successfully updated times
        # record_file = open("lvx.csv", "a")
        # record_file.write(f"{t},{len_trial},{update_count}\n")
        ################################################################
    return objs, F1, F2, P


def optimize(instance, N, T, gen, operator, par, sigma, nr, cflag, cgen):
    t, count, temp = 0, 0, 0  # current generation, values used in convergence
    _, r, s, c, lb, ub, port, mp, vp = prob.set(instance)  # set up problem
    B = neighbor(N//2, T)  # determine neighbors
    P = population(lb, ub, N//2)  # initialize a population 1
    P2 = population(lb, ub, N//2)  # initialize a population 2
    objs = objective(P, port, r, s, c)  # evaluate objectives
    # compute convex hull of individual maxima (CHIM)
    F1, F2 = extreme_point(objs)
    ####################################################################
    indicator_value = igd(objs, mp, vp)  # compute IGD metric
    print("{}\t{}".format(t, indicator_value))
    ####################################################################
    while t < gen:  # start loop
        heuristic = choose_heuristic()
        objs, F1, F2, P = execute_heuristic(
            heuristic, N, operator, par, sigma, nr, B, P, lb, ub, port, r, s, c, objs, F1, F2)

        best_individual(heuristic)
        t += 1
        ####################################################################
        # enable this line to save population onjectives during run
        # if t in [0,1,2,3,4,5,10,20,30,50,100,150,200,300]:
        #     pd.DataFrame(objs, columns=["return", "risk"]).to_csv(
        #         f"lvx_pop_gen_{t}.csv", index=False)
        ####################################################################
        indicator_value = igd(objs, mp, vp)  # compute IGD metric
        print("{}\t{}".format(t, indicator_value))
        ####################################################################
        if np.abs(indicator_value - temp) >= 1e-05:
            temp = indicator_value
            count = 0
        else:
            count += 1
        if count >= cgen and cflag == True:
            break  # convergence judgement
    return objs
