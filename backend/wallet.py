from datetime import datetime
from collections import deque
from backend.balance_snapshot import BalanceSnapshot


class Wallet:
    def __init__(self, wallet_id: str, wallet_name: str):
        """
        Initialize a Wallet instance.

        Args:
            wallet_id (str): Unique identifier for the wallet.
            wallet_name (str): Human-readable name for the wallet.
        """
        self.wallet_id = wallet_id
        self.wallet_name = wallet_name
        self.unclaimed_earnings = 0.0
        self.balance_snapshots = deque(maxlen=144)  # Using deque to limit snapshots efficiently

    def add_balance_snapshot(self, balance: float) -> None:
        """
        Add a balance snapshot for the wallet and limit history to 144 snapshots.

        Args:
            balance (float): The balance to snapshot.
        """
        now = datetime.now()
        self.balance_snapshots.append(BalanceSnapshot(balance, now))

    def get_balance_snapshots(self):
        """
        Get a list of balance snapshots.

        Returns:
            list: A list of balance snapshots.
        """
        return list(self.balance_snapshots)

    def calculate_gain(self, start_time: datetime, end_time: datetime) -> float:
        """
        Calculate gain over a specific time period.

        Args:
            start_time (datetime): The start time of the period.
            end_time (datetime): The end time of the period.

        Returns:
            float: The calculated gain or None if there is not enough data.
        """
        # Find the first snapshot that is at or after the start_time
        start_snapshot = next((s for s in self.balance_snapshots if s.timestamp >= start_time), None)
        # Find the last snapshot that is at or before the end_time
        end_snapshot = next((s for s in reversed(self.balance_snapshots) if s.timestamp <= end_time), None)

        # If either snapshot is missing, return None
        if start_snapshot is None or end_snapshot is None:
            return None

        return end_snapshot.balance - start_snapshot.balance

    def calculate_oldest_gain(self):
        """
        Calculate the gain from the oldest to the newest snapshot.

        Returns:
            tuple: The gain and the time period (start_time, end_time) over which it happened.
        """
        if len(self.balance_snapshots) < 2:
            return None, None, None  # Not enough data to calculate the gain

        start_snapshot = self.balance_snapshots[0]
        end_snapshot = self.balance_snapshots[-1]

        gain = end_snapshot.balance - start_snapshot.balance
        start_time = start_snapshot.timestamp
        end_time = end_snapshot.timestamp

        return gain, start_time, end_time