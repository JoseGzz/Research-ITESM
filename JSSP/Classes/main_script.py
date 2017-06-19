import subprocess
import time


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
            print("    Iteration: " + str(j + 1))
            p = subprocess.Popen(["python simulated_annealing.py -c --df {0} --cf {1}".format(
                data_file_directory + data_file,
                data_collection_directory + result_file.replace("N", str(i)))],
                shell=True)
            
            p.wait()

if __name__ == "__main__":
    start_time = time.time()
    #d_file_directory = "../Instances/toy/"
    #d_files = ["3x3_demo.txt", "4x4_demo.txt", "5x5_demo.txt", "10x10_demo.txt"]
    #p_length = len(d_files)

    d_collection_directory = "../results/"
    
    #run_scripts(d_file_directory, d_files, d_collection_directory, "JSSP", 20)

    d_file_directory = "../Instances/taillard/"
    #d_files = ["15x15/Ta01.txt", "20x15/Ta11.txt", "20x20/Ta21.txt", "30x15/Ta31.txt", "30x20/Ta41.txt",
                  #"50x15/Ta51.txt", "50x20/Ta61.txt", "100x20/Ta71.txt"]
    
    d_files = ["100x20/Ta71.txt"]

    run_scripts(d_file_directory, d_files, d_collection_directory, "JSSP", 19, 15)
    
    end_time = time.time()
    print()
    print("Execution time", end_time - start_time)