import subprocess
import time

seeds = [16208132657630336028, 16103092055305933704, 13194504476707991180, 18291679442162788626, 17699158152506210103,
         9579134963375520473, 14717479184903010206, 10982552536595074125, 295571224282797294, 6436486695648584287]

ks = [2, 3, 4]

temps = [0.9, 0.95]

num_iters = [100, 110]


def run_scripts(dd, dfs, cd, name, iters, pl=0):
    data_file_directory = dd
    data_files = dfs
    previous_length = pl
    data_collection_directory = cd
    result_file = name + "_fN.csv"
    
    for i, data_file in enumerate(data_files):
        print("started: " + data_file)
        i += previous_length + 1
        for j in range(iters):
            print("    Iteration: " + str(j + 1) + " H4")
            print("file: {0}".format(data_collection_directory + result_file.replace("N", str(i))))
            for seed in seeds:
                for k in ks:
                    for temp in temps:
                        for iter in num_iters:
                            p = subprocess.Popen(["python simulated_annealing.py -c --df {0} --cf {1} --func H4 --seed {2} -k {3} --temp {4} --iters {5}".format(
                                data_file_directory + data_file,
                                data_collection_directory + result_file.replace("N", str(i)),
                                seed, k, temp, iter)],
                                shell=True)
                            
                            p.wait()

if __name__ == "__main__":
    start_time = time.time()

    d_collection_directory = "../results/"

    d_file_directory = "../Instances/taillard/"
    d_files = ["15x15/Ta01.txt", "20x15/Ta11.txt", "20x20/Ta21.txt", "30x15/Ta31.txt", "30x20/Ta41.txt"]

    
    run_scripts(d_file_directory, d_files, d_collection_directory, "JSSPH4_params", 1)
    
    end_time = time.time()
    print()
    print("Execution time", end_time - start_time)