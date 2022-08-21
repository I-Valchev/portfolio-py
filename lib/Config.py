import yaml


class Config:
    def __init__(self):
        file = open('config.yaml')
        self.config = yaml.load(file, Loader=yaml.FullLoader)

    def getPrettyPlatforms(self):
        return list(map(lambda p: p['pretty'], self.config['platforms'].values()))

    def getPlatforms(self):
        return self.config['platforms'].keys()
