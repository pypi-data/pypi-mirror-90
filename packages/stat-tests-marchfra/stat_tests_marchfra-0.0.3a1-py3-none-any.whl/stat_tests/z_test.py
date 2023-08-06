import uncertainties
import sympy as sym


def z_test(value : uncertainties.UFloat, alpha : float = 0.05) -> bool:
	'''
	Performs a Z test on a value with 0

	:param value: value to test compatibility wit 0. Has to be an instance of uncertainties.UFloat
	:param alpha: significance value. Defaults to 5%

	returns True if the input value is compatible with 0 with the specified significance, False otherwise
	'''

	# This function returns the probability of obtaining a Z value greater than the one obtained
	def P(Z):
		z = sym.symbols('z')
		I = sym.integrate(sym.exp(-z**2 / 2), (z, 0, Z))	# Integral of a gaussian from 0 to Z
		return .5 - I / sym.sqrt(2 * sym.pi)				# Half the area under the curve - the area from 0 to Z

	# Check wether the input type is right
	try:
		assert isinstance(value, uncertainties.UFloat), f"The function accepts UFloat input only; you tried to pass {type(value)}"
		if alpha > 1:
			raise ValueError(f"The significance value should be smaller than 1; you entered {alpha}")
	except AssertionError as error:
		print(error)
		return AssertionError
	except ValueError as error:
		print(error)
		return ValueError
	else:
		# The Z test
		Z = abs(value.n / value.s)
		p = float(P(Z).evalf())
		if p > alpha:
			return True
		else:
			return False