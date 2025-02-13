class Portfolio:
    def unrealisedGainLoss(self):
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

    def calculateCurrentValue(self) -> float:
        """Calculates the total value of the portfolio."""
        return round(sum(p.calculateBalance() + p.calculateReturn() for p in self.platforms), 2)
    
    def calculateBalance(self) -> float:
        """Calculates the total balance of the portfolio."""
        return round(sum(p.calculateBalance() for p in self.platforms), 2)