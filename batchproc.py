import subprocess
import timeit

def main():
    start = timeit.default_timer()
    chunks = ('000', '010', '011', '100', '111', '110')
    processes = []
    for i in range(1,3):
        p = subprocess.Popen(['~/ssh/venv/bin/python getthresh.py -i iso256cube' + str(i) + '.npy -o iso256cube' + str(i) + '.vti -x 0 -a 256 -y 0 -b 256 -z 0 -c 256 -d u00000 -u q', '-1'], shell=True)
        processes.append(p)
    #subprocess.wait()
    print ("Waiting to finish")
    p.wait()
    end = timeit.default_timer()
    print("**********************Final Total time: %s " % str(end-start))
if __name__ == "__main__":
    main()
