import sys
from app.core.bootstrap import Bootstrap


if __name__ == "__main__":
    bootstrap = Bootstrap(__file__, sys.argv)
    bootstrap.start()
