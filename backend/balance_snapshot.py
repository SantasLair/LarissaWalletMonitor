from datetime import datetime


class BalanceSnapshot:
    def __init__(self, balance, timestamp=None):
        self.balance = balance
        self.timestamp = timestamp if timestamp else datetime.now()

    def __repr__(self):
        return f"BalanceSnapshot(balance={self.balance}, timestamp={self.timestamp})"
