import uncertainties
import sympy as sym


def P(Z):
	z = sym.symbols('z')
	I = sym.integrate(sym.exp(-z**2 / 2), (z, 0, Z))
	return .5 - I / sym.sqrt(2 * sym.pi)


def z_test(value : uncertainties.UFloat, alpha : float = 0.05) -> bool:
	'''
	Performs a Z test on a value with 0

	:param value: value to test compatibility wit 0
	:param alpha: significance value
	'''

	try:
		assert isinstance(value, uncertainties.UFloat), "The functions accepts UFloat input only"
	except AssertionError as error:
		print(error)
		return AssertionError
	else:
		Z = abs(value.n / value.s)
		p = float(P(Z).evalf())
		if p > alpha:
			return True
		else:
			return False