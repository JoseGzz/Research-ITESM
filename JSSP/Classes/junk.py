import random
from datetime import datetime

if __name__ == "__main__":
    values = []
    for i in range(10):
        random.seed(datetime.now())
        for j in range(10):
            values.append(random.getrandbits(64))

    
    with open("seeds.txt", "w") as file:
        # write the column names in the first line of the file
        for value in values:
            file.write(str(value))
            file.write("\n")
