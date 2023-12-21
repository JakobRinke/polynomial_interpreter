from polynom import *
import random
from test_polynom import run_all_test


def integerRootsTest():
    range1 = 3
    st = set()
    polynom = Polynom([1])
    for i in range(10):
        n = random.randrange(0, range1)
        st.add(n)
        s = sum(st)
        polynom *= Polynom([-n, 1])
        k = polynom.solve()
        s2 = sum(k)
        print("Accuracy at ".ljust(15), str())


        range1 += 1

    




test = [
    integerRootsTest,
]

if __name__ == "__main__":
    run_all_test(test)