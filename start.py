from flask_app_core import Bootstrap
from app.config.app import DevelopmentConfig


if __name__ == "__main__":
    bootstrap = Bootstrap(import_name=__name__, app_dir=__file__, config=DevelopmentConfig, environment='development')
    bootstrap.start()
