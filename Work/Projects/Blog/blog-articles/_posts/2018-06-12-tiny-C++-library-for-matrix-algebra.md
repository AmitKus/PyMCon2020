---
layout: post
title: 'Tiny C++ header-only library for matrix algebra'
author: Bob
categories: [C++, tutorial]
image: assets/images/matrix_multiplication.jpg
---

Several numeric libraries exist for matrix algebra, e.g., Armadillo, Eigen, etc. It is important to have exposure to LAPACK as an exercise in scientific computing. Also, when prototyping code, one may require a quick and dirty way to perform matrix computations with minimal external dependencies. Here is a high-level C++ class that wraps around low-level LAPACK subroutines. The full repo is located [here](https://github.com/prav-nak/pub-Matrix-library). This is a small header only C++ library for matrix algebra. It consists of

- A templated matrix class with overloaded operators for
  - matrix-vector operations
  - matrix-matrix operations
- Solution to a system of equations using QR decomposition

<span style="color: red">This, by no means, is a computationally performant code and is only to be used for prototyping purposes. This code is later improved using expression templates.
</span>

## The matrix class

```cpp
template<typename T>
class Matrix {

    private:
        std::vector<std::vector<T> > mat;
        unsigned _nRows;
        unsigned _nCols;

    public:
        Matrix(unsigned numRows, unsigned numCols, const T& initVal);
        Matrix(const Matrix<T>& rhs);
        ~Matrix();

        // Accessing elements of the matrix
        T& operator()(const unsigned& row, const unsigned& col);
        const T& operator()(const unsigned& row, const unsigned& col) const;

        // Operator overloading, for "standard" mathematical matrix operations
        Matrix<T>& operator=(const Matrix<T>& rhs);

        // Matrix-Matrix ops
        // Ideally these should be outside the class
        Matrix<T> operator+(const Matrix<T>& rhs);
        Matrix<T>& operator+=(const Matrix<T>& rhs);
        Matrix<T> operator-(const Matrix<T>& rhs);
        Matrix<T>& operator-=(const Matrix<T>& rhs);
        Matrix<T> operator*(const Matrix<T>& rhs);
        Matrix<T>& operator*=(const Matrix<T>& rhs);
        Matrix<T> transpose();

        // Matrix-Scalar ops
        Matrix<T> operator+(const T& rhs);
        Matrix<T> operator-(const T& rhs);
        Matrix<T> operator*(const T& rhs);
        Matrix<T> operator/(const T& rhs);

        // Matrix-Vector ops
        std::vector<T> operator*(const std::vector<T>& rhs);

        // Functions that return the size of the matrix
        unsigned get_num_rows() const;
        unsigned get_num_cols() const;
};
```

## QR decomposition (also useful in solving linear least squares problem)

```cpp
template<typename T>
void QRSolve(const Matrix<T>& inMatA, const std::vector<T>& inVecb,
        std::vector<T>& outVecx) {

    unsigned rows = inMatA.get_num_rows();
    unsigned cols = inMatA.get_num_cols();

    double *A = new double[rows * cols];
    double *b = new double[inVecb.size()];

     // Convert input Matrix and vector into a format that honors Lapack API;
    // Lapack has column-major order
    for (unsigned col = 0, D1_idx = 0; col < cols; ++col) {
        for (unsigned row = 0; row < rows; ++row) {
            A[D1_idx++] = inMatA(row, col);
        }
        b[col] = inVecb[col];
    }

    for (unsigned row = 0; row < rows; ++row) {
        b[row] = inVecb[row];
    }

    // DGEQRF for Q*R=A, i.e., A and tau hold R and Householder reflectors
    double* tau = new double[cols];
    lapack::geqrf(rows, cols, A, rows, tau); // In place computation of R

    // DORMQR: to compute b := Q^T*b
    lapack::ormqr('L', 'T', rows, 1, cols, A, rows, tau, b, rows); // In place operation

    // DTRTRS: solve Rx=b by back substitution
    lapack::trtrs('U', 'N', 'N', cols, 1, A, rows, b, rows); // In place back substitution

    for (unsigned col = 0; col < cols; col++) {
        outVecx[col] = b[col];
    }

    delete[] A;
    delete[] b;
    delete[] tau;
    return;
}
```
