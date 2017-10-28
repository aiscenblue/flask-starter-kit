import sys
from flask_app_core import Bootstrap
from app.config.app import DevelopmentConfig


if __name__ == "__main__":
    bootstrap = Bootstrap(__name__, __file__, sys.argv, config=DevelopmentConfig)
    bootstrap.start()
