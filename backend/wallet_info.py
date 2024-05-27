from datetime import datetime, timedelta

class WalletInfo:
    def __init__(self, wallet_id: str, wallet_name: str):
        self.wallet_id = wallet_id
        self.wallet_name = wallet_name
        self.current_earning = 0.0
        self.previous_earning = 0.0
        self.gain_amount = 0.0
        self.gain_is_old = False
        self.gain_history = []  # List to store tuples of (timestamp, gain)

    def update_earnings(self, new_earning: float) -> None:
        """Update the earnings for this wallet."""
        now = datetime.now()
        if self.previous_earning == 0.0:
            self.gain_amount = 0.0
        else:
            self.gain_amount = new_earning - self.previous_earning
        
        self.previous_earning = self.current_earning
        self.current_earning = new_earning
        self.gain_history.append((now, self.gain_amount))
        self.clean_old_gains(now)

    def clean_old_gains(self, current_time: datetime) -> None:
        """Remove gain data older than 24 hours."""
        cutoff_time = current_time - timedelta(hours=24)
        self.gain_history = [(time, gain) for time, gain in self.gain_history if time >= cutoff_time]

    def calculate_24h_gain(self) -> float:
        """Calculate total gain over the past 24 hours."""
        return sum(gain for time, gain in self.gain_history)

    def calculate_average_hourly_gain(self) -> float:
        """Calculate average hourly gain over the past 24 hours."""
        if not self.gain_history:
            return 0.0

        hours = 24
        return self.calculate_24h_gain() / hours