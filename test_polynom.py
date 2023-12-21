try:
    from polynom import *
except:
    from .polynom import *
import math


def creationTest():
    p = Polynom([1, 2, 3])
    assert p(0) == 1
    assert p(1) == 6
    assert p(2) == 17

def equalityTest():
    p1 = Polynom([2, 1])
    p2 = Polynom([2, 1])
    assert p1 == p2

    p3 = Polynom([2, 1, 0])
    assert p1 == p3

    p3 = Polynom([2, 1, 1])
    assert p1 != p3

    p4 = Polynom([2, 2])
    assert p1 != p4


def additionTest():
    p1 = Polynom([1, 2, 3])
    p2 = Polynom([1, 2, 3])
    p3 = Polynom([2, 4, 6])
    assert p1 + p2 == p3

def subtractionTest():
    p1 = Polynom([2, 3, 4])
    p2 = Polynom([1, 2, 3])

    p3 = Polynom([1, 1, 1])
    assert p1 - p2 == p3

def negationTest():
    p1 = Polynom([2, 3, 4])
    p2 = Polynom([-2, -3, -4])
    assert -p1 == p2

def multiplicationTest():
    p1 = Polynom([2, 1])

    p2 = Polynom([4, 4, 1])
    assert p1 * p1 == p2

    p3 = Polynom([4, 2])
    assert p1 * 2 == p3

def powerTest():
    p1 = Polynom([2, 1])

    p2 = Polynom([4, 4, 1])
    assert p1 ** 2 == p2


def derivativeTest():
    p1 = Polynom([4, 2, 3])
    p2 = Polynom([2, 6])
    assert p1.get_derivative() == p2

def integralTest():
    p1 = Polynom([2, 1])
    p2 = Polynom([0, 2, 0.5])
    assert p1.get_integral() == p2

    p3 = Polynom([0, 0, 1, 0.5/3])
    assert p2.get_integral() == p3

def factorOutTest():
    p1 = Polynom([0.5, 0.25, 0.1])
    fac, pol = p1.factor_out_to_int()
    assert pol * fac == p1

    p2 = Polynom([0.5, 0.33, 0.16, 0.23])
    fac, pol = p2.factor_out_to_int()
    assert pol * fac == p2


def divisionTest():
    p1 = Polynom([4, 2, 3])
    p2 = Polynom([2, 1])

    assert p1 // p2 == Polynom([-4, 3])
    assert p1 % p2 == Polynom([12])


def solveTest():

    p1 = Polynom([-3, -6, -1,  4, 2])
    sol = p1.solve()
    assert len(sol) == 3
    assert -1 in sol


    p2 = Polynom([1, 2, 1, -5])
    assert len(p2.solve()) == 1

    p3 = Polynom([1, -4, 1])
    assert len(p3.solve()) == 2

    p4 = Polynom([1, 4, 2, -1, -2, 2])
    assert len(p4.solve()) == 1


def limitTest():
    p1 = Polynom([4, 2, 3])
    assert p1.limit(0) == 4
    assert p1.limit(math.inf) == math.inf
    assert p1.limit(-math.inf) == math.inf

    p2 = Polynom([1, 2, 3, -4])
    assert p2.limit(math.inf) == -math.inf
    assert p2.limit(-math.inf) == math.inf

def minmaxTest():
    p1 = Polynom([4, 3, 3])
    assert p1.max() == math.inf
    assert p1.min() == 3.25

    p2 = Polynom([1, 2, 3, -4])
    assert p2.max() == math.inf
    assert p2.min() == -math.inf

def taylorTest():
    # Test with sin(x)
    derivatives_at_0 = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1]
    sin = create_taylor(derivatives_at_0)
    # Test vs math.sin
    for i in range(3):
        assert abs(sin(i) - math.sin(i)) < 4

    # Test with exp(x)
    derivatives_at_0 = [1] * 10
    exp = create_taylor(derivatives_at_0)
    # Test vs math.exp
    for i in range(3):
        assert abs(exp(i) - math.exp(i)) < 4

    e= math.exp(1)
    derivatives_at_1 = [e] * 10
    exp_at_1 = create_taylor(derivatives_at_1, 1)
    # Test vs math.exp
    for i in range(3):
        assert abs(exp_at_1(i) - math.exp(i)) < 4

def fromStringTest():
    p1 = Polynom([4, 2, 3])
    p2 = polynom_from_string(str(p1))
    assert p1 == p2

def createFromRootsTest():
    p1 = create_polynom_from_roots([-1, 0, 1, 2])
    assert p1 == Polynom([0, 2, -1, -2, 1])


tests = [
    creationTest,
    equalityTest,
    additionTest,
    subtractionTest,
    negationTest,
    multiplicationTest,
    powerTest,
    derivativeTest,
    integralTest,
    factorOutTest,
    divisionTest,
    solveTest,
    limitTest,
    minmaxTest,
    taylorTest,
    fromStringTest,
    createFromRootsTest
]


def run_all_test(testings):
    for test in testings:
        try:
            test()
            print('\033[92m', test.__name__.ljust(30), "passed", '\033[0m')
        except AssertionError:
            print("\033[91m",test.__name__.ljust(30), "failed", '\033[0m')


if __name__ == '__main__':
    run_all_test(tests)


