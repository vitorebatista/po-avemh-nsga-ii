if [ -d ./tmp ]; then
  rm -rf ./tmp
  mkdir ./tmp
fi

bash ./run_benchmark.sh 1 #hangseng
bash ./run_benchmark.sh 2 #dax
bash ./run_benchmark.sh 3 #ftse
bash ./run_benchmark.sh 4 #sp
bash ./run_benchmark.sh 5 #nikkei

