---
layout: post
title: 'Forward automatic differentiation using dual arithmetic'
author: Bob
categories: [C++, AD]
image: assets/images/dual.jpg
---

Automatic Differentiation (AD) is used to calculate the derivative of outputs of a model with respect to its inputs. Derivatives play a fundamental role in different areas of mathematics, statistics and engineering. For example, derivatives are needed to calculate:

- Gradients of objective functions used in optimization, parameter estimation and training of machine learning algorithms.
- Jacobian matrices required to solve stiff systems of differential equations.
- Local sensitivity of models to inputs.
- Uncertainty and error propagation through models.

We use dual numbers to implement forward AD using C++ as they are very easy and transparent to code. We create a new Dual datatype that automatically carries the derivative information. All we have to do is to implement dual arithmetic using overloading. Forward AD as opposed to reverse AD is computationally preferable in cases when the number of function evaluations exceed the number of parameters for which we are trying to compute the derivatives.

```cpp
template <typename Scalar>
class Dual
{
	public:
		typedef Scalar ScalarType;

		Dual(Scalar real = Scalar(), Scalar dual = Scalar());
		template <typename Scalar2>
			Dual(const Dual<Scalar2> &rhs);

		Scalar real() const;
		Scalar dual() const;

		Dual<Scalar> &operator=(Scalar rhs);
		Dual<Scalar> &operator+=(Scalar rhs);
		Dual<Scalar> &operator-=(Scalar rhs);
		Dual<Scalar> &operator*=(Scalar rhs);
		Dual<Scalar> &operator/=(Scalar rhs);

		template <typename Scalar2>
			Dual<Scalar> &operator=(const Dual<Scalar2> &rhs);
		template <typename Scalar2>
			Dual<Scalar> &operator+=(const Dual<Scalar2> &rhs);
		template <typename Scalar2>
			Dual<Scalar> &operator-=(const Dual<Scalar2> &rhs);
		template <typename Scalar2>
			Dual<Scalar> &operator*=(const Dual<Scalar2> &rhs);
		template <typename Scalar2>
			Dual<Scalar> &operator/=(const Dual<Scalar2> &rhs);

		Scalar mReal;
		Scalar mDual;

	private:
};


template <typename Scalar>
Dual<Scalar> sin(const Dual<Scalar> &z) {
	return Dual<Scalar>(sin(z.real()), z.dual() * cos(z.real()));
}

template <typename Scalar>
Dual<Scalar> cos(const Dual<Scalar> &z) {
	return Dual<Scalar>(cos(z.real()), -z.dual() * sin(z.real()));
}

template <typename Scalar>
Dual<Scalar> tan(const Dual<Scalar> &z) {
	Scalar x = tan(z.real());
	return Dual<Scalar>(x, z.dual() * (Scalar(1) + x * x));
}
```

## Example usage

```cpp
Dual<double> x(0.0, 1.0);
auto z = sin(x) + cos(x) + tan(x);
std::cout<<"z deriv = "<<z.dual()<<std::endl;
```

This can be easily extended to handle tensors as shown [here](https://github.com/prav-nak/forward-ad). All one has to do is implement basic arithmetic operations and the derivative information is automatically carried forward.
