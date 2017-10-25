from flask import Blueprint
from module.home.methods import index

""" blueprint module for url handler """
__method__ = Blueprint(__name__, __name__)

""" 
    ROUTES:
        routing for base directory module
        name, slug, function, methods
"""
__routes__ = [
    ("home", "/", index, ['GET'])
]
