---
layout: post
title: 'Expression templates in C++'
author: Bob
categories: [C++, tutorial]
image: assets/images/expression_templates.jpg
---

The usual approach to designing scientific computing libraries in C++ involves coming up with “the right” object-oriented model and making the library-API fit this model. An alternative approach is to design the library in such a way that it serves as another language (e.g., DSEL) making the code clear to the end-user. This enables one to code “what we want to do“ instead of “what we should do to get the effect we want“. One way to accomplish this is by using expression templates (ETs). The other advantages of ETs are

- we can capture entire mathematical expressions (similar to ASTs) in complex proxy objects without the need to evaluate them. Evaluation is defered until the code that triggers the computation
- it enables lazy evaluation amenable to compile-time optimizations
- we can avoid temporary objects in chained operations
- we can traverse the expression tree, evaluate the expression based on the data type at hand, inject additional computation like adjoint variables in an automatic differentiation setting etc.

## Example

Using the matrix class shown [here](https://prav-nak.github.io/blog-articles/tiny-C++-library-for-matrix-algebra/), we can write matrix expressions as follows:

```cpp
Matrix<double> A(10,10,1.0);
Matrix<double> B(10,10,1.0);
Matrix<double> C(10,10,1.0);
Matrix<double> D(10,10,1.0);

D = A + B * C;
```

Even though this mimics natural mathematical notation, it unfortunately degrades computational performance by creating multiple temporary objects. Such superfluous temporary objects in expressions can be avoided through the use of expression templates.

## ETs

We use CRTP to define our unary and binary expressions as follows:

```cpp
template <class Derived>
struct base_expr;


template <class Derived>
struct base_expr {

	public:
		base_expr() : _v{static_cast<Derived*>(this)}{}
		auto const& self() const {
			return ( static_cast<const Derived&> (*this));
		}

		auto operator()() {
			return self()();
		}

	private:
		Derived* _v;

};

// Operation is a type which in itself is a callable object.
// I evaluate my Operand and whatever it evaluates, I pass it on to the operation
// and I return whatever this operation returns.
template<class Operation, class Operand>
struct unary_expr : public base_expr<unary_expr<Operation, Operand> > {

	explicit unary_expr(const Operand& val) : _val(val) {
	}

	auto operator()() const {
		return _op(_val());
	}

	private:
	Operation _op;
	Operand _val;
};

template<class Operation, class Operand1, class Operand2>
struct binary_expr : public base_expr<binary_expr<Operation, Operand1, Operand2> > {

	explicit binary_expr(const Operand1& val1, const Operand2& val2) : _val1(val1), _val2(val2) {

	}
	auto operator()() const {
		return _op(_val1(), _val2());
	}

	private:
	Operation _op;
	Operand1 _val1;
	Operand2 _val2;
};
```

Then we have operations for each template type as follows:

```cpp
// For every template type, you now have to define the following operations
// For example, if you have a matrix class, then it should contain a + operator
// if you want the following plus_ to be delegated to the underlying types
struct plus_ {

	template<typename T, typename U>
	auto operator()(T const& t, U const& u) const {
			return t+u;
	}

};
```

```cpp
// We have a special case called terminal which is a leaf of a tree.
template<class T>
struct terminal : public base_expr<terminal<T> >{

	explicit terminal(const T& val) : _val(val){}

	auto operator()() const {
		return _val;
	}

	private:
	T _val;
};
```

Finally we overload the operators as shown below:

```c
template <typename E1, typename E2>
auto operator+(base_expr<E1> const& e1, base_expr<E2> const& e2) {
	return binary_expr<plus_,E1, E2>{e1.self(), e2.self()};
}
```

Such a code would let us capture the entire expression tree and evaluate it only when we want to (that is done by calling the () operator). As a simple example,

```cpp
auto d = terminal<int>{4};
auto e = terminal<int>{5};
auto f = terminal<int>{6};
auto g = terminal<int>{7};
auto h = d + e*f - g; // At this point, the expression is not evaluated yet. h holds the entire express tree.

std::cout << e() <<"\n"; // Only now, the expression is evaluated without any temporaries.
```

In the above code, if we have an appropriate templatized Matrix class, we could use that in place of integer datatype to achieve code as follows:

```cpp
Matrix<double> A(10,10,1.0); // Matrix(number of rows, number of columns, default value)
Matrix<double> B(10,10,1.0);
Matrix<double> C(10,10,1.0);

auto D = A + B*C; // This only captures the expression without evaluating it.
std::cout <<"Evaluation without temporaties is done when the following syntax is encountered "<<D()<<std::endl;
```

