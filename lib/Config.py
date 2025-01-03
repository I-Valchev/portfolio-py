import yaml
import os


class Config:
    def __init__(self, portfolio):
        # Construct the path dynamically based on the portfolio folder
        config_path = os.path.join(portfolio, 'config.yaml')
        
        # Open the config.yaml file from the portfolio directory
        with open(config_path, 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        
        # Store the portfolio name
        self.portfolio = portfolio

    def getPrettyPlatforms(self):
        return list(map(lambda p: p['pretty'], self.config['platforms'].values()))

    def getPlatforms(self):
        return self.config['platforms'].keys()

    def getPortfolio(self):
        return self.portfolio
