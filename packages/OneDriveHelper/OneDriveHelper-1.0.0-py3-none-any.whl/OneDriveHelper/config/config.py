import os
import yaml


class config:
    def __init__(self):
        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(
                __file__)))  # https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
        self.config = self.get_config()

    def get_config(self):
        """
        Get config file
        :return: config
        :rtype: dict
        """
        with open(os.path.join(self.__location__, 'config.yaml')) as f:
            docs = yaml.load(f)
            return dict(docs)
