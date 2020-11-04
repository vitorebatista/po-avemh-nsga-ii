# Portfolio optimisation with AVEMH and NSGA-II

## AVEMH

Adaptive Vector Multiobjective Heuristics is... (wip)

## NSGA-II

NSGA-II is one of the most popular multi objective optimization algorithms with three special characteristics, fast non-dominated sorting approach, fast crowded distance estimation procedure and simple crowded comparison operator

## Instances

There are currently 5 data files of [OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/portinfo.html).

These data files are the test problems used in the paper:
Chang, T.-J., Meade, N., Beasley, J.E. and Sharaiha, Y.M.,
"Heuristics for cardinality constrained portfolio optimisation"
Comp. & Opns. Res. 27 (2000) 1271-1302.

The test problems are the files:
port1, port2, ..., port5

The format of these data files is:
number of assets (N)
for each asset i (i=1,...,N):
mean return, standard deviation of return
for all possible pairs of assets:
i, j, correlation between asset i and asset j

The unconstrained efficient frontiers for each of these
data sets are available in the files:
portef1, portef2, ..., portef5

The format of these files is:
for each of the calculated points on the unconstrained frontier:
mean return, variance of return

### Disclamer

One more analysis of new approach used in portfolio optimization. Others can be [found here](https://www.scielo.br/scielo.php?script=sci_arttext&pid=S0103-65132020000100404&tlng=en#c01)
