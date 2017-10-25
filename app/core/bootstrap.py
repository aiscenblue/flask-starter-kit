from flask import Flask
from app.core.blueprint import CoreBlueprint
from config.app import DevelopmentConfig as Config
from os import path as os_path


class Bootstrap:

    __app = None
    __root_dir = None

    def __init__(self, main_dir, *args):
        self.__root_dir = os_path.dirname(main_dir)
        self.__app = Flask(__name__, instance_relative_config=True)

        if len(args):
            self.system_config(system=args[0])

        self.configuration(Config)

    def system_config(self, system):
        if len(system) > 1:
            if '--debug' in system:
                setattr(Config, 'DEBUG', system[2])
        self.configuration(conf=Config)

    def configuration(self, conf):
        """ configuration file fore core module """
        self.__app.config.from_object(conf)

    def start(self):
        """ for blueprint registration """
        CoreBlueprint(app=self.__app, root_path='.module')
        self.__app.run(host=Config.HOST, port=Config.PORT)
