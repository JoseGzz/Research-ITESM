import subprocess

results = {}

def run_scripts(dd, dfs, cd, name, iters, pl=0):
    data_file_directory = dd
    data_files = dfs
    previous_length = pl
    data_collection_directory = cd
    result_file = name + "_fN_rM.csv"
    
    for i, data_file in enumerate(data_files):
        print("started: " + data_file)
        i += previous_length + 1
        for j in range(iters):
            print("    Iteration: " + str(j + 1))
            p = subprocess.Popen(["python simulated_annealing.py --df {0}".format(
                data_file_directory + data_file,
                data_collection_directory + result_file.replace("N", str(i)).replace("M", str(j + 1)))],
                shell=True, stdout=subprocess.PIPE)

            new_makespan = int(p.communicate()[0])
            print("iters: " + str(iters) + " - result: " + str(new_makespan))
            
            if iters in results:
                if results[iters] > new_makespan:
                    results[iters] = new_makespan
            else:
                results[iters] = new_makespan

if __name__ == "__main__":
    d_file_directory = ""
    d_files = ["Ta01.txt"]
    p_length = len(d_files)
    
    d_collection_directory = "../results/"
    
    for i in range(10, 41):
        print("Iters: " + str(i))
        run_scripts(d_file_directory, d_files, d_collection_directory, "JSSP", i)

    with open("../results/results.txt", "w") as file:
        for iters in results:
            file.write(str(results[iters]) + " - " + str(iters))
            file.write("\n")
