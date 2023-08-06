from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


def slice_(value, begins, ends, strides,
           dtype=None, name=None, par=1,
           value_ram_size=None, out_ram_size=None,
           value_dtype=None):

    slices = to_slices(begins, ends, strides)
    return value[slices]


def to_slices(begins, ends, strides):
    slices = []

    for begin, end, stride in zip(begins, ends, strides):
        slices.append(slice(begin, end, stride))

    return tuple(slices)
