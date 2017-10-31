from flask import Blueprint
from module.api.v1.posts.methods import Methods

""" blueprint module for url handler """
__method__ = Blueprint(__name__, __name__)

""" 
    ROUTES:
        routing for base directory module
        name, slug, function, methods
"""
__routes__ = [
    (__name__, "/", Methods)
]
