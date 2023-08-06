from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import collections
import numpy as np

import nngen.operator as operator

from . import util


def Squeeze(visitor, node):
    args = []

    for arg in node.input:
        arg_obj = visitor.visit(arg)
        args.append(arg_obj)

    args = [util.optimize_to_raw_value(arg) for arg in args]

    input = args[0]

    if isinstance(input, operator.matmul) and input.onnx_batchnorm is not None:
        return input

    axes = []
    for attribute in node.attribute:
        if attribute.name == 'axes':
            axes = [i for i in attribute.ints]

    if len(axes) == 0:
        for i, s in enumerate(input.shape):
            if i == 1:
                axes.append(i)

    if isinstance(input, (tuple, list)):
        input = np.array(input)

    if isinstance(input, np.ndarray):
        ret = input
        offset = 0

        for axis in sorted(axes):
            ret = np.squeeze(ret, axis - offset)
            offset += 1

        return ret

    layout = input.get_layout()
    onnx_layout = input.get_onnx_layout()

    if layout is not None and onnx_layout is not None:
        axes = [layout.index(onnx_layout[axis]) for axis in axes]
        axes.sort()

    name = util.get_name(node)

    new_shape = input.shape[:]
    offset = 0

    for axis in sorted(axes):
        new_shape.pop(axis - offset)
        offset += 1

    return operator.reshape(input, new_shape, name=name)


def Unsqueeze(visitor, node):
    args = []

    for arg in node.input:
        arg_obj = visitor.visit(arg)
        args.append(arg_obj)

    args = [util.optimize_to_raw_value(arg) for arg in args]

    input = args[0]

    for attribute in node.attribute:
        if attribute.name == 'axes':
            axes = attribute.ints

    name = util.get_name(node)

    ret = input
    offset = 0

    for axis in sorted(axes):
        if isinstance(ret, (tuple, list)):
            ret = np.array(ret)

        if isinstance(ret, (np.ndarray, np.float, np.int, float, int)):
            ret = np.expand_dims(ret, axis + offset)

        else:
            kwargs = collections.OrderedDict()
            kwargs['name'] = '{}_{}'.format(name, offset)
            ret = operator.expand_dims(ret, axis + offset, **kwargs)

        offset += 1

    return ret
