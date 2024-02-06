"""
A context processor is a function that takes in the request variable as argument and returns a dictionary that gets added to the request context
"""

from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
