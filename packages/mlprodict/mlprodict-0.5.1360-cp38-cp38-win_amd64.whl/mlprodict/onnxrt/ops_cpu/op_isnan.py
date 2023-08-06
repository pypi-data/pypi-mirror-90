# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRunUnary


class IsNaN(OpRunUnary):

    def __init__(self, onnx_node, desc=None, **options):
        OpRunUnary.__init__(self, onnx_node, desc=desc,
                            **options)

    def _run(self, data):  # pylint: disable=W0221
        return (numpy.isnan(data), )

    def _infer_shapes(self, x):  # pylint: disable=W0221
        return (x.copy(dtype=numpy.bool), )

    def to_python(self, inputs):
        return self._to_python_numpy(inputs, 'isnan')
