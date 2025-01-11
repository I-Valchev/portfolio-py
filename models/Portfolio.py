from models.Platform import Platform
from lib.Config import Config
from lib.helpers import generatePlatforms


class Portfolio:
    def __init__(self, config: Config):
        self.platforms = generatePlatforms(config)

    def calculateTotalUnrealizedGainLoss(self):
        """
        Calculates the unrealized gain/loss percentage for the entire portfolio,
        based on all platforms combined.
        """
        total_value = sum(p.calculateBalance() + p.calculateReturn() for p in self.platforms)
        total_invested = sum(p.calculateBalance() for p in self.platforms)

        if total_invested > 0:
            unrealized_gain_loss = (total_value - total_invested) / total_invested * 100
        else:
            unrealized_gain_loss = 0.0  # Avoid division by zero if there are no investments

        return round(unrealized_gain_loss, 2)

    def calculatePortfolioValue(self):
        """Calculates the total value of the portfolio."""
        return round(sum(p.calculateBalance() + p.calculateReturn() for p in self.platforms), 2)