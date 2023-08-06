# simple automatic differentiation for fun
import numpy as np
import types

# approximate the gradient of function f at point x
def grad(f, h=0.00001):
    # make sure f is a function:
    if not isinstance(f, types.FunctionType):
        raise Exception('Error: input f must be a function!')

    # get list of variable names of function f:
    args = list(f.__code__.co_varnames)
    if len(args) == 0:
        raise Exception('Error: function f has no inputs!')

    # define the gradient function:
    def gradient_function(*args):
        # if there are no arguments provided, raise an exception:
        if len(args) == 0:
            raise Exception('Error: gradient function received no inputs!')

        # extract the first argument and everything else:
        x = args[0]
        other_args = args[1:]

        # if the argument is a single number:
        if isinstance(x, (int, float)):
            # calculate the gradient:
            values = []
            for n in (x, x+h):
                values.append(f(n, *other_args))

            # approximate the gradient:
            return (values[1] - values[0]) / h

        # otherwise, if the argument is a list or a numpy array:
        elif isinstance(x, (list, np.ndarray)):
            # initialize the list of gradients:
            gradient_list = []

            # if x is a numpy array and not of type 64-bit float, cast it:
            if isinstance(x, np.ndarray) and (x.dtype != np.float64):
                x = x.astype('float64')

            # calculate the gradient for each dimension:
            fx = f(x, *other_args)
            for i in range(len(x)):
                x[i] += h
                f_ih = f(x, *other_args) # f_ih = f([x_0, x_1, ... i+h, ...])
                x[i] -= h

                # approximate the gradient in this dimension:
                gradient_list.append((f_ih - fx) / h)

            # return the approximated gradient:
            return gradient_list if isinstance(x, list) else np.array(gradient_list)

    # return the gradient function we defined:
    return gradient_function
