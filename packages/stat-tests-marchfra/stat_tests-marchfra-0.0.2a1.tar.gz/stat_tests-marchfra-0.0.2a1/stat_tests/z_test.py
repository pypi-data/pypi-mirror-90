import uncertainties
import sympy as sym


def z_test(value : uncertainties.UFloat, alpha : float = 0.05) -> str:
	'''
	Performs a Z test on a value with 0

	:param value: value to test compatibility wit 0
	:param alpha: significance value
	'''

	# This function returns the probability of obtaining a Z value greater than the one obtained
	def P(Z):
		z = sym.symbols('z')
		I = sym.integrate(sym.exp(-z**2 / 2), (z, 0, Z))	# Integral of a gaussian from 0 to Z
		return .5 - I / sym.sqrt(2 * sym.pi)				# Half the area under the curve - the area from 0 to Z

	# Check wether the input type is right
	try:
		assert isinstance(value, uncertainties.UFloat), "The functions accepts UFloat input only"
	except AssertionError as error:
		print(error)
		return AssertionError
	else:
		# The Z test
		Z = abs(value.n / value.s)
		p = float(P(Z).evalf())
		if p > alpha:
			return f'The input value {value} is compatible with 0 with a significance of {alpha*100}%'
		else:
			return f'The input value {value} is not compatible with 0 with a significance of {alpha*100}%'