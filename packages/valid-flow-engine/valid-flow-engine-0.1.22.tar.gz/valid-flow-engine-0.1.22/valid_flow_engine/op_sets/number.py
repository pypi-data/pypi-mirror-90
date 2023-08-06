from typing import List

from valid_flow_engine.op_set_registry import register_op_set, as_op

@register_op_set
class NumberOpSet:
    @staticmethod
    @as_op(display='Sum Of', help_text='Sum of a set of numbers')
    def sum(of: List[float]):
        return sum(of)

    @staticmethod
    @as_op(display='Difference Of', help_text='X minus of the numbers in the list')
    def diff(x: float, of: List[float]):
        for arg in of:
            x -= arg
        return x

    @staticmethod
    @as_op(display='Product', help_text='Multiply all numbers provided')
    def product(of: List[float]):
        base = of[0]
        for arg in of[1:]:
            base *= arg
        return base

    @staticmethod
    @as_op(display='Quotient', help_text='Numerator divided by all denomenators')
    def quotient(numerator: float, denomenators: List[float]):
        for arg in denomenators:
            numerator /= arg
        return numerator

    @staticmethod
    @as_op(display='Maximum', help_text='Find maximum of a set of numbers')
    def max(of: List[float]):
        return max(of)

    @staticmethod
    @as_op(display='Minimum', help_text='Find minimum of a set of numbers')
    def min(of: List[float]):
        return min(of)

    @staticmethod
    @as_op(display='Raise to', help_text='Base, raised to the exponent powert')
    def pow(base: float, exponent: float):
        return base**exponent

    @staticmethod
    @as_op(display='Root of', help_text='nth root of base')
    def root(base: float, n: float):
        return base**(1/n)
