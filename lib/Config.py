import yaml
import os


class Config:
    def __init__(self, args):
        self.portfolio = args.portfolio
        self.summary = args.summary
        self.currency = args.currency
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

    def getCurrencyAdjustment(self):
        """Returns the currency adjustment factor based on the currency."""
        eurToBgn = 1.95583

        if self.currency == 'BGN' and self.__getPortfolioCurrency() == 'EUR':
            return eurToBgn
        elif self.currency == 'EUR' and self.__getPortfolioCurrency() == 'BGN':
            return 1/eurToBgn
        return 1.0
    
    def __getPortfolioCurrency(self):
        return self.config.get('currency', 'EUR')
