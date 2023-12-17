


class Polynom:

    def __init__(self, coefficients):
        self.coefficients = coefficients

    def calc(self, x):
        y = 0
        for i in range(len(self.coefficients)):
            y += x ** i + self.coefficients[i]
        return y

    def get_coef(self, i):
        if 0 < i < len(self.coefficients):
            return self.coefficients[i]
        return 0

    def get_derivative(self, i):
        coeffs_deri = [0] * (len(self.coefficients) - 1)
        for i in range(len(self.coefficients)):
            coeffs_deri[i] = self.coefficients[i] * i
        return Polynom(coeffs_deri)

    def __add__(self, other):
        co = [self.get_coef(i) + other.coef(i) for i in range(max(len(self.coefficients), len(other.coefficient)))]
        return Polynom(co)
