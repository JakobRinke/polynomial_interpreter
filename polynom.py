import numbers
import math

ACCURACY = 10e-6
SPEED_BREAK = 4000

class Polynom:

    def __init__(self, coefficients):
        if coefficients == []:
            coefficients = [0]
        for i in range(len(coefficients)-1, 0, -1):
            if coefficients[i] == 0:
                coefficients.pop(i)
            else:
                break
        self.coefficients = coefficients

    def calc(self, x):
        y = 0
        x_c = 1
        for i in range(len(self.coefficients)):
            y += x_c * self.coefficients[i]
            x_c *= x
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

    def get_integral(self):
        coeffs_inte = [0] * (len(self.coefficients) + 1)
        for i in range(len(self.coefficients)):
            coeffs_inte[i+1] = self.coefficients[i] / (i+1)
        return Polynom(coeffs_inte)

    def factor_out_to_int(self):
        factor = numbers.least_common_multiplier([c for c in (self.coefficients + [1])])
        coefficients = [c * factor for c in self.coefficients]
        outPoly = Polynom(coefficients)
        return 1 / factor, outPoly



    def limit(self, x):
        if len(self.coefficients) == 1:
            return self.coefficients[0]
        if x == math.inf:
            return numbers.sign(self.coefficients[-1]) * math.inf
        elif x == -math.inf:
            if len(self.coefficients) % 2 == 1:
                return numbers.sign(self.coefficients[-1]) * math.inf
            else:
                return -1 * numbers.sign(self.coefficients[-1]) * math.inf
        else:
            return self(x)

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
        fac, pl = self.factor_out_to_int() 
        a = pl.coefficients[0]
        b = pl.coefficients[-1]

        divisors_a = numbers.factors(abs(a))
        divisors_b = numbers.factors(abs(b))
        if len(divisors_a) * len(divisors_b) <= SPEED_BREAK:
            solutions = set()
            for i in divisors_a:
                for j in divisors_b:
                    if abs(pl(i / j)) <= ACCURACY:
                        solutions.add((i / j))
                    if abs(pl(-i / j)) <= ACCURACY:
                        solutions.add((-i / j))
            if len(solutions) > 0:
                n = self
                for s in solutions:
                    n = n // Polynom([-s, 1])
                return list(set(list(solutions) + n.solve()))


        # Use Newton's method
        x = 0
        deri = self.get_derivative()
        y = self(x)
        n = SPEED_BREAK
        while abs(y) > ACCURACY:
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

    def max(self, interval=(-math.inf, -math.inf)):
        m1 = self.limit(interval[0])
        m2 = self.limit(interval[1])
        m = max(m1, m2)
        if m == math.inf:
            return math.inf
        deri = self.get_derivative()
        extrems = deri.solve()
        for extrem in extrems:
            if interval[0] <= extrem <= interval[1]:
                m = max(m, self(extrem))
        return m

    def min(self, interval=(-math.inf, math.inf)):
        m1 = self.limit(interval[0])
        m2 = self.limit(interval[1])
        m = min(m1, m2)
        if m == -math.inf:
            return -math.inf
        deri = self.get_derivative()
        extrems = deri.solve()
        for extrem in extrems:
            if interval[0] <= extrem <= interval[1]:
                m = min(m, self(extrem))
        return m

    def get_extrems(self):
        deri = self.get_derivative()
        return deri.solve()

    def get_all_max(self, interval=(-math.inf, math.inf)):
        deri1 = self.get_derivative()
        deri2 = deri1.get_derivative()
        extrems = deri1.solve()
        return [x for x in extrems if interval[0] <= x <= interval[1] and deri2(x) < 0]

    def get_all_min(self, interval=(-math.inf, math.inf)):
        deri1 = self.get_derivative()
        deri2 = deri1.get_derivative()
        extrems = deri1.solve()
        return [x for x in extrems if interval[0] <= x <= interval[1] and deri2(x) > 0]

    def integral(self, a, b):
        inte = self.get_integral()
        return inte(b) - inte(a)





def create_taylor( derivatives:list, start=0):
    if start == 0:
        f = 1
        coeff = []
        for i in range(len(derivatives)):
            coeff.append(derivatives[i] / f)
            f*=(i+1)
        return Polynom(coeff)
    else:
        f = 1
        coeff = [0] * len(derivatives)
        # Use binomial coefficient for taylor at (x- start)
        for i in range(len(derivatives)):
            for l in range(i+1):
                coeff[i-l] += (derivatives[i] / f) * math.comb(i, l) *  (-start)**(l)
            f*=(i+1)
        return Polynom(coeff)

def find_intersection(p1:Polynom, p2:Polynom):
    # Find union of two polynoms
    p = p1 - p2
    return [(x, p1(x)) for x in p.solve()]

def polynom_from_string(s:str):
    s = s.lower()
    s = s.replace(" ", "")
    factors = s.split("+")
    factors.reverse()
    coefficients = []
    for factor in factors:
        if factor == "":
            continue
        cf = factor.split("x^")
        if len(cf) == 1:
            coeff = cf[0]
            power = ""
        else:
            coeff = cf[0]
            power = cf[1]
        if coeff == "":
            coeff = 1
        if power == "":
            power = 0
        elif power == "{}":
            power = 1
        else:
            power = int(power.replace("{", "").replace("}", ""))
        if len(coefficients) <= power:
            coefficients += [0] * (power - len(coefficients) + 1)
        coefficients[power] = float(coeff)
    return Polynom(coefficients)

def create_polynom_from_roots(roots):
    p = Polynom([1])
    for root in roots:
        p *= Polynom([-root, 1])
    return p


