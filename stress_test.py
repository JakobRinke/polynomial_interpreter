from polynom import *
import random
from test_polynom import run_all_test

random.seed = 42

def integerRootsTest():
    range1 = 3
    st = set()
    polynom = Polynom([1])
    for i in range(20):
        n = random.randrange(0, range1)
        st.add(n)
        s = sum(st)
        polynom *= Polynom([-n, 1])
        k = polynom.solve()
        s2 = sum(k)
        if len(st) == len(k):
            print("\tAccuracy at ".ljust(15), str(i).rjust(3), "  ", str(round(1-abs(1-s/s2)*100)).rjust(7), '\033[0m')
        else:
            print("\tFailed at ", i, '\033[0m')
            assert False
        

        range1 += 1

    
def rationalRootsTest():
    range1 = 3
    st = set()
    polynom = Polynom([1])
    for i in range(10):
        n = random.random() * range1
        st.add(n)
        s = sum(st)
        polynom *= Polynom([-n, 1])
        k = polynom.solve()
        s2 = sum(k)
        if len(st) == len(k):
            print("\tAccuracy at ".ljust(15), str(i).rjust(3), "  ", str(round(1-abs(1-s/s2)*100)).rjust(7), '\033[0m')
        else:
            print("\tFailed at ", i, '\033[0m')
            assert False
        

        range1 += 1




test = [
    integerRootsTest,
    rationalRootsTest
]

if __name__ == "__main__":
    run_all_test(test)