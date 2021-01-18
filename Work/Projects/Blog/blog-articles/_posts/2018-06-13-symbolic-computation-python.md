---
layout: post
title: 'Symbolic computation in python'
author: Bob
categories: [python]
image: assets/images/python.jpg
---

Basic arithmetic operations in python can easily be extended to custom objects by overriding **op** functions or **dunder** functions. While this might be easy and trivial in some cases, it is extremely useful in numerical software where the
required math can be done using symbolic expressions and constructing the AST.
This AST is then traversed and nodes are evaluated using custom objects.

For example,

```python
# Symbolic math
x = sympy.Symbol('x')
y = sympy.Symbol('y')
expr = str(x * 2 + y ** 2 + y * 2)

# Final substitution
a = CustomModel(np.arange(0, 1000, 10))
b = CustomModel(np.arange(0, 1000, 10))
subs2 = {'x': xval, 'y': yval}
c = eval_expr(str_expr, CustomEvaluator(), subs2)
```

The underlying data in these CustomModels could be numpy arrays. While these operations work for numpy datatypes by default, in compute heavy numerical software
this is extremely useful and powerful where one can <span style="color: red">extend to parallel computing using MPI (Message Passing Interface.)</span> Numpy arrays do not perform these arithmetic operations in parallel. We can decompose these numpy data in CustomModel and be used for parallel operations.

```python
def eval_expr(expr, eval_caller=None, subs=None):
    '''Evaluates a string expression.'''

    if eval_caller is None:
        eval_caller = Evaluator()

    if subs is None:
        frame = sys._getframe()
        subs = {}
        subs.update(frame.f_globals)
        subs.update(frame.f_back.f_globals)

    return eval_caller(ast.parse(expr, mode='eval').body, subs)


class IEvaluator:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, node, subs):
        '''
        :param node: ast.AST object.
        :param subs: dict. Dictionary with values to substitute.
        '''


class Evaluator(IEvaluator):

    @classmethod
    def _get_op(cls, node):
        # supported operators
        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.BitXor: op.xor,
            ast.USub: op.neg
        }
        return operators[type(node.op)]

    @classmethod
    def _num_op(cls, node, subs):
        return node.n

    @classmethod
    def _bin_op(cls, node, subs):
        op = cls._get_op(node)
        left_node = cls._eval(node.left, subs)
        right_node = cls._eval(node.right, subs)
        return op(left_node, right_node)

    @classmethod
    def _unary_op(cls, node, subs):
        op = cls._get_op(node)
        return op(cls._eval(node.operand, subs))

    @classmethod
    def _subs_op(cls, node, subs):
        try:
            return subs[node.id]
        except KeyError:
            raise TypeError(node)

    @classmethod
    def _eval(cls, node, subs):
        node_type = type(node)

        return {
            ast.Num: cls._num_op,
            ast.BinOp: cls._bin_op,
            ast.UnaryOp: cls._unary_op
        }.get(node_type, cls._subs_op)(node, subs)

    def __call__(self, node, subs):
        return self._eval(node, subs)


class CustomEvaluator(Evaluator):

    @classmethod
    def _num_op(cls, node, subs):
        return CustomModel(node.n)
```

Herein we use the following datatypes

```python
class CustomData(object):
    '''
    This class contains operations on objects of CustomData class.
    This assumes that that CustomData class has a variable called data.
    This can trivially be extended to add MPI functionality to
    either numpy data (left out of this exercise) or have this added to a
    another custom class.
    '''
    def __init__(self, data):
        self.data = data

    def __mul__(self, other):
        return CustomData(self.data * other.data)

    def __add__(self, other):
        return CustomData(self.data + other.data)

    def __pow__(self, other):
        return CustomData(self.data ** other.data)

class Scalar(CustomData):
    '''
    This is a Scalar class derived from CustomData (a specialization for scalars.)
    '''
    def __init__(self, scalar):
        self.data = scalar

class CustomModel(CustomData):
    '''
    This is a CustomModel class derived from CustomData.
    '''
    def __init__(self, data):
        self.data = data
```
