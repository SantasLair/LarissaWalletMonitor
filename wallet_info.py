from termcolor import colored

class WalletInfo:
    def __init__(self, wallet_id: str, wallet_name: str):
        self.wallet_id = wallet_id
        self.wallet_name = wallet_name
        self.current_earning = 0.0
        self.previous_earning = 0.0
        self.gain_amount = 0.0
        self.gain_is_old = False

    def update_earnings(self, new_earning: float) -> None:
        """Update the earnings for this wallet."""
        if new_earning == self.previous_earning:
            self.gain_is_old = True
            return

        if self.previous_earning > 0:
            self.gain_amount = new_earning - self.previous_earning
            self.gain_is_old = False

        self.previous_earning = self.current_earning
        self.current_earning = new_earning

    def display_earnings(self, width: int) -> None:
        """Display the earnings in a formatted way."""
        name_width = 30
        name_str = self.wallet_name.ljust(name_width)
        output = f"{name_str}: {self.current_earning:.4f}"
        
        if self.gain_amount != 0:
            gain_str = f" (+{self.gain_amount:.4f})"
            if self.gain_is_old:
                output += colored(gain_str, "yellow")
            else:
                output += gain_str
        
        print(output.center(width))
