import numbers


class Polynom:

    def __init__(self, coefficients):
        for i in range(len(coefficients)-1, 0, -1):
            if coefficients[i] == 0:
                coefficients.pop(i)
            else:
                break
        self.coefficients = coefficients

    def calc(self, x):
        y = 0
        for i in range(len(self.coefficients)):
            y += x ** i * self.coefficients[i]
        return y

    def __call__(self, x):
        return self.calc(x)

    def get_coef(self, i):
        if 0 <= i < len(self.coefficients):
            return self.coefficients[i]
        return 0

    def get_derivative(self):
        coeffs_deri = [0] * (len(self.coefficients) - 1)
        for i in range(len(coeffs_deri)):
            coeffs_deri[i] = self.coefficients[i+1] * (i+1)
        return Polynom(coeffs_deri)

    def solve(self):
        if len(self.coefficients) == 1:
            return []
        if len(self.coefficients) == 2:
            return [-self.coefficients[0] / self.coefficients[1]]
        if len(self.coefficients) == 3:
            a = self.coefficients[2]
            b = self.coefficients[1]
            c = self.coefficients[0]
            delta = b ** 2 - 4 * a * c
            if delta < 0:
                return []
            if delta == 0:
                return [-b / (2 * a)]
            return [(-b - delta ** 0.5) / (2 * a), (-b + delta ** 0.5) / (2 * a)]

        # Try Rational Root Theorem
        a = self.coefficients[0]
        b = self.coefficients[-1]
        divisors_a = numbers.factors(abs(a))
        divisors_b = numbers.factors(abs(b))
        solutions = set()
        for i in divisors_a:
            for j in divisors_b:
                if abs(self(i / j)) <= 10e-6:
                    solutions.add(i / j)
                if abs(self(-i / j)) <= 10e-6:
                    solutions.add(-i / j)
        if len(solutions) > 0:
            n = self
            for s in solutions:
                n = n // Polynom([-s, 1])
            return list(set(list(solutions) + n.solve()))

        # Use Newton's method
        x = 0
        deri = self.get_derivative()
        y = self(x)
        n = 4000
        while abs(y) > 1e-10:
            x = x - y / deri(x)
            y = self(x)
            n-=1
            if n <= 0:
                return []
        return list(set([x] + (self // Polynom([-x, 1])).solve()))



    def __add__(self, other):
        co = [self.get_coef(i) + other.get_coef(i) for i in range(max(len(self.coefficients), len(other.coefficients)))]
        return Polynom(co)

    def __sub__(self, other):
        co = [self.get_coef(i) - other.get_coef(i) for i in range(max(len(self.coefficients), len(other.coefficients)))]
        return Polynom(co)

    def __neg__(self):
        co = [-self.get_coef(i) for i in range(len(self.coefficients))]
        return Polynom(co)

    def __mul__(self, other):
        if type(other) != type(self):
            if type(other) == int or type(other) == float:
                return Polynom([self.coefficients[i] * other for i in range(len(self.coefficients))])
            return NotImplemented
        co = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                co[i + j] += self.coefficients[i] * other.coefficients[j]
        return Polynom(co)

    def __rmul__(self, other):
        co = [0] * len(self.coefficients)
        for i in range(len(self.coefficients)):
            co = self.coefficients[i] * other
        return co

    def __floordiv__(self, other):
        if type(other) != type(self):
            if type(other) == int or type(other) == float:
                return Polynom([self.coefficients[i] // other for i in range(len(self.coefficients))])
            return NotImplemented
        if len(self.coefficients) < len(other.coefficients):
            return Polynom([0])
        # Use Polynomial long division, dont change self
        coeff_self = self.coefficients.copy()
        co = [0] * (len(self.coefficients) - len(other.coefficients) + 1)
        for i in range(len(self.coefficients) - len(other.coefficients), -1, -1):
            co[i] = coeff_self[i + len(other.coefficients) - 1] // other.coefficients[-1]
            for j in range(len(other.coefficients)):
                coeff_self[i + j] -= co[i] * other.coefficients[j]
        return Polynom(co)


    def __mod__(self, other):
        if type(other) != type(self):
            if type(other) == int or type(other) == float:
                return Polynom([self.coefficients[i] % other for i in range(len(self.coefficients))])
            return NotImplemented
        if len(self.coefficients) < len(other.coefficients):
            return Polynom(self.coefficients)
        # Use Polynomial long division
        coeff_self = self.coefficients.copy()
        co = [0] * (len(self.coefficients) - len(other.coefficients) + 1)
        for i in range(len(self.coefficients) - len(other.coefficients), -1, -1):
            co[i] = coeff_self[i + len(other.coefficients) - 1] // other.coefficients[-1]
            for j in range(len(other.coefficients)):
                coeff_self[i + j] -= co[i] * other.coefficients[j]
        return Polynom(coeff_self)

    def __truediv__(self, other):
        return (self.__floordiv__(other), self.__mod__(other))

    def __pow__(self, n):
        if n < 0:
            raise ValueError("n must be greater than 0")
        if n == 0:
            return Polynom([1])
        if n > 0:
            return self * self ** (n - 1)

    def __eq__(self, other):
        if len(self.coefficients) != len(other.coefficients):
            return False
        for i in range(len(self.coefficients)):
            if self.coefficients[i] != other.coefficients[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = ""
        for i in range(len(self.coefficients)-1, 0, -1):
            s += str(self.coefficients[i]) + "x^{" + str(i) + "} + "
        s += str(self.coefficients[0])
        return s
