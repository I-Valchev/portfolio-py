import yaml
import os


class Config:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        config_path = os.path.join(self.getPortfolioDir(), 'config.yaml')

        with open(config_path, 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def getPortfolioDir(self):
        """Returns the directory path for the selected portfolio."""
        return os.path.join('data', self.portfolio)

    def getPrettyPlatforms(self):
        return [p['pretty'] for p in self.config['platforms'].values()]

    def getPlatforms(self):
        return self.config['platforms'].keys()

    def getPortfolio(self):
        return self.portfolio
