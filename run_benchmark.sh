benchmarks=("hangseng" "dax" "ftse" "sp" "nikkei")

mkdir ./tmp/${benchmarks[$1-1]}
mkdir ./tmp/${benchmarks[$1-1]}/avemh
mkdir ./tmp/${benchmarks[$1-1]}/nsga2

python run_avemh.py $1 >> ./tmp/${benchmarks[$1-1]}/avemh/igd.txt
echo Finish AVEMH on $1

python run_nsga2.py $1 >> ./tmp/${benchmarks[$1-1]}/nsga2/igd.txt
echo Finish NSGA-II on $1
