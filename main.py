from polynom import Polynom


def creationTest():
    print("Creation test:")
    p = Polynom([1, 2, 3])
    print(p)
    print(p(0))
    print(p(2))

def additionTest():
    print("Addition test:")
    p1 = Polynom([1, 2, 3])
    p2 = Polynom([1, 2, 3])
    print(p1 + p2)

def subtractionTest():
    print("Subtraction test:")
    p1 = Polynom([2, 3, 4])
    p2 = Polynom([1, 2, 3])
    print(p1 - p2)

def negationTest():
    print("Negation test:")
    p1 = Polynom([2, 3, 4])
    print(-p1)

def multiplicationTest():
    print("Multiplication test:")
    p1 = Polynom([2, 1])
    print(p1 * p1)
    print(p1 * 2)

def powerTest():
    print("Power test:")
    p1 = Polynom([2, 1])
    print(p1 ** 2)

def equalityTest():
    print("Equality test:")
    p1 = Polynom([2, 1])
    p2 = Polynom([2, 1])
    print(p1 == p2)
    p3 = Polynom([2, 1, 5])
    print(p1 == p3)
    print(p1 != p3)
    p4 = Polynom([2, 5])
    print(p1 == p4)

def derivativeTest():
    print("Derivative test:")
    p1 = Polynom([4, 2, 3])
    print(p1.get_derivative())


def divisionTest():
    print("Division test:")
    p1 = Polynom([4, 2, 3])
    p2 = Polynom([2, 1])
    print(p1 // p2)
    print(p1 % p2)

def solveTest():
    print("Solve test:")

    p1 = Polynom([-3, -6, -1,  4, 2])
    print(p1)
    print(p1.solve())

    p2 = Polynom([1, 2, 1, -5])
    print(p2)
    print(p2.solve())

    p3 = Polynom([1, -4, 1])
    print(p3)
    print(p3.solve())

    p4 = Polynom([1, 4, 2, -1, -2, 2])
    print(p4)
    print(p4.solve())






if __name__ == '__main__':
    creationTest()
    additionTest()
    subtractionTest()
    negationTest()
    multiplicationTest()
    powerTest()
    equalityTest()
    derivativeTest()
    divisionTest()
    solveTest()


